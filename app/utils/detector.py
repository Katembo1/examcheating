"""
Object Detection using Roboflow API
"""
import os
import cv2
import numpy as np
from roboflow import Roboflow
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class ObjectDetector:
    """Roboflow-based object detection"""
    
    def __init__(self):
        """Initialize Roboflow detector"""
        self.model = None
        self.confidence_threshold = current_app.config['CONFIDENCE_THRESHOLD']
        self.detection_classes = current_app.config['DETECTION_CLASSES']
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize Roboflow model"""
        try:
            api_key = current_app.config['ROBOFLOW_API_KEY']
            workspace = current_app.config['ROBOFLOW_WORKSPACE']
            project = current_app.config['ROBOFLOW_PROJECT']
            version = current_app.config['ROBOFLOW_VERSION']
            
            if not api_key:
                logger.warning("Roboflow API key not configured. Detection will not work.")
                return
            
            rf = Roboflow(api_key=api_key)
            project_obj = rf.workspace(workspace).project(project)
            self.model = project_obj.version(version).model
            
            logger.info("Roboflow model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Roboflow model: {str(e)}")
            self.model = None
    
    def detect_objects(self, frame):
        """
        Detect objects in a frame
        
        Args:
            frame: OpenCV image (numpy array)
            
        Returns:
            List of detections with format:
            [{'class': str, 'confidence': float, 'bbox': [x, y, w, h]}, ...]
        """
        if self.model is None:
            logger.warning("Model not initialized. Cannot perform detection.")
            return []
        
        try:
            # Save frame temporarily
            temp_path = 'temp_frame.jpg'
            cv2.imwrite(temp_path, frame)
            
            # Perform inference
            predictions = self.model.predict(temp_path, confidence=self.confidence_threshold).json()
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Parse predictions
            detections = []
            for pred in predictions.get('predictions', []):
                class_name = pred['class']
                
                # Filter by detection classes
                if class_name.lower() in [c.lower() for c in self.detection_classes]:
                    detection = {
                        'class': class_name,
                        'confidence': pred['confidence'],
                        'bbox': [
                            int(pred['x'] - pred['width'] / 2),
                            int(pred['y'] - pred['height'] / 2),
                            int(pred['width']),
                            int(pred['height'])
                        ]
                    }
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection error: {str(e)}")
            return []
    
    def draw_detections(self, frame, detections):
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: OpenCV image
            detections: List of detection dictionaries
            
        Returns:
            Frame with drawn detections
        """
        frame_copy = frame.copy()
        
        for detection in detections:
            x, y, w, h = detection['bbox']
            class_name = detection['class']
            confidence = detection['confidence']
            
            # Draw bounding box
            color = (0, 255, 0)  # Green
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), color, 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame_copy, (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), color, -1)
            cv2.putText(frame_copy, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return frame_copy
    
    def update_confidence_threshold(self, threshold):
        """Update confidence threshold"""
        self.confidence_threshold = threshold
        logger.info(f"Confidence threshold updated to {threshold}")
    
    def update_detection_classes(self, classes):
        """Update detection classes"""
        self.detection_classes = classes
        logger.info(f"Detection classes updated to {classes}")
