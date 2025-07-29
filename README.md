# AI-Powered Pothole Detection with Landing AI and NVIDIA Jetson

Real-time pothole detection system using Landing AI's computer vision platform integrated with NVIDIA Jetson edge computing and GPS tracking for municipal infrastructure monitoring.

## 🎯 Features

- **Real-time pothole detection** using Landing AI's trained computer vision models
- **Precise GPS coordinate logging** with multiple connection methods (GPSD, Serial, Mock)
- **Live camera feed** with detection overlays and system status
- **Automated data management** with timestamped images and structured JSON logs
- **Robust error handling** with retry logic and network resilience
- **Configurable monitoring** with adjustable capture intervals and confidence thresholds
- **Multiple deployment modes** for testing camera, GPS, and full system operation

## 🛠️ Hardware Requirements

### Core Platform
- **Seeed Studio reComputer J40** with NVIDIA Jetson Orin NX 8GB
- **reComputer J401 carrier board**
- **128GB NVMe SSD** (included)
- **Aluminum heatsink with cooling fan** (included)
- **12V/5A power adapter** (included)

### Peripherals
- **USB Camera**: Logitech C920 HD Pro Webcam (recommended) or compatible USB camera
- **GPS Module**: u-blox NEO-8M GPS receiver with USB interface
- **External GPS Antenna** (optional, for improved signal reception)
- **USB Hub** (if connecting multiple devices)

### Optional Accessories
- **Vehicle mount** for mobile deployment
- **Weatherproof enclosure** for outdoor installations
- **12V vehicle power adapter** for automotive deployment

## 📋 Software Dependencies

### System Requirements
- **JetPack 4.6.1** (includes Ubuntu 18.04 LTS, CUDA 10.2, cuDNN 8.2)
- **Python 3.6.9** (pre-installed with JetPack)
- **OpenCV 4.1.1** with CUDA support (pre-installed with JetPack)

### Python Package Dependencies

```bash
# Core Dependencies
pip3 install landingai==0.3.7
pip3 install opencv-python==4.8.1.78

# GPS and Serial Communication
pip3 install gpsd-py3==0.3.0
pip3 install pyserial==3.5
pip3 install pynmea2==1.19.0

# Data Processing and Utilities
pip3 install numpy>=1.21.0
pip3 install python-dotenv==1.0.0

# Development and Testing (Optional)
pip3 install matplotlib==3.5.3
pip3 install Pillow>=8.3.0
```

### System Package Dependencies

```bash
# GPS Daemon and Clients
sudo apt update
sudo apt install -y gpsd gpsd-clients python3-gps

# USB and Serial Support
sudo apt install -y python3-serial

# Development Tools (Optional)
sudo apt install -y python3-pip python3-venv git

# Camera Utilities
sudo apt install -y v4l-utils

# Network Tools
sudo apt install -y curl wget
```

## 🚀 Complete Installation Guide

### Step 1: System Setup and Basic Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python pip if not already installed
sudo apt install python3-pip -y

# Install OpenCV for display (if not already installed)
sudo apt install python3-opencv -y

# Install Landing AI Python library
pip3 install landingai

# Install additional dependencies
pip3 install numpy opencv-python

# Upgrade to latest versions
pip3 install --upgrade landingai opencv-python numpy

# Enable maximum performance mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Verify CUDA installation
nvcc --version

# Check GPU status
tegrastats

# Verify OpenCV with CUDA support
python3 -c "import cv2; print(f'OpenCV Version: {cv2.__version__}')"
python3 -c "import cv2; print(f'CUDA Devices: {cv2.cuda.getCudaEnabledDeviceCount()}')"
```

### Step 2: Project Directory Setup

```bash
# Create project directory
mkdir ~/pothole_detection
cd ~/pothole_detection

# Create the Python file
nano TEJAS_pothole_detector.py
```

### Step 3: Add the Main Application Code

Copy the complete `TEJAS_pothole_detector.py` code into the file you created in Step 2. The main application file contains:

- GPS tracking with multiple connection methods
- OpenCV camera interface with live display
- Landing AI integration for pothole detection
- Automated data logging and image capture
- Real-time visualization with detection overlays
- Comprehensive error handling and retry logic

### Step 4: Make Script Executable and Set Permissions

```bash
# Make the script executable
chmod +x TEJAS_pothole_detector.py

# Set up additional permissions for hardware access
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/video* 2>/dev/null || true
sudo chmod 666 /dev/ttyUSB* 2>/dev/null || true
sudo chmod 666 /dev/ttyACM* 2>/dev/null || true
```

### Step 5: Install Complete Dependencies

```bash
# Install from requirements file (if you have it)
pip install -r requirements.txt

# Or install all dependencies individually:
pip3 install landingai gpsd-py3 pyserial pynmea2 numpy python-dotenv matplotlib Pillow

# Install GPS system packages
sudo apt install -y gpsd gpsd-clients python3-gps python3-serial

