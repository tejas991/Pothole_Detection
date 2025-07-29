#!/bin/bash
# Complete system setup script for NVIDIA Jetson

echo "🚀 Setting up Pothole Detection System on Jetson..."

# System optimization
echo "⚡ Optimizing Jetson performance..."
sudo nvpmodel -m 0
sudo jetson_clocks

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
echo "📦 Installing system packages..."
sudo apt install -y gpsd gpsd-clients python3-gps python3-serial python3-pip python3-venv git v4l-utils curl wget python3-opencv

# Install Landing AI and core dependencies
echo "🤖 Installing Landing AI and dependencies..."
pip3 install landingai
pip3 install numpy opencv-python
pip3 install --upgrade landingai opencv-python numpy

# Install additional Python packages
echo "🐍 Installing additional Python packages..."
pip3 install gpsd-py3 pyserial pynmea2 python-dotenv matplotlib Pillow

# Configure GPSD
echo "📍 Configuring GPS services..."
sudo systemctl enable gpsd
sudo systemctl start gpsd

# Set permissions
echo "🔐 Setting up permissions..."
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/video* 2>/dev/null || true
sudo chmod 666 /dev/ttyUSB* 2>/dev/null || true
sudo chmod 666 /dev/ttyACM* 2>/dev/null || true

# Create project directory structure
echo "📁 Creating project directories..."
mkdir -p ~/pothole_detection
cd ~/pothole_detection

# Copy environment template
if [ -f ".env.example" ]; then
    cp .env.example .env
    echo "📝 Created .env file from template"
    echo "⚠️  Please edit .env file with your Landing AI credentials"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Landing AI credentials:"
echo "   nano .env"
echo "2. Reboot the system to apply permission changes:"
echo "   sudo reboot"
echo "3. After reboot, run the application:"
echo "   python3 TEJAS_pothole_detector.py"
echo ""
echo "To test individual components:"
echo "- Camera only: python3 TEJAS_pothole_detector.py (option 2)"
echo "- GPS only: python3 TEJAS_pothole_detector.py (option 3)"
