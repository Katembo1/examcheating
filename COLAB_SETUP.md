# Google Colab Setup Guide

## 🌐 Running Smart Surveillance System on Google Colab with Ngrok

This guide will help you run your Flask application on Google Colab and make it accessible via a public ngrok URL.

---

## 📋 Prerequisites

1. **Ngrok Account**: Sign up at [https://ngrok.com](https://ngrok.com)
2. **Ngrok Auth Token**: Get it from [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. **Google Account**: For accessing Google Colab

---

## 🚀 Setup Instructions

### Step 1: Get Your Ngrok Auth Token

1. Go to [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Sign up or log in
3. Copy your auth token (it looks like: `2efObXdvDqYyUTd3tq6pNB6vxzG_iFmhkfeYj4LgdvgGPLCL`)
4. Save it - you'll need it in the next step

### Step 2: Update Your .env File

Open your `.env` file and update these values:

```properties
# Ngrok Configuration (for Google Colab / Public URL)
NGROK_AUTH_TOKEN=your-actual-ngrok-token-here
USE_NGROK=True
```

**Replace** `your-actual-ngrok-token-here` with your actual ngrok auth token.

### Step 3: Upload to Google Colab

1. Open [Google Colab](https://colab.research.google.com/)
2. Create a new notebook
3. Upload your entire project folder or clone from GitHub

---

## 📝 Google Colab Notebook Setup

Copy and paste these cells into your Colab notebook:

### Cell 1: Install System Dependencies

```python
# Install system dependencies
!apt-get update
!apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
```

### Cell 2: Clone Your Repository (if using GitHub)

```python
# If your code is on GitHub
!git clone https://github.com/Katembo1/examcheating.git
%cd examcheating/code
```

**OR** Upload your files manually using Colab's file upload feature.

### Cell 3: Install Python Dependencies

```python
# Install all required packages
!pip install -r requirements.txt
```

### Cell 4: Set Up Environment Variables

```python
# Create .env file with your credentials
import os

env_content = """
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///surveillance.db

# Roboflow API Configuration
ROBOFLOW_API_KEY=3IU9udNBJgg1CMyaG6Z8
ROBOFLOW_WORKSPACE=jkat
ROBOFLOW_PROJECT=Laxt
ROBOFLOW_VERSION=1
ROBOFLOW_WORKFLOW_ID=detect-count-and-visualize
MAX_FPS=15

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=japhet simeon
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=jphtkatembo1841@gmail.com
ALERT_EMAIL_RECIPIENT=japhetsimeon755@gmail.com

# Camera Configuration
CAMERA_SOURCE=0

# Detection Configuration
CONFIDENCE_THRESHOLD=0.5
DETECTION_CLASSES=cheating,normal
FRAME_SKIP=2
MAX_CAMERAS=4

# Storage Configuration
MAX_VIDEO_CLIP_DURATION=10
RETENTION_DAYS=30

# Ngrok Configuration
NGROK_AUTH_TOKEN=YOUR_ACTUAL_NGROK_TOKEN_HERE
USE_NGROK=True
"""

# Write to .env file
with open('.env', 'w') as f:
    f.write(env_content)

print("✅ .env file created!")
print("⚠️  Remember to replace YOUR_ACTUAL_NGROK_TOKEN_HERE with your real token!")
```

### Cell 5: Initialize Database

```python
# Initialize the database
!python run.py init-db
```

### Cell 6: Create Admin User

```python
# Create admin user programmatically
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created!")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("ℹ️  Admin user already exists")
```

### Cell 7: Run the Application

```python
# Run the Flask app with ngrok
!python run.py
```

---

## 🎉 Accessing Your Application

After running Cell 7, you should see output like:

```
======================================================================
🚀 Creating ngrok tunnel...
======================================================================
✅ Smart Surveillance System is LIVE!
🌐 Public URL: https://abc123.ngrok-free.app
📹 Workflow Detection: https://abc123.ngrok-free.app/workflow
📊 Dashboard: https://abc123.ngrok-free.app/dashboard
🔐 Login: https://abc123.ngrok-free.app/login
======================================================================

⚠️  Keep this window open while using the application
⚠️  Share the public URL with anyone to access your app
```

**Click on the public URL** to access your application from anywhere!

---

## 🔐 Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Change these after first login!**

---

## 📹 Using Webcam on Colab

**Important**: Google Colab doesn't have direct access to your local webcam. You have two options:

### Option 1: Upload a Video File
1. Upload a test video to Colab
2. In the workflow dashboard, select the "Video File" tab
3. Enter the path to your uploaded video (e.g., `/content/test_video.mp4`)

### Option 2: Use RTSP Stream
1. Set up a camera streaming service (like IP Webcam app on your phone)
2. Get the RTSP URL
3. In the workflow dashboard, select "RTSP Stream" tab
4. Enter your RTSP URL

### Option 3: Use YouTube Video
1. Find a YouTube video URL
2. In the workflow dashboard, you can potentially use it as a source
3. Or use yt-dlp to download it first

---

## 🛠️ Troubleshooting

### Issue: "NGROK_AUTH_TOKEN not set"
**Solution**: Make sure you've replaced `YOUR_ACTUAL_NGROK_TOKEN_HERE` in Cell 4 with your real ngrok token.

### Issue: "pyngrok not installed"
**Solution**: Run `!pip install pyngrok` in a new cell.

### Issue: Ngrok URL not working
**Solution**: 
- Check if the cell is still running (you should see `[*]` next to it)
- The ngrok URL expires when you stop the cell
- Restart Cell 7 to get a new URL

### Issue: "Max connections reached" on ngrok
**Solution**: 
- Free ngrok accounts have connection limits
- Close old tunnels or upgrade to a paid plan
- Or wait a few minutes and try again

### Issue: Database errors
**Solution**: Run Cell 5 again to reinitialize the database.

### Issue: Low FPS / Laggy Video
**Solution**: 
- Colab's resources are limited
- Reduce `MAX_FPS` in .env to 10 or 15
- Use smaller video files
- Close other notebooks

---

## 💡 Tips for Best Performance

1. **Lower FPS**: Set `MAX_FPS=10` or `MAX_FPS=15` in .env for better performance on Colab
2. **Use GPU**: Go to Runtime > Change runtime type > Select GPU (if needed)
3. **Keep Cell Running**: Don't interrupt Cell 7 while using the app
4. **Monitor Resources**: Use `!nvidia-smi` to check GPU usage
5. **Session Timeout**: Colab sessions timeout after ~12 hours or 90 minutes of inactivity

---

## 🔄 Restarting the Application

If you need to restart:

1. Click the **Stop** button on Cell 7
2. Wait for it to fully stop
3. Run Cell 7 again
4. You'll get a new ngrok URL

---

## 📤 Sharing Your Application

1. Copy the ngrok public URL from the output
2. Share it with your lecturer or teammates
3. They can access it from any device with internet
4. **Note**: The URL changes every time you restart

---

## 🎓 Demo Tips for Lecturers

1. **Prepare beforehand**: Set everything up 15 minutes before your presentation
2. **Test the URL**: Open it on your phone to verify it's working
3. **Use a test video**: Upload a pre-recorded video showing cheating behaviors
4. **Enable dark mode**: Looks better on projectors
5. **Show stats**: Demonstrate the real-time FPS, frame count, and detection results

---

## ⚠️ Important Notes

- **Free Tier Limits**: Ngrok free tier has connection limits and session duration limits
- **Session Persistence**: Your Colab session will timeout after inactivity
- **URL Changes**: You get a new URL every time you restart the application
- **No Local Webcam**: Colab can't access your computer's webcam directly
- **API Costs**: Remember Roboflow API calls still count against your quota

---

## 📞 Need Help?

If you encounter issues:
1. Check the error messages in the Colab cell output
2. Verify all credentials in .env are correct
3. Make sure your ngrok token is valid
4. Check Roboflow API key is working
5. Try reducing MAX_FPS if performance is poor

---

## 🎯 Quick Start Summary

```bash
# 1. Get ngrok token from https://dashboard.ngrok.com
# 2. Upload code to Colab or clone from GitHub
# 3. Run these commands in order:

!apt-get update && apt-get install -y libgl1-mesa-glx
!pip install -r requirements.txt
# Update .env with your ngrok token and set USE_NGROK=True
!python run.py init-db
!python run.py  # This creates ngrok tunnel and runs the app
```

That's it! Your Smart Surveillance System is now publicly accessible! 🚀