# Install additional utilities
sudo apt install -y v4l-utils git curl wget
```

### Step 6: Configure Environment and Run

```bash
# Create environment file for API credentials
nano .env

# Add your Landing AI credentials to .env file:
# LANDING_AI_ENDPOINT_ID=your-endpoint-id-here
# LANDING_AI_API_KEY=land_sk_your-api-key-here

# Run the application
python3 TEJAS_pothole_detector.py
```

### Step 7: Verify Output Structure

After running the application, it will automatically create the following directory structure:

```
~/pothole_detection/
├── TEJAS_pothole_detector.py    # Main application
├── .env                         # Your API credentials
├── pothole_detections/          # Generated during runtime
│   ├── screenshots/             # Saved detection images
│   │   ├── pothole_20241128_143022_456.jpg
│   │   └── pothole_20241128_143156_789.jpg
│   └── logs/                    # Detection data and logs
│       ├── detection_log_20241128.log
│       ├── pothole_20241128_143022_456_data.json
│       └── pothole_20241128_143156_789_data.json
```

### Step 8: System Service Configuration

```bash
# Configure GPSD for automatic GPS detection
sudo nano /etc/default/gpsd

# Add these lines:
# DEVICES="/dev/ttyUSB0 /dev/ttyACM0"
# GPSD_OPTIONS="-n"
# START_DAEMON="true"

# Enable and start GPSD service
sudo systemctl enable gpsd
sudo systemctl start gpsd

# Test GPS functionality
cgps  # Press Ctrl+C to exit
```

### Step 9: Camera Setup and Testing

```bash
# List available video devices
ls /dev/video*

# Test camera capabilities
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --list-formats-ext

# Quick camera test
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    print('Camera working properly')
    cv2.imwrite('test_capture.jpg', frame)
else:
    print('Camera not detected')
cap.release()
"
```

### Step 10: Landing AI Configuration

```bash
# Create environment file for API credentials
nano .env

# Add your Landing AI credentials:
# LANDING_AI_ENDPOINT_ID=your-endpoint-id-here
# LANDING_AI_API_KEY=land_sk_your-api-key-here

# Update the Python script to use environment variables
# (See Security Configuration section below)
```

### Step 11: Hardware Connections

#### GPS Module Connection:
- **VCC**: Connect to 3.3V or 5V pin on J401 carrier board
- **GND**: Connect to Ground pin
- **TX**: Connect to UART RX pin (GPIO 15)
- **RX**: Connect to UART TX pin (GPIO 14)

#### Camera Connection:
- Connect USB camera to any USB 3.0 port on reComputer J401

### Step 12: Final System Reboot

```bash
# Reboot to apply all group changes and permissions
sudo reboot
```

After reboot, your system is ready to run the pothole detection application!

## 🔧 Configuration

### Environment Variables (.env file)
```bash
# Landing AI Configuration
LANDING_AI_ENDPOINT_ID=your-endpoint-id-here
LANDING_AI_API_KEY=land_sk_your-api-key-here

# System Configuration
CAMERA_ID=0
CAPTURE_INTERVAL=2.0
CONFIDENCE_THRESHOLD=0.5
GPS_METHOD=auto
SHOW_CAMERA=true
```

### Script Configuration Variables
```python
# Camera Settings
CAMERA_ID = 0                    # Primary camera (usually 0)
CAPTURE_INTERVAL = 2.0           # Seconds between AI analysis
CONFIDENCE_THRESHOLD = 0.5       # Minimum detection confidence (0.0-1.0)
SHOW_CAMERA = True              # Display live camera feed

# GPS Configuration
GPS_METHOD = "auto"             # "gpsd", "serial", "mock", or "auto"
GPS_SERIAL_PORT = "/dev/ttyUSB0" # For USB GPS dongles
GPS_BAUDRATE = 9600             # Standard GPS communication rate
```

## 🚀 Quick Start

### Method 1: Direct Execution
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/pothole-detection-jetson.git
cd pothole-detection-jetson

# Install dependencies
pip install -r requirements.txt

# Configure Landing AI credentials
cp .env.example .env
nano .env  # Add your API credentials

# Run the application
python3 TEJAS_pothole_detector.py
```

### Method 2: Step-by-Step Testing
```bash
# Test individual components first
python3 TEJAS_pothole_detector.py
# Choose option 2: Test Camera Only
# Choose option 3: Test GPS Only
# Choose option 1: Start Detection with GPS
```

## 📁 Project Structure

```
pothole-detection-jetson/
├── TEJAS_pothole_detector.py   # Main application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your API credentials (not in git)
├── .gitignore                # Git ignore file
├── README.md                  # This file
├── LICENSE                    # Project license
├── docs/
│   ├── setup-guide.md         # Detailed setup instructions
│   ├── troubleshooting.md     # Common issues and solutions
│   └── api-reference.md       # Code documentation
├── examples/
│   ├── sample_detection.json  # Example detection output
│   └── sample_config.py       # Example configuration
└── pothole_detections/        # Generated during runtime
    ├── screenshots/           # Detection images
    └── logs/                 # JSON data and log files
```

