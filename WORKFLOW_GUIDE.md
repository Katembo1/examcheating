# Roboflow Workflow Integration Guide

## Overview
Your Smart Surveillance System now supports **two detection modes**:

### 1. **Standard Detection** (Original)
- Uses Roboflow model API directly
- Frame-by-frame processing
- Accessible via `/dashboard`

### 2. **Workflow Detection** (New - Optimized)
- Uses Roboflow InferencePipeline with custom workflows
- Real-time streaming pipeline
- More efficient for continuous video streams
- Accessible via `/workflow`

## Configuration

### Environment Variables (.env)
```env
# Roboflow API Configuration
ROBOFLOW_API_KEY=3IU9udNBJgg1CMyaG6Z8
ROBOFLOW_WORKSPACE=jkat
ROBOFLOW_PROJECT=your-project-name
ROBOFLOW_VERSION=1
ROBOFLOW_WORKFLOW_ID=custom-workflow-3
MAX_FPS=10

# Detection Classes
DETECTION_CLASSES=cheating,normal

# Camera Source
CAMERA_SOURCE=0
```

## New API Endpoints

### `/api/workflow/start-workflow-detection` (POST)
Start workflow-based detection
```json
{
  "camera_source": "0"  // or URL, RTSP, video path
}
```

### `/api/workflow/stop-workflow-detection` (POST)
Stop workflow-based detection

### `/api/workflow/workflow-status` (GET)
Get detection status and frame count

### `/api/workflow/workflow-video-feed` (GET)
Video stream with detections drawn

### `/api/workflow/workflow-predictions` (GET)
Get latest predictions from workflow

### `/api/workflow/save-detection-event` (POST)
Save detection to database

## Features

### Workflow Detection Benefits:
✅ **Better Performance**: Uses InferencePipeline for efficient processing
✅ **Real-time Processing**: Continuous video stream handling
✅ **Throttling Control**: MAX_FPS prevents queue backlog
✅ **Auto-annotation**: Bounding boxes drawn automatically
✅ **Multiple Sources**: Supports webcam, RTSP, video files, YouTube URLs

### Supported Video Sources:
- **Webcam**: `0` or `1`
- **RTSP Stream**: `rtsp://username:password@ip:port/stream`
- **Video File**: `/path/to/video.mp4`
- **YouTube**: `https://www.youtube.com/watch?v=...`
- **HTTP Stream**: `http://your-stream-url/video`

## How to Use

### 1. Install Additional Dependencies
```powershell
pip install inference inference-sdk
```

### 2. Restart the Application
```powershell
python run.py
```

### 3. Access Workflow Detection
- Navigate to: `http://localhost:5000/workflow`
- Select camera source
- Click "Start Detection"
- View real-time annotated video feed

## Key Differences

| Feature | Standard Detection | Workflow Detection |
|---------|-------------------|-------------------|
| API Type | Direct Model API | InferencePipeline |
| Processing | Frame-by-frame | Continuous stream |
| Performance | Good for single frames | Optimized for video |
| Setup | Simple | Requires workflow setup |
| Annotations | Manual drawing | Auto-drawn |
| FPS Control | Frame skip | MAX_FPS throttle |

## Workflow Setup on Roboflow

1. Log in to Roboflow
2. Go to your workspace
3. Create or select a workflow
4. Note the **Workflow ID** (e.g., `custom-workflow-3`)
5. Add it to `.env` as `ROBOFLOW_WORKFLOW_ID`

## Troubleshooting

### "Failed to start detection"
- Check API key is correct
- Verify workspace name matches your Roboflow account
- Ensure workflow ID exists

### "No frames appearing"
- Check camera source is accessible
- Try different camera index (0, 1, 2...)
- Verify webcam permissions in Windows

### "Detection too slow"
- Reduce MAX_FPS in .env (try 5 or 8)
- Lower video resolution
- Check internet connection (for cloud API)

## Code Structure

```
app/
├── utils/
│   ├── detector.py           # Original detector
│   └── workflow_detector.py  # NEW: Workflow detector
├── routes/
│   ├── api.py               # Original API routes
│   └── workflow_api.py      # NEW: Workflow API routes
└── templates/
    ├── dashboard.html        # Original dashboard
    └── workflow_dashboard.html  # NEW: Workflow dashboard
```

## Next Steps

1. **Test the workflow detection** at `/workflow`
2. **Compare performance** between standard and workflow modes
3. **Adjust MAX_FPS** for optimal performance
4. **Configure detection classes** for your use case
5. **Set up email alerts** for detected events

## Support

For issues with:
- **InferencePipeline**: Check Roboflow documentation
- **Workflow configuration**: Visit Roboflow workspace settings
- **API errors**: Verify API key and workspace access
