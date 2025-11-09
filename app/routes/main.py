"""
Main application routes
"""
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.event import Event
from app import db
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.workflow'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get recent events
    recent_events = Event.query.order_by(desc(Event.timestamp)).limit(10).all()
    
    # Get statistics
    total_events = Event.query.count()
    unreviewed_events = Event.query.filter_by(is_reviewed=False).count()
    alerts_sent = Event.query.filter_by(alert_sent=True).count()
    
    stats = {
        'total_events': total_events,
        'unreviewed_events': unreviewed_events,
        'alerts_sent': alerts_sent
    }
    
    return render_template('dashboard.html', 
                         recent_events=recent_events,
                         stats=stats)

@main_bp.route('/events')
@login_required
def events():
    """Events management page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    events_pagination = Event.query.order_by(desc(Event.timestamp)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('events.html', events=events_pagination)

@main_bp.route('/cameras')
@login_required
def cameras():
    """Camera management page"""
    return render_template('cameras.html')

@main_bp.route('/settings')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html')

@main_bp.route('/workflow')
@login_required
def workflow():
    """Workflow-based detection page"""
    return render_template('workflow_dashboard.html')
