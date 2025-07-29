# Detailed Setup Guide

## Prerequisites

- Seeed Studio reComputer J40 with NVIDIA Jetson Orin NX 8GB
- JetPack 4.6.1 installed
- USB camera (Logitech C920 recommended)
- GPS module (u-blox NEO-8M recommended)
- Internet connection for Landing AI API

## Hardware Setup

### 1. reComputer J40 Assembly
- Ensure 128GB NVMe SSD is properly installed
- Verify cooling fan is connected and operational
- Connect 12V/5A power adapter

### 2. Camera Connection
- Connect USB camera to any USB 3.0 port on J401 carrier board
- Verify detection: `lsusb | grep -i camera`

### 3. GPS Module Connection
```
GPS Module    →    reComputer J401
VCC           →    5V Pin
GND           →    GND Pin  
TX            →    UART RX (GPIO 15)
RX            →    UART TX (GPIO 14)
```

## Software Installation

### Step 1: System Setup and Dependencies

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
```

### Step 2: Project Directory and File Setup

```bash
# Create project directory
mkdir ~/pothole_detection
cd ~/pothole_detection

# Create the Python file
nano TEJAS_pothole_detector.py
```

### Step 3: Add Application Code

Copy the complete `TEJAS_pothole_detector.py` code into the file you created in Step 2. You can get this code from the GitHub repository or copy it from the main application file.

The main application contains:
- GPS tracking with multiple connection methods
- OpenCV camera interface with live display
- Landing AI integration for pothole detection
- Automated data logging and image capture
- Real-time visualization with detection overlays
- Comprehensive error handling and retry logic

### Step 4: Make Script Executable

```bash
# Make the script executable
chmod +x TEJAS_pothole_detector.py

# Install additional system dependencies for GPS
sudo apt install -y gpsd gpsd-clients python3-gps python3-serial

# Install remaining Python packages
pip3 install gpsd-py3 pyserial pynmea2 python-dotenv matplotlib Pillow

# Set up permissions for hardware access
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/video* 2>/dev/null || true
sudo chmod 666 /dev/ttyUSB* 2>/dev/null || true
sudo chmod 666 /dev/ttyACM* 2>/dev/null || true
```

### Step 5: Configure and Run

```bash
# Create environment file for API credentials
nano .env

# Add your Landing AI credentials to .env file:
# LANDING_AI_ENDPOINT_ID=your-endpoint-id-here
# LANDING_AI_API_KEY=land_sk_your-api-key-here

# Configure GPSD for GPS (if using GPS)
sudo nano /etc/default/gpsd
# Add: DEVICES="/dev/ttyUSB0 /dev/ttyACM0"
# Add: GPSD_OPTIONS="-n"
# Add: START_DAEMON="true"

# Enable and start GPSD service
sudo systemctl enable gpsd
sudo systemctl start gpsd

# Run the application
python3 TEJAS_pothole_detector.py
```

## Testing and Verification

### 1. Test Camera Only
```bash
python3 TEJAS_pothole_detector.py
# Select option 2: Test Camera Only
```

### 2. Test GPS Only
```bash
python3 TEJAS_pothole_detector.py
# Select option 3: Test GPS Only
```

### 3. Full System Test
```bash
python3 TEJAS_pothole_detector.py
# Select option 1: Start Detection with GPS
```

## Expected Output Structure

After running the application, it will create:

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

## Landing AI Configuration

Get your Landing AI credentials from: https://app.landing.ai/

1. Create an account on Landing AI platform
2. Upload your pothole dataset (if training custom model)
3. Train your model or use existing pothole detection model
4. Get your Endpoint ID and API Key
5. Add credentials to `.env` file

## System Optimization

### Jetson Performance
```bash
# Enable maximum performance mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Monitor performance
tegrastats

# Verify CUDA support
python3 -c "import cv2; print(f'OpenCV Version: {cv2.__version__}')"
python3 -c "import cv2; print(f'CUDA Devices: {cv2.cuda.getCudaEnabledDeviceCount()}')"
```

### Final System Reboot
```bash
# Reboot to apply all permission changes
sudo reboot
```

After reboot, your pothole detection system is ready to use!

## Troubleshooting

### Camera Issues
- Check USB connections: `lsusb | grep -i camera`
- Verify permissions: `sudo chmod 666 /dev/video0`
- Test with: `v4l2-ctl --list-devices`

### GPS Issues
- Check device: `lsusb | grep -i gps`
- Test GPSD: `sudo systemctl status gpsd`
- Manual test: `cat /dev/ttyUSB0`

### Landing AI Issues
- Verify internet connection: `ping landing.ai`
- Check API credentials in .env file
- Test API connectivity with sample request

### Performance Issues
- Monitor temperatures: `tegrastats`
- Ensure cooling fan is operational
- Check for thermal throttling

For comprehensive troubleshooting, see the main README.md troubleshooting section.
