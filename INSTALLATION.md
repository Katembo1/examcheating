# Smart Surveillance System - Installation Guide

## Quick Start (Windows)

Follow these steps to get your surveillance system running:

### 1. Install Python
- Download Python 3.8 or higher from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify installation: `python --version`

### 2. Open PowerShell in the project directory
```powershell
cd "c:\Users\user\OneDrive\Documents\Exam Project\code"
```

### 3. Create a virtual environment
```powershell
python -m venv venv
```

### 4. Activate the virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Install dependencies
```powershell
pip install -r requirements.txt
```

### 6. Configure environment variables
```powershell
copy .env.example .env
```

Then edit `.env` file with your settings:
- Add your Roboflow API key
- Configure email settings for alerts
- Set camera source (0 for webcam, or RTSP URL for IP camera)

### 7. Initialize the database
```powershell
python
```
Then in Python:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
exit()
```

Or use the CLI command:
```powershell
python run.py init-db
```

### 8. Create an admin user
```powershell
python run.py create-admin
```

### 9. Run the application
```powershell
python run.py
```

### 10. Access the application
Open your browser and go to: http://localhost:5000

## Troubleshooting

### Camera not detected
- Make sure your webcam is connected
- Try different camera indices (0, 1, 2) in the .env file
- Check Windows camera permissions

### Roboflow errors
- Verify your API key is correct
- Check internet connection
- Ensure project name and version match your Roboflow project

### Email alerts not working
- For Gmail, use an App Password instead of your regular password
- Go to Google Account > Security > 2-Step Verification > App Passwords
- Generate an app password for "Mail"
- Use this password in the .env file

## Next Steps

1. Login with your admin account
2. Go to Dashboard
3. Click "Start Detection" to begin monitoring
4. Configure detection settings in Settings page
5. Review detected events in the Events page

For more details, see README.md
