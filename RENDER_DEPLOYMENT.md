# Render Deployment Guide - Smart Surveillance System

## 🚀 Deploying to Render

Render is a modern cloud platform that makes it easy to deploy your Flask application with a free tier option.

---

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be on GitHub
2. **Render Account** - Sign up at [https://render.com](https://render.com)
3. **Roboflow API Key** - From your Roboflow dashboard

---

## 🔧 Step 1: Prepare Your Repository

### Push to GitHub

1. Make sure your code is committed to your GitHub repository:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. Verify these files exist in your repo:
   - ✅ `requirements.txt`
   - ✅ `Procfile`
   - ✅ `render.yaml`
   - ✅ `run.py`
   - ✅ `env.env` (optional - we'll set env vars in Render)

---

## 🌐 Step 2: Create a Render Account

1. Go to [https://render.com](https://render.com)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with your GitHub account (recommended)
4. Authorize Render to access your GitHub repositories

---

## 📦 Step 3: Create a New Web Service

### Option A: Using render.yaml (Automatic - Recommended)

1. **In Render Dashboard:**
   - Click **"New +"** button
   - Select **"Blueprint"**
   
2. **Connect Repository:**
   - Select your `examcheating` repository
   - Render will detect the `render.yaml` file
   - Click **"Apply"**

3. **Render will automatically create:**
   - Web Service
   - PostgreSQL Database (if needed)
   - All environment variables

### Option B: Manual Setup

1. **In Render Dashboard:**
   - Click **"New +"** button
   - Select **"Web Service"**

2. **Connect Repository:**
   - Click **"Connect GitHub"**
   - Search for `examcheating`
   - Click **"Connect"**

3. **Configure Service:**
   - **Name**: `smart-surveillance-system`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank (or `code` if needed)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT run:app`

4. **Select Plan:**
   - Choose **"Free"** plan (or upgrade for better performance)

---

## 🔑 Step 4: Set Environment Variables

In your Render service dashboard, go to **"Environment"** tab and add:

### Required Variables:

```
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=generate-a-random-secret-key-here
```

### Roboflow Configuration:

```
ROBOFLOW_API_KEY=3IU9udNBJgg1CMyaG6Z8
ROBOFLOW_WORKSPACE=jkat
ROBOFLOW_PROJECT=Laxt
ROBOFLOW_VERSION=1
ROBOFLOW_WORKFLOW_ID=detect-count-and-visualize
MAX_FPS=15
```

### Detection Settings:

```
CONFIDENCE_THRESHOLD=0.5
DETECTION_CLASSES=cheating,normal
FRAME_SKIP=2
CAMERA_SOURCE=0
```

### Optional (Email Alerts):

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
ALERT_EMAIL_RECIPIENT=recipient@example.com
```

### Important Settings:

```
USE_NGROK=False
DATABASE_URL=postgresql://... (auto-generated if using database)
```

**💡 Tip:** Click the **"Generate"** button next to SECRET_KEY for a secure random key.

---

## 🗄️ Step 5: Add Database (Optional)

If you want persistent storage:

1. **Create PostgreSQL Database:**
   - Click **"New +"** → **"PostgreSQL"**
   - Name: `surveillance-db`
   - Select **Free** plan
   - Click **"Create Database"**

2. **Connect to Web Service:**
   - Go to your web service
   - Environment tab
   - Add variable: `DATABASE_URL`
   - Select **"Database URL"** from your database
   - Or manually copy the Internal Database URL

3. **Update Config:**
   - The `DATABASE_URL` will automatically be used by SQLAlchemy
   - Render will create the connection

---

## 🚀 Step 6: Deploy

1. **Click "Create Web Service"** or **"Manual Deploy"**
2. **Wait for Build:**
   - Watch the build logs
   - This takes 5-10 minutes on first deploy
   - Subsequent deploys are faster

3. **Check Logs:**
   - Click on **"Logs"** tab
   - Look for: `✅ Smart Surveillance System is LIVE!`
   - Or errors if something went wrong

4. **Get Your URL:**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - Example: `https://smart-surveillance-system.onrender.com`

---

## 🔍 Step 7: Initialize Database

After first deployment, you need to create the database tables:

### Option A: Using Render Shell

1. Go to your service dashboard
2. Click **"Shell"** tab at the top
3. Run:
   ```bash
   python run.py init-db
   ```

### Option B: Using API Call

Create an admin user by accessing:
```
https://your-app-name.onrender.com/init
```
(You'll need to create this route)

### Option C: Add Initialization to run.py

The database will auto-create on first run if you have this in `run.py`:
```python
with app.app_context():
    db.create_all()
```

---

## 🎯 Step 8: Create Admin User

### Method 1: Using Shell (Recommended)

1. In Render Dashboard → **Shell** tab:
   ```python
   from app import create_app, db
   from app.models.user import User
   from werkzeug.security import generate_password_hash
   
   app = create_app()
   with app.app_context():
       admin = User(
           username='admin',
           email='admin@example.com',
           password_hash=generate_password_hash('admin123'),
           is_admin=True
       )
       db.session.add(admin)
       db.session.commit()
       print("Admin created!")
   ```

### Method 2: Create Initialization Route

Add to your Flask app:
```python
@app.route('/setup-admin')
def setup_admin():
    # Add authentication check here
    from werkzeug.security import generate_password_hash
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
        return "Admin created!"
    return "Admin already exists"
```

---

## 📱 Step 9: Access Your App

1. **Get Your URL:**
   - Format: `https://your-service-name.onrender.com`
   - Find it in your Render dashboard

2. **Test the App:**
   - Open: `https://your-service-name.onrender.com`
   - Login with admin credentials
   - Navigate to: `/workflow` for detection

3. **Share the URL:**
   - This is your permanent public URL
   - Share with your lecturer or team
   - No need for ngrok!

---

## ⚙️ Important Configuration Notes

### 1. Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for demos)
- Upgrade to paid plan for always-on service

### 2. Camera Source

On Render, you **cannot** use local webcams (Camera ID 0). Instead:

**Option A: Upload Video Files**
```python
CAMERA_SOURCE=/opt/render/project/src/uploads/test_video.mp4
```

**Option B: Use RTSP Streams**
```python
CAMERA_SOURCE=rtsp://camera-ip:port/stream
```

**Option C: YouTube URLs**
- Process YouTube videos for testing

### 3. Performance Optimization

Set these for better performance on free tier:
```
MAX_FPS=10
FRAME_SKIP=3
CONFIDENCE_THRESHOLD=0.6
```

### 4. File Storage

- Render's free tier has **ephemeral storage**
- Uploaded files are deleted on restart
- Use **Render Disks** (paid) or **external storage** (S3, Cloudinary) for persistence

---

## 🔧 Troubleshooting

### Build Fails

**Check:**
- All packages in `requirements.txt` are valid
- Python version is compatible
- No typos in package names

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
```

### Application Crashes

**Check Logs:**
1. Go to **Logs** tab in Render
2. Look for Python errors
3. Common issues:
   - Missing environment variables
   - Database connection errors
   - Import errors

**Fix:**
- Add missing environment variables
- Check DATABASE_URL is set
- Verify all imports are in requirements.txt

### Database Errors

**Problem:** `sqlalchemy.exc.OperationalError`

**Solution:**
- Ensure DATABASE_URL is set correctly
- Run `init-db` in shell
- Check database is created and accessible

### Slow Performance

**Solutions:**
1. Reduce MAX_FPS to 5-10
2. Increase FRAME_SKIP to 3-5
3. Upgrade to paid plan for more resources
4. Use smaller video files

### CORS Errors

**Add to run.py:**
```python
from flask_cors import CORS
CORS(app)
```

**Add to requirements.txt:**
```
flask-cors
```

---

## 🔄 Updating Your Deployment

### Automatic Deploy (Recommended)

1. **Enable Auto-Deploy:**
   - Go to service settings
   - Enable **"Auto-Deploy"**
   - Every push to `main` branch deploys automatically

2. **Push Changes:**
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
   
3. **Render automatically:**
   - Detects the push
   - Rebuilds the app
   - Deploys the new version

### Manual Deploy

1. Go to Render dashboard
2. Click **"Manual Deploy"**
3. Select **"Deploy latest commit"**

---

## 📊 Monitoring

### View Logs

1. **Real-time Logs:**
   - Dashboard → **Logs** tab
   - See all application output
   - Filter by severity

2. **Download Logs:**
   - Click download icon
   - Save for debugging

### Metrics

On paid plans:
- CPU usage
- Memory usage
- Request counts
- Response times

---

## 💰 Pricing

### Free Tier
- ✅ 750 hours/month
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Spins down after inactivity
- ⚠️ Limited resources

### Starter Plan ($7/month)
- ✅ Always on
- ✅ More resources
- ✅ Faster builds
- ✅ Priority support

### Professional Plan ($25/month)
- ✅ Horizontal scaling
- ✅ Advanced metrics
- ✅ Zero-downtime deploys

---

## 🎓 Demo Tips for Lecturers

### Before Presentation:

1. **Wake Up Service:**
   - Visit your URL 5 minutes before
   - Let it spin up if it was sleeping

2. **Prepare Test Video:**
   - Upload a demo video showing cheating
   - Or use a YouTube URL

3. **Test Everything:**
   - Login works
   - Video detection works
   - Dashboard displays correctly

### During Presentation:

1. **Show the URL:**
   - Demonstrate it's publicly accessible
   - Open on phone to show responsiveness

2. **Explain the Deployment:**
   - Mention Render platform
   - Show it's production-ready
   - Discuss scalability

3. **Demonstrate Features:**
   - Real-time detection
   - Dark mode toggle
   - Stats and metrics

---

## 📝 Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] `requirements.txt` updated
- [ ] `Procfile` created
- [ ] `render.yaml` created
- [ ] Roboflow API key ready
- [ ] Secret key generated

After deploying:
- [ ] Service is running
- [ ] No errors in logs
- [ ] Environment variables set
- [ ] Database initialized
- [ ] Admin user created
- [ ] Can access via public URL
- [ ] Detection works with test video

---

## 🆘 Support

**Render Documentation:**
- [https://render.com/docs](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-flask)

**Community:**
- [Render Community Forum](https://community.render.com)
- [Discord Server](https://render.com/discord)

**Your Repository:**
- [GitHub Issues](https://github.com/Katembo1/examcheating/issues)

---

## 🎉 Success!

Your Smart Surveillance System is now deployed on Render with a public URL that you can share with anyone! 

**Your app URL:** `https://your-service-name.onrender.com`

No more localhost or ngrok - you have a production-ready application! 🚀
