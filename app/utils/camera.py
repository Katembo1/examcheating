"""
Camera management and video stream handling
"""
import cv2
import threading
import logging
from flask import current_app

logger = logging.getLogger(__name__)

class Camera:
    """Individual camera handler"""
    
    def __init__(self, camera_id, source):
        """
        Initialize camera
        
        Args:
            camera_id: Unique camera identifier
            source: Camera source (0 for webcam, RTSP URL for IP camera)
        """
        self.camera_id = camera_id
        self.source = source
        self.video_capture = None
        self.is_active = False
        self.current_frame = None
        self.lock = threading.Lock()
        self.thread = None
    
    def start(self):
        """Start camera capture"""
        if self.is_active:
            logger.warning(f"Camera {self.camera_id} is already active")
            return False
        
        try:
            # Try to convert source to int (for webcam index)
            try:
                source = int(self.source)
            except ValueError:
                source = self.source
            
            self.video_capture = cv2.VideoCapture(source)
            
            if not self.video_capture.isOpened():
                logger.error(f"Failed to open camera {self.camera_id} with source {self.source}")
                return False
            
            # Set camera properties
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, current_app.config['VIDEO_WIDTH'])
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, current_app.config['VIDEO_HEIGHT'])
            self.video_capture.set(cv2.CAP_PROP_FPS, current_app.config['VIDEO_FPS'])
            
            self.is_active = True
            
            # Start frame capture thread
            self.thread = threading.Thread(target=self._capture_frames, daemon=True)
            self.thread.start()
            
            logger.info(f"Camera {self.camera_id} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting camera {self.camera_id}: {str(e)}")
            return False
    
    def stop(self):
        """Stop camera capture"""
        self.is_active = False
        
        if self.thread:
            self.thread.join(timeout=2.0)
        
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        
        self.current_frame = None
        logger.info(f"Camera {self.camera_id} stopped")
    
    def _capture_frames(self):
        """Internal method to continuously capture frames"""
        while self.is_active:
            try:
                ret, frame = self.video_capture.read()
                
                if ret:
                    with self.lock:
                        self.current_frame = frame
                else:
                    logger.warning(f"Failed to read frame from camera {self.camera_id}")
                    
            except Exception as e:
                logger.error(f"Error capturing frame from camera {self.camera_id}: {str(e)}")
    
    def get_frame(self):
        """Get current frame"""
        with self.lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
        return None
    
    def is_opened(self):
        """Check if camera is opened"""
        return self.video_capture is not None and self.video_capture.isOpened()


class CameraManager:
    """Manage multiple cameras"""
    
    def __init__(self):
        """Initialize camera manager"""
        self.cameras = {}
        self.max_cameras = current_app.config['MAX_CAMERAS']
    
    def add_camera(self, camera_id, source):
        """
        Add a new camera
        
        Args:
            camera_id: Unique camera identifier
            source: Camera source
            
        Returns:
            True if camera added successfully
        """
        if len(self.cameras) >= self.max_cameras:
            logger.warning(f"Maximum number of cameras ({self.max_cameras}) reached")
            return False
        
        if camera_id in self.cameras:
            logger.warning(f"Camera {camera_id} already exists")
            return False
        
        camera = Camera(camera_id, source)
        if camera.start():
            self.cameras[camera_id] = camera
            logger.info(f"Camera {camera_id} added successfully")
            return True
        
        return False
    
    def remove_camera(self, camera_id):
        """Remove a camera"""
        if camera_id in self.cameras:
            self.cameras[camera_id].stop()
            del self.cameras[camera_id]
            logger.info(f"Camera {camera_id} removed")
            return True
        
        logger.warning(f"Camera {camera_id} not found")
        return False
    
    def get_camera(self, camera_id):
        """Get camera by ID"""
        return self.cameras.get(camera_id)
    
    def get_frame(self, camera_id):
        """Get frame from specific camera"""
        camera = self.get_camera(camera_id)
        if camera:
            return camera.get_frame()
        return None
    
    def get_all_cameras(self):
        """Get all cameras"""
        return self.cameras
    
    def stop_all_cameras(self):
        """Stop all cameras"""
        for camera_id in list(self.cameras.keys()):
            self.remove_camera(camera_id)
        logger.info("All cameras stopped")
    
    def get_camera_count(self):
        """Get number of active cameras"""
        return len(self.cameras)
