"""
API routes for AJAX requests and video streaming
"""
from flask import Blueprint, jsonify, request, Response, current_app
from flask_login import login_required, current_user
from app import db
from app.models.event import Event
from app.utils.detector import ObjectDetector
from app.utils.camera import CameraManager
from app.utils.email_alerts import send_alert_email, send_test_email
from app.utils.video_utils import save_frame_image, save_video_clip, encode_frame_to_jpeg
import cv2
import json
import logging
from datetime import datetime

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# Global instances
camera_manager = None
detector = None
detection_active = False

def get_camera_manager():
    """Get or create camera manager instance"""
    global camera_manager
    if camera_manager is None:
        camera_manager = CameraManager()
    return camera_manager

def get_detector():
    """Get or create detector instance"""
    global detector
    if detector is None:
        detector = ObjectDetector()
    return detector

@api_bp.route('/start-detection', methods=['POST'])
@login_required
def start_detection():
    """Start object detection"""
    global detection_active
    
    try:
        data = request.get_json()
        camera_id = data.get('camera_id', 'default')
        camera_source = data.get('camera_source', current_app.config['CAMERA_SOURCE'])
        
        manager = get_camera_manager()
        
        # Add camera if not exists
        if not manager.get_camera(camera_id):
            if not manager.add_camera(camera_id, camera_source):
                return jsonify({'success': False, 'message': 'Failed to initialize camera'}), 400
        
        detection_active = True
        logger.info(f"Detection started for camera {camera_id}")
        
        return jsonify({
            'success': True,
            'message': 'Detection started successfully'
        })
        
    except Exception as e:
        logger.error(f"Error starting detection: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/stop-detection', methods=['POST'])
@login_required
def stop_detection():
    """Stop object detection"""
    global detection_active
    
    try:
        detection_active = False
        manager = get_camera_manager()
        manager.stop_all_cameras()
        
        logger.info("Detection stopped")
        
        return jsonify({
            'success': True,
            'message': 'Detection stopped successfully'
        })
        
    except Exception as e:
        logger.error(f"Error stopping detection: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/video-feed/<camera_id>')
@login_required
def video_feed(camera_id):
    """Video streaming route"""
    def generate():
        manager = get_camera_manager()
        det = get_detector()
        frame_count = 0
        
        while detection_active:
            frame = manager.get_frame(camera_id)
            
            if frame is None:
                continue
            
            # Perform detection on every Nth frame
            if frame_count % current_app.config['FRAME_SKIP'] == 0:
                detections = det.detect_objects(frame)
                
                # Save event if objects detected
                if detections:
                    for detection in detections:
                        event = Event(
                            camera_id=camera_id,
                            camera_name=f"Camera {camera_id}",
                            object_type=detection['class'],
                            confidence=detection['confidence'],
                            bounding_box=json.dumps(detection['bbox']),
                            user_id=current_user.id
                        )
                        
                        # Save frame image
                        db.session.add(event)
                        db.session.flush()
                        
                        frame_with_boxes = det.draw_detections(frame, detections)
                        image_path = save_frame_image(frame_with_boxes, camera_id, event.id)
                        event.image_path = image_path
                        
                        db.session.commit()
                        
                        # Send alert email (in background)
                        if not event.alert_sent:
                            send_alert_email({
                                'object_type': detection['class'],
                                'confidence': detection['confidence'],
                                'camera_id': camera_id,
                                'camera_name': f"Camera {camera_id}"
                            })
                            event.alert_sent = True
                            event.alert_sent_at = datetime.utcnow()
                            db.session.commit()
                
                # Draw detections on frame
                frame = det.draw_detections(frame, detections)
            
            frame_count += 1
            
            # Encode frame to JPEG
            jpeg_bytes = encode_frame_to_jpeg(frame)
            
            if jpeg_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n')
    
    return Response(generate(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@api_bp.route('/events', methods=['GET'])
@login_required
def get_events():
    """Get events data"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        events_query = Event.query.order_by(Event.timestamp.desc())
        
        # Filtering
        object_type = request.args.get('object_type')
        if object_type:
            events_query = events_query.filter_by(object_type=object_type)
        
        reviewed = request.args.get('reviewed')
        if reviewed is not None:
            events_query = events_query.filter_by(is_reviewed=reviewed == 'true')
        
        # Pagination
        pagination = events_query.paginate(page=page, per_page=per_page, error_out=False)
        
        events_data = [event.to_dict() for event in pagination.items]
        
        return jsonify({
            'success': True,
            'events': events_data,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        })
        
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/events/<int:event_id>/review', methods=['POST'])
@login_required
def review_event(event_id):
    """Mark event as reviewed"""
    try:
        event = Event.query.get_or_404(event_id)
        data = request.get_json()
        notes = data.get('notes', '')
        
        event.mark_as_reviewed(notes)
        
        return jsonify({
            'success': True,
            'message': 'Event marked as reviewed'
        })
        
    except Exception as e:
        logger.error(f"Error reviewing event: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/cameras', methods=['GET'])
@login_required
def get_cameras():
    """Get active cameras"""
    try:
        manager = get_camera_manager()
        cameras = manager.get_all_cameras()
        
        cameras_data = [
            {
                'id': cam_id,
                'source': cam.source,
                'is_active': cam.is_active
            }
            for cam_id, cam in cameras.items()
        ]
        
        return jsonify({
            'success': True,
            'cameras': cameras_data
        })
        
    except Exception as e:
        logger.error(f"Error fetching cameras: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/test-email', methods=['POST'])
@login_required
def test_email():
    """Send test email"""
    try:
        success = send_test_email()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Test email sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send test email'
            }), 500
            
    except Exception as e:
        logger.error(f"Error sending test email: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get system statistics"""
    try:
        from sqlalchemy import func
        from datetime import timedelta
        
        # Get counts
        total_events = Event.query.count()
        unreviewed_events = Event.query.filter_by(is_reviewed=False).count()
        alerts_sent = Event.query.filter_by(alert_sent=True).count()
        
        # Events by type
        events_by_type = db.session.query(
            Event.object_type,
            func.count(Event.id)
        ).group_by(Event.object_type).all()
        
        # Events in last 24 hours
        day_ago = datetime.utcnow() - timedelta(days=1)
        recent_events = Event.query.filter(Event.timestamp >= day_ago).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_events': total_events,
                'unreviewed_events': unreviewed_events,
                'alerts_sent': alerts_sent,
                'recent_events': recent_events,
                'events_by_type': dict(events_by_type)
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500
