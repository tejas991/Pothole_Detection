# AI-Powered Pothole Detection with Landing AI and NVIDIA Jetson

Real-time pothole detection system using Landing AI's computer vision platform integrated with NVIDIA Jetson edge computing and GPS tracking for municipal infrastructure monitoring.

## Features

- **Real-time pothole detection** using Landing AI's trained computer vision models
- **Precise GPS coordinate logging** with multiple connection methods (GPSD/Serial/Mock)
- **Live camera feed** with detection overlays and system status
- **Automated data management** with timestamped images and structured JSON logs
- **Error handling** with retry logic and network resilience
- **Configurable monitoring** with adjustable capture intervals and confidence thresholds
- **Multiple deployment modes** for 1)Testing camera, 2)Testing GPS 3)Full system operation

## Hardware Requirements

### Core Platform ( I used )
- **Seeed Studio reComputer J40** with NVIDIA Jetson Orin NX 8GB
- **reComputer J401 carrier board**
- **128GB NVMe SSD** (included)
- **Aluminum heatsink with cooling fan** (included)
- **12V/5A power adapter** (included)

### Peripherals
- **USB Camera**: 4K Webcam 
- **GPS Module**: u-blox NEO-8M GPS receiver with USB interface
- **USB Hub** (if connecting multiple devices)

### Optional Accessories
- **Vehicle mount** for mobile deployment
- **Weatherproof enclosure** for outdoor installations
- **12V vehicle power adapter** for automotive deployment

## Software Dependencies

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

# Development Tools 
sudo apt install -y python3-pip python3-venv git

# Camera Utilities
sudo apt install -y v4l-utils

# Network Tools
sudo apt install -y curl wget
```

## Complete Installation Guide

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


## Contact

**Author**: Tejas Bharadwaj
**Project Link**: [https://github.com/tejas991/pothole-detection-jetson](https://github.com/YOUR_USERNAME/pothole-detection-jetson)

---

*For detailed technical documentation and advanced configuration options, see the `docs/` directory.*
