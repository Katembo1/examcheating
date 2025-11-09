"""
Workflow-based API routes using Roboflow InferencePipeline
"""
from flask import Blueprint, jsonify, request, Response, current_app
from flask_login import login_required, current_user
from app import db
from app.models.event import Event
from app.utils.workflow_detector import WorkflowDetector
from app.utils.email_alerts import send_alert_email
from app.utils.video_utils import save_frame_image
import cv2
import json
import numpy as np
import time
import logging
from datetime import datetime

workflow_api_bp = Blueprint('workflow_api', __name__)
logger = logging.getLogger(__name__)

# Global workflow detector instance
workflow_detector = None

def get_workflow_detector():
    """Get or create workflow detector instance"""
    global workflow_detector
    if workflow_detector is None:
        workflow_detector = WorkflowDetector()
    return workflow_detector

@workflow_api_bp.route('/start-workflow-detection', methods=['POST'])
@login_required
def start_workflow_detection():
    """
    Start workflow-based detection
    Body: {
        "camera_source": "0" or "video_url" or "rtsp://..."
    }
    """
    try:
        data = request.get_json() or {}
        camera_source = data.get('camera_source', current_app.config['CAMERA_SOURCE'])
        
        # Convert "0" string to integer for webcam
        if camera_source == "0" or camera_source == 0:
            camera_source = 0
        
        detector = get_workflow_detector()
        result = detector.start_detection(camera_source)
        
        if result['success']:
            logger.info(f"Workflow detection started for source: {camera_source}")
            return jsonify(result)
        else:
            logger.error(f"Failed to start workflow detection: {result['message']}")
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error starting workflow detection: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@workflow_api_bp.route('/stop-workflow-detection', methods=['POST'])
@login_required
def stop_workflow_detection():
    """Stop workflow-based detection"""
    try:
        detector = get_workflow_detector()
        result = detector.stop_detection()
        
        logger.info("Workflow detection stopped")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error stopping workflow detection: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@workflow_api_bp.route('/workflow-status', methods=['GET'])
@login_required
def workflow_status():
    """Get workflow detection status"""
    try:
        detector = get_workflow_detector()
        status = detector.get_status()
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Error getting workflow status: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@workflow_api_bp.route('/workflow-video-feed')
@login_required
def workflow_video_feed():
    """
    Video streaming route for workflow-based detection
    Returns: Multipart JPEG stream
    """
    def generate():
        detector = get_workflow_detector()
        last_yield = 0
        
        while True:
            try:
                # Throttle frame delivery to ~15 FPS for smooth browser rendering
                current_time = time.time()
                if current_time - last_yield < 0.066:  # ~15 FPS
                    time.sleep(0.01)
                    continue
                
                # Get processed frame from detector
                frame_bytes = detector.get_frame()
                
                if frame_bytes:
                    last_yield = current_time
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                else:
                    # Send blank frame when no data available
                    blank = np.zeros((480, 640, 3), dtype=np.uint8)
                    
                    # Add status text
                    status = detector.get_status()
                    if status['is_running']:
                        text = f'Processing... Frames: {status["frame_count"]}'
                        color = (0, 255, 0)
                    else:
                        text = 'Waiting for detection to start...'
                        color = (255, 255, 255)
                    
                    cv2.putText(blank, text, (150, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    
                    # Encode blank frame
                    ret, buffer = cv2.imencode('.jpg', blank, 
                                              [cv2.IMWRITE_JPEG_QUALITY, 85])
                    if ret:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                    
                    time.sleep(0.1)
                    
            except GeneratorExit:
                logger.info("Video feed client disconnected")
                break
            except Exception as e:
                logger.error(f"Error in workflow video feed: {e}")
                time.sleep(0.1)
    
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@workflow_api_bp.route('/workflow-predictions', methods=['GET'])
@login_required
def workflow_predictions():
    """Get latest predictions from workflow"""
    try:
        detector = get_workflow_detector()
        predictions = detector.get_predictions()
        detections = detector.parse_detections()
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'detections': detections
        })
        
    except Exception as e:
        logger.error(f"Error getting workflow predictions: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@workflow_api_bp.route('/save-detection-event', methods=['POST'])
@login_required
def save_detection_event():
    """
    Save a detection event to the database
    Body: {
        "camera_id": "camera_1",
        "camera_name": "Main Camera",
        "detections": [...]
    }
    """
    try:
        data = request.get_json()
        camera_id = data.get('camera_id', 'default')
        camera_name = data.get('camera_name', 'Camera')
        detections = data.get('detections', [])
        
        detector = get_workflow_detector()
        
        # Save each detection as an event
        saved_events = []
        for detection in detections:
            event = Event(
                camera_id=camera_id,
                camera_name=camera_name,
                object_type=detection.get('class', 'unknown'),
                confidence=detection.get('confidence', 0.0),
                bounding_box=json.dumps(detection.get('bbox', [])),
                user_id=current_user.id
            )
            
            db.session.add(event)
            db.session.flush()
            
            # Save frame image
            frame_bytes = detector.get_frame()
            if frame_bytes:
                # Convert bytes back to image
                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is not None:
                    image_path = save_frame_image(frame, camera_id, event.id)
                    event.image_path = image_path
            
            saved_events.append(event.to_dict())
        
        db.session.commit()
        
        logger.info(f"Saved {len(saved_events)} detection events")
        
        return jsonify({
            'success': True,
            'message': f'Saved {len(saved_events)} events',
            'events': saved_events
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving detection event: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@workflow_api_bp.route('/test-workflow', methods=['GET'])
@login_required
def test_workflow():
    """Test workflow configuration"""
    try:
        api_key = current_app.config.get('ROBOFLOW_API_KEY')
        workspace = current_app.config.get('ROBOFLOW_WORKSPACE')
        workflow_id = current_app.config.get('ROBOFLOW_WORKFLOW_ID')
        
        return jsonify({
            'success': True,
            'config': {
                'api_key_set': bool(api_key),
                'workspace': workspace,
                'workflow_id': workflow_id,
                'max_fps': current_app.config.get('MAX_FPS')
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
