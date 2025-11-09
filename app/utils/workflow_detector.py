"""
Roboflow Workflow-based Object Detection using InferencePipeline
This uses the InferencePipeline approach for real-time video processing
"""
import cv2
import numpy as np
import threading
import time
import logging
from flask import current_app
from inference import InferencePipeline

logger = logging.getLogger(__name__)

class WorkflowDetector:
    """
    Roboflow InferencePipeline-based detector with custom workflow
    This approach is more efficient for continuous video streams
    """
    
    def __init__(self):
        """Initialize the workflow detector"""
        self.pipeline = None
        self.is_running = False
        self.current_frame = None
        self.latest_predictions = None
        self.lock = threading.Lock()
        self.frame_count = 0
        self.error_message = None
        self.video_source = None
        
    def frame_sink(self, result, video_frame):
        """
        Callback function that receives processed frames from InferencePipeline
        
        Args:
            result: Dictionary containing predictions and processed image
            video_frame: Raw video frame object
        """
        with self.lock:
            try:
                # Get the processed image with bounding boxes drawn
                if result.get("output_image"):
                    self.current_frame = result["output_image"].numpy_image
                    self.frame_count += 1
                # Fallback to raw frame if no output image
                elif video_frame is not None:
                    if hasattr(video_frame, 'image'):
                        self.current_frame = video_frame.image
                    elif hasattr(video_frame, 'numpy_image'):
                        self.current_frame = video_frame.numpy_image
                    self.frame_count += 1
                
                # Store predictions for analysis
                self.latest_predictions = result
                
                # Log progress periodically
                if self.frame_count % 30 == 0:
                    logger.info(f"Processed frame {self.frame_count}")
                    
            except Exception as e:
                logger.error(f"Error in frame_sink: {e}")
                self.error_message = str(e)
    
    def start_detection(self, video_source=0):
        """
        Start the detection pipeline
        
        Args:
            video_source: Camera index (0 for webcam) or video path/URL
            
        Returns:
            dict: Status of the operation
        """
        if self.is_running:
            return {"success": False, "message": "Detection already running"}
        
        try:
            # Get configuration from Flask app
            api_key = current_app.config.get('ROBOFLOW_API_KEY')
            workspace = current_app.config.get('ROBOFLOW_WORKSPACE')
            workflow_id = current_app.config.get('ROBOFLOW_WORKFLOW_ID', 'detect-count-and-visualize')
            max_fps = current_app.config.get('MAX_FPS', 30)
            
            if not api_key:
                return {"success": False, "message": "Roboflow API key not configured"}
            
            self.video_source = video_source
            
            # Convert string "0" to integer 0 for webcam
            video_reference = video_source
            if video_source == "0" or video_source == 0:
                video_reference = 0
            
            # Initialize InferencePipeline with workflow (simplified approach)
            logger.info(f"Initializing InferencePipeline with workflow {workflow_id}")
            logger.info(f"Workspace: {workspace}, Video source: {video_reference}")
            
            self.pipeline = InferencePipeline.init_with_workflow(
                api_key=api_key,
                workspace_name=workspace,
                workflow_id=workflow_id,
                video_reference=video_reference,  # Path to video, device id, or RTSP stream url
                max_fps=max_fps,
                on_prediction=self.frame_sink
            )
            
            # Start the pipeline (non-blocking)
            self.pipeline.start()
            self.is_running = True
            
            logger.info("Detection pipeline started successfully")
            return {"success": True, "message": "Detection started"}
            
        except Exception as e:
            error_msg = f"Failed to start detection: {str(e)}"
            logger.error(error_msg)
            self.error_message = error_msg
            return {"success": False, "message": error_msg}
    
    def stop_detection(self):
        """
        Stop the detection pipeline
        
        Returns:
            dict: Status of the operation
        """
        if not self.is_running:
            return {"success": False, "message": "Detection not running"}
        
        try:
            if self.pipeline:
                self.pipeline.terminate()
                self.pipeline = None
            
            self.is_running = False
            self.current_frame = None
            self.latest_predictions = None
            
            logger.info("Detection pipeline stopped")
            return {"success": True, "message": "Detection stopped"}
            
        except Exception as e:
            error_msg = f"Error stopping detection: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    def get_frame(self):
        """
        Get the latest processed frame as JPEG bytes
        
        Returns:
            bytes: JPEG encoded frame or None
        """
        with self.lock:
            if self.current_frame is not None:
                # Encode with lower quality for faster transmission
                ret, buffer = cv2.imencode('.jpg', self.current_frame, 
                                          [cv2.IMWRITE_JPEG_QUALITY, 75])
                if ret:
                    return buffer.tobytes()
        return None
    
    def get_status(self):
        """
        Get current status of the detector
        
        Returns:
            dict: Status information
        """
        return {
            "is_running": self.is_running,
            "frame_count": self.frame_count,
            "has_frame": self.current_frame is not None,
            "video_source": self.video_source,
            "error_message": self.error_message,
            "predictions": self.latest_predictions
        }
    
    def get_predictions(self):
        """
        Get latest predictions from the workflow
        
        Returns:
            dict: Latest predictions or None
        """
        with self.lock:
            return self.latest_predictions
    
    def parse_detections(self):
        """
        Parse predictions into standardized detection format
        
        Returns:
            list: List of detection dictionaries
        """
        if not self.latest_predictions:
            return []
        
        detections = []
        try:
            # Parse workflow predictions (format may vary based on workflow)
            predictions = self.latest_predictions.get('predictions', [])
            
            for pred in predictions:
                detection = {
                    'class': pred.get('class', pred.get('class_name', 'unknown')),
                    'confidence': pred.get('confidence', 0.0),
                    'bbox': self._extract_bbox(pred)
                }
                detections.append(detection)
                
        except Exception as e:
            logger.error(f"Error parsing detections: {e}")
        
        return detections
    
    def _extract_bbox(self, pred):
        """
        Extract bounding box from prediction in various formats
        
        Args:
            pred: Prediction dictionary
            
        Returns:
            list: [x, y, width, height]
        """
        try:
            # Format 1: x, y, width, height
            if 'x' in pred and 'y' in pred and 'width' in pred and 'height' in pred:
                return [
                    int(pred['x'] - pred['width'] / 2),
                    int(pred['y'] - pred['height'] / 2),
                    int(pred['width']),
                    int(pred['height'])
                ]
            # Format 2: bbox array
            elif 'bbox' in pred:
                return pred['bbox']
            # Format 3: bounding_box object
            elif 'bounding_box' in pred:
                bb = pred['bounding_box']
                return [bb.get('x', 0), bb.get('y', 0), 
                       bb.get('width', 0), bb.get('height', 0)]
        except Exception as e:
            logger.error(f"Error extracting bbox: {e}")
        
        return [0, 0, 0, 0]
