# Enhanced Workflow Dashboard - User Guide

## 🎨 New Features

### Professional UI/UX
- **Light/Dark Mode Toggle**: Click the moon/sun icon in the header
- **Real-time Stats**: 4 stat cards showing Frames, Detections, Alerts, Camera Status
- **Live Uptime Counter**: Shows system running time in HH:MM:SS format
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Color Scheme
- **Light Mode**: Clean white background with purple gradient
- **Dark Mode**: Dark theme optimized for night viewing
- **Status Colors**:
  - Green: Success/Active
  - Red: Error/Inactive
  - Yellow: Warning
  - Blue: Info

### Camera Management

#### Multiple Input Options
1. **Webcam Tab**: Select from detected webcams (0, 1, 2, 3)
2. **RTSP Stream Tab**: Enter IP camera RTSP URL
3. **Video File Tab**: Upload or specify video file path

#### Live Video Display
- Large video feed with real-time detections
- Overlay badges showing status and frame count
- Start/Stop controls with visual feedback
- FPS counter for performance monitoring

### Detection Results
- **Recent Detections Panel**: Right sidebar showing latest detections
- **Color-coded confidence**:
  - Green border: High confidence (>70%)
  - Yellow border: Medium confidence (40-70%)
  - Red border: Low confidence (<40%)
- **Real-time updates**: Auto-refreshes every 3 seconds

### System Status
- **Status Grid**: Shows Detection status, Video source, Frame rate, Frame availability
- **Error Display**: Red error banner when issues occur
- **Configuration Panel**: Shows Roboflow API settings

### Error Handling
- Toast notifications for all actions
- Detailed error messages in status section
- Graceful video feed error recovery
- Form validation before submission

## 🎯 Usage Instructions

### Starting Detection

1. **Select Camera Source**:
   - Click the appropriate tab (Webcam/RTSP/File)
   - Enter or select your video source
   
2. **Start Detection**:
   - Click the green "Start Detection" button
   - Wait for confirmation toast
   - Watch stats update in real-time

3. **Monitor Results**:
   - View live annotated video feed
   - Check detection panel for identified objects
   - Monitor FPS and frame count
   - Track system uptime

### Stopping Detection

- Click the red "Stop Detection" button
- System will gracefully shut down the pipeline
- All stats will be preserved

### Theme Switching

- Click the moon/sun icon in header
- Theme preference is saved in browser
- All colors adapt automatically

## 🔧 Technical Details

### Performance Monitoring
- **FPS Display**: Real-time frames per second calculation
- **Frame Counter**: Total processed frames since start
- **Uptime**: Time elapsed since detection started
- **Detection Count**: Number of objects detected

### Status Indicators
- **Camera Status**: Active (green) / Inactive (red)
- **Running Badge**: Visual indicator on video feed
- **Frame Status**: Yes/No for frame availability
- **Source Display**: Shows current video source

### Auto-refresh Intervals
- Status updates: Every 2 seconds
- Predictions: Every 3 seconds
- Uptime: Every 1 second

## 🎓 Lecturer-Friendly Features

### Professional Appearance
- Clean, academic color scheme
- Clear data visualization
- Professional typography
- Consistent spacing and alignment

### Easy Demonstration
- Large, clear video display
- Real-time performance metrics
- Color-coded confidence levels
- Intuitive controls

### Accessibility
- High contrast in both themes
- Clear status indicators
- Readable font sizes
- Logical layout structure

## 📊 Stats Panel Breakdown

### Frames Processed
- Total number of video frames analyzed
- Updates in real-time
- Useful for performance tracking

### Total Detections
- Count of detected objects
- Based on latest predictions
- Resets when new predictions arrive

### Active Alerts
- Number of current alerts/warnings
- Future integration with alert system
- Currently displays detection count

### Camera Status
- Shows "Active" when running
- Shows "Inactive" when stopped
- Color-coded (green/red)

## 🛠️ Troubleshooting

### Video Not Showing
1. Check camera permissions in browser
2. Verify video source is correct
3. Look for error messages in status section
4. Try different camera index (0, 1, 2...)

### Low FPS
1. Reduce MAX_FPS in .env (try 15-20)
2. Check internet connection
3. Close other applications
4. Try lower resolution camera

### Detections Not Appearing
1. Verify Roboflow API key is valid
2. Check workflow ID is correct
3. Ensure detection classes match workflow
3. Review error messages in status panel

### Theme Not Saving
1. Clear browser cache
2. Enable local storage in browser
3. Try different browser

## 🌟 Best Practices

### For Demonstrations
1. Start in light mode for projector visibility
2. Use webcam for live demonstrations
3. Pre-load configuration before presentation
4. Test detection before showing to audience

### For Development
1. Use dark mode for reduced eye strain
2. Monitor FPS for performance issues
3. Check error panel regularly
4. Use RTSP for production cameras

### For Testing
1. Start with video file for controlled testing
2. Monitor frame count for consistency
3. Verify detection accuracy in results panel
4. Test both themes for UI consistency

## 📝 Keyboard Shortcuts

- No keyboard shortcuts currently implemented
- Future update may include:
  - Space: Start/Stop detection
  - T: Toggle theme
  - R: Refresh predictions
  - F: Fullscreen video

## 🔄 Future Enhancements

Potential additions:
- Export detection logs
- Screenshot capture
- Recording functionality
- Multiple camera views
- Detection history graph
- Alert sound notifications
- Email alert integration
