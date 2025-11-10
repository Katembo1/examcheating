"""
Smart Surveillance System - Main Entry Point
"""
import os
from dotenv import load_dotenv
from app import create_app, db, socketio
from app.models.user import User
from app.models.event import Event

# Load environment variables
load_dotenv()

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
    # Check if ngrok should be used (for Google Colab)
    use_ngrok = os.getenv('USE_NGROK', 'False').lower() == 'true'
    
    if use_ngrok:
        try:
            from pyngrok import ngrok
            from pyngrok.conf import PyngrokConfig
            
            # Get ngrok auth token from environment
            ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')
            
            if not ngrok_auth_token or ngrok_auth_token == 'your-ngrok-auth-token-here':
                print("=" * 70)
                print("⚠️  WARNING: NGROK_AUTH_TOKEN not set!")
                print("Please set your ngrok auth token in .env file")
                print("Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken")
                print("=" * 70)
            else:
                # Set ngrok auth token
                ngrok.set_auth_token(ngrok_auth_token)
                
                # Configure ngrok
                pyngrok_config = PyngrokConfig()
                
                # Close any existing tunnels
                try:
                    existing_tunnels = ngrok.get_tunnels()
                    for tunnel in existing_tunnels:
                        print(f"Closing existing tunnel: {tunnel.public_url}")
                        ngrok.disconnect(tunnel.public_url)
                except Exception:
                    pass
                
                # Create ngrok tunnel
                flask_port = 5000
                print("\n" + "=" * 70)
                print("🚀 Creating ngrok tunnel...")
                public_url = ngrok.connect(flask_port, pyngrok_config=pyngrok_config).public_url
                
                print("=" * 70)
                print(f"✅ Smart Surveillance System is LIVE!")
                print(f"🌐 Public URL: {public_url}")
                print(f"📹 Workflow Detection: {public_url}/workflow")
                print(f"📊 Dashboard: {public_url}/dashboard")
                print(f"🔐 Login: {public_url}/login")
                print("=" * 70)
                print("\n⚠️  Keep this window open while using the application")
                print("⚠️  Share the public URL with anyone to access your app\n")
                
        except ImportError:
            print("=" * 70)
            print("⚠️  pyngrok not installed!")
            print("Install it with: pip install pyngrok")
            print("=" * 70)
            use_ngrok = False
        except Exception as e:
            print(f"❌ Error setting up ngrok: {e}")
            use_ngrok = False
    
    # Run the application with SocketIO support
    print("\n🔧 Starting Flask application...")
    socketio.run(
        app,
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False if use_ngrok else True  # Disable reloader with ngrok
    )
