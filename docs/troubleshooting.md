# Troubleshooting Guide

## Common Issues and Solutions

### Camera Problems

#### Camera Not Detected
```bash
# Check if camera is connected
lsusb | grep -i camera

# List video devices
ls -la /dev/video*

# Test camera capabilities
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --list-formats-ext
```

**Solutions:**
- Ensure USB cable is securely connected
- Try different USB port (use USB 3.0 if available)
- Check camera compatibility with V4L2
- Set proper permissions: `sudo chmod 666 /dev/video0`

#### Poor Image Quality
```bash
# Adjust camera settings
v4l2-ctl -d /dev/video0 -c exposure_auto=1
v4l2-ctl -d /dev/video0 -c exposure_absolute=300
v4l2-ctl -d /dev/video0 -c brightness=128
```

#### Camera Permission Denied
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Set device permissions
sudo chmod 666 /dev/video0

# Create udev rule for persistent permissions
echo 'SUBSYSTEM=="video4linux", GROUP="video", MODE="0664"' | sudo tee /etc/udev/rules.d/99-camera.rules
sudo udevadm control --reload-rules
```

### GPS Issues

#### GPS Module Not Detected
```bash
# Check USB connection
lsusb | grep -i gps
dmesg | grep -i gps

# Check serial devices
ls -la /dev/ttyUSB*
ls -la /dev/ttyACM*
```

**Solutions:**
- Verify physical connections (VCC, GND, TX, RX)
- Check if GPS module has power LED indicator
- Try different USB port or cable
- Install GPS drivers if needed

#### GPSD Service Issues
```bash
# Check GPSD status
sudo systemctl status gpsd

# Restart GPSD service
sudo systemctl restart gpsd

# Manual GPSD debugging
sudo gpsd -D 5 -N -n /dev/ttyUSB0

# Test GPSD connection
cgps
gpsmon
```

**Solutions:**
- Edit `/etc/default/gpsd` configuration
- Ensure correct device path in DEVICES setting
- Check if gpsd is binding to correct port
- Kill existing gpsd processes: `sudo killall gpsd`

#### No GPS Fix
```bash
# Test raw GPS data
cat /dev/ttyUSB0

# Check satellite visibility
gpsmon

# Verify antenna connection
# Move to open area for better signal
```

**Solutions:**
- Move to outdoor location with clear sky view
- Check GPS antenna connection
- Wait longer for initial fix (cold start can take 5-15 minutes)
- Verify GPS module has valid firmware

### Landing AI Connection Issues

#### API Authentication Errors
```bash
# Verify credentials
echo $LANDING_AI_ENDPOINT_ID
echo $LANDING_AI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $LANDING_AI_API_KEY" https://api.landing.ai/v1/status
```

**Solutions:**
- Check API key format (should start with `land_sk_`)
- Verify endpoint ID is correct
- Ensure .env file is in correct directory
- Check for trailing spaces in credentials

#### Network Connectivity Issues
```bash
# Test internet connection
ping google.com
ping landing.ai

# Check firewall settings
sudo ufw status

# Test with curl
curl -v https://api.landing.ai
```

**Solutions:**
- Verify internet connection is stable
- Check corporate firewall settings
- Try different network if available
- Ensure ports 80 and 443 are open

#### Rate Limiting
**Error:** `429 Too Many Requests`

**Solutions:**
- Increase `CAPTURE_INTERVAL` to reduce API calls
- Implement exponential backoff (already in code)
- Check Landing AI account usage limits
- Contact Landing AI support for rate limit increase

### Performance Issues

#### High CPU/GPU Usage
```bash
# Monitor system resources
htop
tegrastats

# Check thermal status
cat /sys/devices/virtual/thermal/thermal_zone*/temp
```

**Solutions:**
- Ensure cooling fan is working
- Enable maximum performance mode: `sudo nvpmodel -m 0`
- Lower camera resolution if needed
- Increase capture interval to reduce processing load

#### Memory Issues
```bash
# Check memory usage
free -h
sudo dmesg | grep -i memory

# Clear cache if needed
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

**Solutions:**
- Close unnecessary applications
- Reduce image retention (delete old detection images)
- Consider using swap file if needed
- Monitor for memory leaks in application

#### Thermal Throttling
```bash
# Monitor temperatures
watch -n 1 cat /sys/devices/virtual/thermal/thermal_zone*/temp

# Check throttling status
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq
```

**Solutions:**
- Ensure adequate cooling (fan operational)
- Reduce ambient temperature
- Lower performance mode if overheating persists
- Add external cooling if needed

### Software Issues

#### Python Package Conflicts
```bash
# Create clean virtual environment
python3 -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

#### OpenCV CUDA Issues
```bash
# Verify CUDA installation
nvcc --version
nvidia-smi

# Test OpenCV CUDA support
python3 -c "import cv2; print(cv2.cuda.getCudaEnabledDeviceCount())"
```

**Solutions:**
- Reinstall JetPack for proper CUDA integration
- Use OpenCV version compatible with JetPack
- Verify CUDA paths in environment

#### Landing AI SDK Issues
```bash
# Update to latest version
pip install --upgrade landingai

# Check version compatibility
pip list | grep landing
```

### File System Issues

#### Disk Space Full
```bash
# Check disk usage
df -h
du -sh pothole_detections/

# Clean up old files
find pothole_detections/ -name "*.jpg" -mtime +7 -delete
find pothole_detections/ -name "*.json" -mtime +7 -delete
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER ~/pothole_detection
chmod -R 755 ~/pothole_detection

# Fix device permissions
sudo chmod 666 /dev/video*
sudo chmod 666 /dev/ttyUSB*
```

## Error Messages and Solutions

### "Failed to read from camera"
- Camera disconnected or failed
- Check USB connection and power
- Restart application

### "GPS read error"
- GPS module communication issue
- Check serial connection
- Verify GPS module power

### "Landing AI analysis failed"
- Network connectivity issue
- API rate limiting
- Invalid credentials

### "Cannot open camera [ID]"
- Camera not detected by system
- Wrong camera ID (try 0, 1, 2)
- Permission denied

## Getting Additional Help

### Log Analysis
- Check daily log files in `pothole_detections/logs/`
- Look for error patterns in system logs: `dmesg`
- Monitor application output for specific error messages

### System Information
```bash
# Jetson info
cat /etc/nv_tegra_release

# Hardware info
lshw -short
lsusb
lspci

# Software versions
python3 --version
pip list
```

### Contact Information
- GitHub Issues: Report bugs and request features
- Landing AI Support: API-related issues
- NVIDIA Developer Forums: Jetson-specific problems

## Preventive Measures

### Regular Maintenance
- Clean cooling fan monthly
- Update software dependencies quarterly
- Monitor disk space usage
- Backup important detection data

### Monitoring
- Set up system monitoring for temperature
- Monitor GPS signal quality
- Track API usage limits
- Log system performance metrics

### Best Practices
- Use stable power supply
- Protect from dust and moisture
- Regular system updates
- Proper cable management