## 🔍 Usage Examples

### Basic Operation
```bash
# Start with default settings
python3 TEJAS_pothole_detector.py

# Select option 1: Start Detection with GPS
# Press 'q' in camera window to stop
# Use Ctrl+C in terminal for emergency stop
```

### Testing Individual Components
```bash
# Test camera only (no GPS or AI)
python3 TEJAS_pothole_detector.py
# Select option 2

# Test GPS only (no camera or AI)
python3 TEJAS_pothole_detector.py
# Select option 3
```

### Custom Configuration
```python
# Modify configuration in script or environment file
CAPTURE_INTERVAL = 5.0      # Analyze every 5 seconds
CONFIDENCE_THRESHOLD = 0.7  # Higher confidence requirement
GPS_METHOD = "serial"       # Force serial GPS connection
```

## 📊 Output Data Format

### Detection Image Files
- **Location**: `pothole_detections/screenshots/`
- **Format**: `pothole_YYYYMMDD_HHMMSS_mmm.jpg`
- **Content**: High-resolution image with detected pothole

### Detection Data Files
- **Location**: `pothole_detections/logs/`
- **Format**: `pothole_YYYYMMDD_HHMMSS_mmm_data.json`
- **Content**: Structured detection metadata

```json
{
  "timestamp": "20241128_143022_456",
  "analysis_id": 47,
  "image_file": "pothole_20241128_143022_456.jpg",
  "gps_location": {
    "latitude": 33.684673,
    "longitude": -117.826543,
    "altitude": 45.2,
    "satellites": 8,
    "fix_quality": 1
  },
  "detections": [
    {
      "confidence": 0.87,
      "label": "pothole",
      "bbox": {
        "x1": 245, "y1": 156,
        "x2": 398, "y2": 289
      }
    }
  ],
  "total_detections": 1,
  "camera_settings": {
    "width": 640,
    "height": 480,
    "camera_id": 0
  }
}
```

### Daily Log Files
- **Location**: `pothole_detections/logs/`
- **Format**: `detection_log_YYYYMMDD.log`
- **Content**: Chronological session events and summaries

## ⚠️ Troubleshooting

### Common Issues and Solutions

#### Camera Not Detected
```bash
# Check camera connection
lsusb | grep -i camera

# List video devices
ls -la /dev/video*

# Test camera access
v4l2-ctl --list-devices

# Fix permissions
sudo chmod 666 /dev/video0
```

#### GPS Not Working
```bash
# Check GPS device detection
dmesg | grep -i gps
lsusb | grep -i gps

# Test GPSD service
sudo systemctl status gpsd
sudo gpsd -D 5 -N -n /dev/ttyUSB0

# Manual GPS testing
cat /dev/ttyUSB0
```

#### Landing AI Connection Issues
```bash
# Test internet connectivity
ping landing.ai

# Verify API credentials
echo $LANDING_AI_API_KEY

# Check Landing AI service status
curl -H "Authorization: Bearer $LANDING_AI_API_KEY" https://api.landing.ai/v1/status
```

#### Performance Issues
```bash
# Monitor system resources
htop
tegrastats

# Check thermal throttling
cat /sys/devices/virtual/thermal/thermal_zone*/temp

# Ensure maximum performance
sudo nvpmodel -m 0
sudo jetson_clocks
```

## 🔒 Security Configuration

### API Key Protection
```python
# Use environment variables instead of hardcoded keys
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT_ID = os.getenv("LANDING_AI_ENDPOINT_ID")
API_KEY = os.getenv("LANDING_AI_API_KEY")

# Validate credentials before use
if not ENDPOINT_ID or not API_KEY:
    raise ValueError("Landing AI credentials not configured")
```

### File Permissions
```bash
# Secure environment file
chmod 600 .env

# Secure log directory
chmod 755 pothole_detections/
chmod 644 pothole_detections/logs/*
```

## 📖 Documentation

- **Setup Guide**: `docs/setup-guide.md` - Detailed installation instructions
- **API Reference**: `docs/api-reference.md` - Code documentation
- **Troubleshooting**: `docs/troubleshooting.md` - Common issues and solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Landing AI** for providing the computer vision platform
- **NVIDIA** for Jetson edge computing hardware
- **Seeed Studio** for the reComputer J40 development platform
- **OpenCV** community for computer vision libraries

## 📧 Contact

**Author**: Tejas Patel
**Project Link**: [https://github.com/YOUR_USERNAME/pothole-detection-jetson](https://github.com/YOUR_USERNAME/pothole-detection-jetson)

---

*For detailed technical documentation and advanced configuration options, see the `docs/` directory.*
