"""
Video processing utilities
"""
import os
import cv2
import logging
from datetime import datetime
from flask import current_app

logger = logging.getLogger(__name__)

def save_video_clip(frames, camera_id, event_id):
    """
    Save video clip from frames
    
    Args:
        frames: List of OpenCV frames
        camera_id: Camera identifier
        event_id: Event identifier
        
    Returns:
        Path to saved video file or None
    """
    try:
        if not frames:
            logger.warning("No frames provided to save")
            return None
        
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"event_{event_id}_{camera_id}_{timestamp}.mp4"
        filepath = os.path.join(current_app.config['DETECTED_EVENTS_FOLDER'], filename)
        
        # Get frame properties
        height, width = frames[0].shape[:2]
        fps = current_app.config['VIDEO_FPS']
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
        
        # Write frames
        for frame in frames:
            out.write(frame)
        
        out.release()
        
        logger.info(f"Video clip saved: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error saving video clip: {str(e)}")
        return None


def save_frame_image(frame, camera_id, event_id):
    """
    Save single frame as image
    
    Args:
        frame: OpenCV frame
        camera_id: Camera identifier
        event_id: Event identifier
        
    Returns:
        Path to saved image file or None
    """
    try:
        if frame is None:
            logger.warning("No frame provided to save")
            return None
        
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"event_{event_id}_{camera_id}_{timestamp}.jpg"
        filepath = os.path.join(current_app.config['DETECTED_EVENTS_FOLDER'], filename)
        
        # Save image
        cv2.imwrite(filepath, frame)
        
        logger.info(f"Frame image saved: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error saving frame image: {str(e)}")
        return None


def resize_frame(frame, width=None, height=None):
    """
    Resize frame maintaining aspect ratio
    
    Args:
        frame: OpenCV frame
        width: Target width
        height: Target height
        
    Returns:
        Resized frame
    """
    if frame is None:
        return None
    
    h, w = frame.shape[:2]
    
    if width is None and height is None:
        return frame
    
    if width is None:
        # Calculate width based on height
        aspect_ratio = w / h
        width = int(height * aspect_ratio)
    elif height is None:
        # Calculate height based on width
        aspect_ratio = h / w
        height = int(width * aspect_ratio)
    
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    return resized


def encode_frame_to_jpeg(frame, quality=85):
    """
    Encode frame to JPEG bytes
    
    Args:
        frame: OpenCV frame
        quality: JPEG quality (0-100)
        
    Returns:
        JPEG encoded bytes
    """
    if frame is None:
        return None
    
    try:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
        
        if result:
            return encoded_frame.tobytes()
        
        return None
        
    except Exception as e:
        logger.error(f"Error encoding frame: {str(e)}")
        return None


def cleanup_old_files(directory, days=30):
    """
    Clean up old files from directory
    
    Args:
        directory: Directory path
        days: Delete files older than this many days
        
    Returns:
        Number of files deleted
    """
    try:
        if not os.path.exists(directory):
            return 0
        
        deleted_count = 0
        current_time = datetime.now()
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            if os.path.isfile(filepath):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                age_days = (current_time - file_modified).days
                
                if age_days > days:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.info(f"Deleted old file: {filename}")
        
        return deleted_count
        
    except Exception as e:
        logger.error(f"Error cleaning up old files: {str(e)}")
        return 0
