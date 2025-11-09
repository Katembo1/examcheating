"""
Utility functions package
"""
from app.utils.detector import ObjectDetector
from app.utils.camera import CameraManager
from app.utils.email_alerts import send_alert_email
from app.utils.video_utils import save_video_clip

__all__ = ['ObjectDetector', 'CameraManager', 'send_alert_email', 'save_video_clip']
