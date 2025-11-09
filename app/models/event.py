"""
Event model for storing detection events
"""
from datetime import datetime
from app import db

class Event(db.Model):
    """Detection event model"""
    
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    camera_id = db.Column(db.String(64), nullable=False)
    camera_name = db.Column(db.String(128))
    
    # Detection details
    object_type = db.Column(db.String(64), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    bounding_box = db.Column(db.Text)  # JSON string: {x, y, width, height}
    
    # Media files
    image_path = db.Column(db.String(256))
    video_path = db.Column(db.String(256))
    
    # Alert status
    alert_sent = db.Column(db.Boolean, default=False)
    alert_sent_at = db.Column(db.DateTime)
    
    # User reference
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Additional metadata
    notes = db.Column(db.Text)
    is_reviewed = db.Column(db.Boolean, default=False)
    reviewed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert event to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'camera_id': self.camera_id,
            'camera_name': self.camera_name,
            'object_type': self.object_type,
            'confidence': self.confidence,
            'bounding_box': self.bounding_box,
            'image_path': self.image_path,
            'video_path': self.video_path,
            'alert_sent': self.alert_sent,
            'is_reviewed': self.is_reviewed,
            'notes': self.notes
        }
    
    def mark_as_reviewed(self, notes=None):
        """Mark event as reviewed"""
        self.is_reviewed = True
        self.reviewed_at = datetime.utcnow()
        if notes:
            self.notes = notes
        db.session.commit()
    
    def __repr__(self):
        return f'<Event {self.id}: {self.object_type} at {self.timestamp}>'
