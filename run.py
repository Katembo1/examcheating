"""
Smart Surveillance System - Main Entry Point
"""
import os
from app import create_app, db, socketio
from app.models.user import User
from app.models.event import Event

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Event': Event
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized successfully!")

@app.cli.command()
def create_admin():
    """Create an admin user"""
    from werkzeug.security import generate_password_hash
    
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    admin = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        is_admin=True
    )
    
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user '{username}' created successfully!")

if __name__ == '__main__':
    # Run the application with SocketIO support
    socketio.run(
        app,
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
