"""
Email alert functionality
"""
import logging
from flask import current_app, render_template_string
from flask_mail import Message
from app import mail
from datetime import datetime

logger = logging.getLogger(__name__)

def send_alert_email(event_data):
    """
    Send email alert for detection event
    
    Args:
        event_data: Dictionary containing event information
        
    Returns:
        True if email sent successfully
    """
    try:
        recipient = current_app.config['ALERT_EMAIL_RECIPIENT']
        
        if not recipient:
            logger.warning("Alert email recipient not configured")
            return False
        
        # Email subject
        subject = f"Security Alert: {event_data.get('object_type', 'Object')} Detected"
        
        # Email body (HTML)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .detail-row {{ padding: 10px 0; border-bottom: 1px solid #ddd; }}
                .detail-label {{ font-weight: bold; display: inline-block; width: 150px; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 Security Alert</h1>
                    <p>Object Detected in Surveillance Area</p>
                </div>
                
                <div class="content">
                    <h2>Detection Details</h2>
                    
                    <div class="detail-row">
                        <span class="detail-label">Object Type:</span>
                        <span>{event_data.get('object_type', 'Unknown')}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Confidence:</span>
                        <span>{event_data.get('confidence', 0) * 100:.1f}%</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Camera:</span>
                        <span>{event_data.get('camera_name', event_data.get('camera_id', 'Unknown'))}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Time:</span>
                        <span>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Location:</span>
                        <span>{event_data.get('location', 'Surveillance Area')}</span>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 20px 0;">
                    <p>Please review the surveillance system for more details.</p>
                    <a href="http://localhost:5000/dashboard" 
                       style="background-color: #007bff; color: white; padding: 10px 20px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        View Dashboard
                    </a>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from Smart Surveillance System</p>
                    <p>© 2025 Smart Surveillance System. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        text_body = f"""
        SECURITY ALERT
        
        Object Type: {event_data.get('object_type', 'Unknown')}
        Confidence: {event_data.get('confidence', 0) * 100:.1f}%
        Camera: {event_data.get('camera_name', event_data.get('camera_id', 'Unknown'))}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Location: {event_data.get('location', 'Surveillance Area')}
        
        Please review the surveillance system for more details.
        
        ---
        Smart Surveillance System
        """
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=text_body,
            html=html_body
        )
        
        # Send email
        mail.send(msg)
        logger.info(f"Alert email sent to {recipient}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send alert email: {str(e)}")
        return False


def send_test_email():
    """
    Send a test email to verify configuration
    
    Returns:
        True if test email sent successfully
    """
    try:
        recipient = current_app.config['ALERT_EMAIL_RECIPIENT']
        
        if not recipient:
            logger.error("Alert email recipient not configured")
            return False
        
        msg = Message(
            subject="Smart Surveillance System - Test Email",
            recipients=[recipient],
            body="This is a test email from Smart Surveillance System. Email configuration is working correctly!",
            html="""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #28a745;">✓ Email Configuration Test</h2>
                    <p>This is a test email from <strong>Smart Surveillance System</strong>.</p>
                    <p>Email configuration is working correctly!</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">Smart Surveillance System © 2025</p>
                </body>
            </html>
            """
        )
        
        mail.send(msg)
        logger.info(f"Test email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send test email: {str(e)}")
        return False
