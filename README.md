# Smart Surveillance System

An intelligent surveillance system using Flask and Roboflow API for real-time object detection and security monitoring.

## Features

- 🎥 Real-time video surveillance from webcam or IP cameras
- 🤖 AI-powered object detection using Roboflow
- 🚨 Automatic alert generation and email notifications
- 📊 Event logging and management dashboard
- 👤 User authentication and authorization
- 📹 Video clip recording of detected events
- 🎛️ Configurable detection settings
- 📱 Responsive web interface

## Project Structure

```
code/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── event.py
│   ├── routes/               # Application routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── api.py
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── detector.py       # Roboflow detection logic
│   │   ├── camera.py         # Camera handling
│   │   ├── email_alerts.py   # Email notifications
│   │   └── video_utils.py    # Video processing utilities
│   ├── static/               # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/            # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── dashboard.html
│       ├── login.html
│       └── events.html
├── config/
│   └── config.py             # Configuration settings
├── tests/                    # Unit tests
├── logs/                     # Application logs
├── uploads/                  # Uploaded files
├── detected_events/          # Saved detection videos
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Example environment variables
├── .gitignore
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Webcam or IP camera
- Roboflow account and API key

### Setup Steps

1. **Clone or download the project**

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your:
   - Roboflow API key
   - Email credentials (for alerts)
   - Camera source
   - Other configuration settings

6. **Initialize the database**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

7. **Run the application**
   ```bash
   python run.py
   ```

8. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Roboflow Setup

1. Create an account at [Roboflow](https://roboflow.com/)
2. Create a new project for object detection
3. Train a model or use a pre-trained model
4. Get your API key from Account Settings
5. Add the API key and project details to your `.env` file

## Usage

### First Time Setup

1. Access the application at `http://localhost:5000`
2. Register a new admin account
3. Log in with your credentials
4. Configure camera settings in the dashboard
5. Set detection preferences (confidence threshold, classes to detect)
6. Start surveillance monitoring

### Daily Operations

- **Monitor Live Feed**: View real-time camera feeds with detection overlays
- **Review Events**: Check detected events in the events dashboard
- **Configure Alerts**: Set up email notifications for specific detections
- **Manage Cameras**: Add, remove, or configure camera sources
- **View Reports**: Access detection statistics and logs

## Configuration

Key configuration options in `.env`:

- `CONFIDENCE_THRESHOLD`: Minimum confidence score for detections (0.0-1.0)
- `DETECTION_CLASSES`: Comma-separated list of objects to detect
- `FRAME_SKIP`: Process every Nth frame (higher = faster, lower accuracy)
- `MAX_VIDEO_CLIP_DURATION`: Length of saved video clips (seconds)
- `RETENTION_DAYS`: How long to keep detection records

## Troubleshooting

### Camera not detected
- Check camera permissions
- Verify camera source in `.env` file
- Try different camera indices (0, 1, 2...)

### Roboflow API errors
- Verify API key is correct
- Check internet connection
- Ensure project name and version are correct

### Email alerts not working
- Verify SMTP settings
- For Gmail, enable "Less secure app access" or use App Password
- Check firewall settings

## API Endpoints

- `GET /` - Home page
- `GET /dashboard` - Main dashboard (authenticated)
- `GET /events` - View detection events (authenticated)
- `POST /api/start-detection` - Start surveillance
- `POST /api/stop-detection` - Stop surveillance
- `GET /api/video-feed` - Live video stream
- `GET /api/events` - Get events data (JSON)

## Testing

Run tests using:
```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Security Considerations

- Change the default `SECRET_KEY` in production
- Use strong passwords
- Enable HTTPS in production
- Regularly update dependencies
- Comply with privacy regulations (GDPR, etc.)
- Inform individuals about surveillance in monitored areas

## License

This project is for educational purposes. Use responsibly and in compliance with local laws.

## Support

For issues or questions:
- Check the documentation
- Review troubleshooting section
- Contact project maintainer

## Future Enhancements

- [ ] Mobile app integration
- [ ] Facial recognition (with privacy controls)
- [ ] Multi-site support
- [ ] Cloud storage integration
- [ ] Advanced analytics and reporting
- [ ] Behavioral pattern detection
- [ ] Integration with home automation systems

## Credits

Built with:
- Flask (Web framework)
- Roboflow (Object detection API)
- OpenCV (Computer vision)
- SQLAlchemy (Database ORM)
- SocketIO (Real-time communication)

---

**Note**: This system is designed for educational and research purposes. Ensure compliance with local surveillance and privacy laws before deployment.
"# examcheating" 
