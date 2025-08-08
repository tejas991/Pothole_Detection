TEJAS_pothole_detecor.py
"""
Jetson w/Camera --> Landing AI w/ GPS Location Tracking
Captures frames from camera, detects potholes, and logs GPS coordinates
"""

import time
import os
import cv2
import json
from datetime import datetime
from landingai.pipeline.frameset import Frame
from landingai.predict import Predictor

# GPS imports - install with: pip install gpsd-py3
try:
    import gpsd
    GPS_AVAILABLE = True
    print("✅ GPS module available")
except ImportError:
    GPS_AVAILABLE = False
    print("GPS module not available - install with: pip install gpsd-py3")

# Alternative GPS using serial (for USB GPS dongles)
try:
    import serial
    import pynmea2
    SERIAL_GPS_AVAILABLE = True
except ImportError:
    SERIAL_GPS_AVAILABLE = False

# YOUR LANDING AI CREDENTIALS 
ENDPOINT_ID = "your-endpoint-id-here"
API_KEY = "land_sk_your-api-key-here"

# CONFIGURATION
CAMERA_ID = 0           # Whichever camera works for you
CAPTURE_INTERVAL = 1.0  # Seconds between captures
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence to consider a detection
SHOW_CAMERA = True      # Show live camera feed

# GPS CONFIGURATION
GPS_METHOD = "auto"     # "gpsd", "serial", "mock", or "auto"
GPS_SERIAL_PORT = "/dev/ttyUSB0"  # For USB GPS dongles
GPS_BAUDRATE = 9600     # Standard GPS baud rate

class GPSTracker:
    """Handle GPS location tracking with multiple methods"""
    
    def __init__(self, method="auto"):
        self.method = method
        self.gps_connection = None
        self.serial_connection = None
        self.last_known_location = None
        self.mock_location = {
            "latitude": 39.6846,   # Irvine, CA (example, use gpa modeule for exact)
            "longitude": -127.8265,
            "altitude": 90.0,
            "speed": 0.0
        }
        
        self.initialize_gps()
    
    def initialize_gps(self):
        """Initialize GPS connection based on available methods"""
        
        if self.method == "auto":
            if self._try_gpsd():
                self.method = "gpsd"
                print("Using GPSD for GPS")
            elif self._try_serial_gps():
                self.method = "serial"
                print("Using Serial GPS")
            else:
                self.method = "mock"
                print("Using mock GPS coordinates (for testing)")
        
        elif self.method == "gpsd":
            if not self._try_gpsd():
                print("GPSD not available, falling back to mock")
                self.method = "mock"
        
        elif self.method == "serial":
            if not self._try_serial_gps():
                print("Serial GPS not available, falling back to mock")
                self.method = "mock"
        
        elif self.method == "mock":
            print("Using mock GPS coordinates")
    
    def _try_gpsd(self):
        """Try to connect to GPSD"""
        if not GPS_AVAILABLE:
            return False
        
        try:
            gpsd.connect()
            packet = gpsd.get_current()
            if packet.mode >= 2:  # At least 2D fix
                self.gps_connection = gpsd
                return True
        except Exception as e:
            print(f"GPSD connection failed: {e}")
        
        return False
    
    def _try_serial_gps(self):
        """Try to connect to serial GPS"""
        if not SERIAL_GPS_AVAILABLE:
            return False
        
        try:
            self.serial_connection = serial.Serial(GPS_SERIAL_PORT, GPS_BAUDRATE, timeout=1)
            return True
        except Exception as e:
            print(f"Serial GPS connection failed: {e}")
        
        return False
    
    def get_location(self):
        """Get current GPS location"""
        
        if self.method == "gpsd":
            return self._get_gpsd_location()
        elif self.method == "serial":
            return self._get_serial_location()
        elif self.method == "mock":
            return self._get_mock_location()
        else:
            return None
    
    def _get_gpsd_location(self):
        """Get location from GPSD"""
        try:
            packet = gpsd.get_current()
            if packet.mode >= 2:
                location = {
                    "latitude": packet.lat,
                    "longitude": packet.lon,
                    "altitude": packet.alt if packet.mode >= 3 else 0.0,
                    "speed": packet.hspeed,
                    "timestamp": datetime.now().isoformat(),
                    "fix_quality": packet.mode,
                    "satellites": packet.sats
                }
                self.last_known_location = location
                return location
        except Exception as e:
            print(f"GPS read error: {e}")
        
        return self.last_known_location
    
    def _get_serial_location(self):
        """Get location from serial GPS"""
        try:
            line = self.serial_connection.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA') or line.startswith('$GNGGA'):
                msg = pynmea2.parse(line)
                if msg.latitude and msg.longitude:
                    location = {
                        "latitude": float(msg.latitude),
                        "longitude": float(msg.longitude),
                        "altitude": float(msg.altitude) if msg.altitude else 0.0,
                        "speed": 0.0,  # Not available in GGA
                        "timestamp": datetime.now().isoformat(),
                        "fix_quality": int(msg.gps_qual),
                        "satellites": int(msg.num_sats)
                    }
                    self.last_known_location = location
                    return location
        except Exception as e:
            print(f"Serial GPS read error: {e}")
        
        return self.last_known_location
    
    def _get_mock_location(self):
        """Get mock location (for testing without GPS)"""
        # Simulate movement by slightly changing coordinates
        import random
        location = self.mock_location.copy()
        location["latitude"] += random.uniform(-0.0001, 0.0001)
        location["longitude"] += random.uniform(-0.0001, 0.0001)
        location["timestamp"] = datetime.now().isoformat()
        location["fix_quality"] = 1
        location["satellites"] = 8
        return location

def capture_with_opencv_and_gps():
    """Main function with GPS tracking"""
    
    print("Jetson Camera to Landing AI with GPS")
    print("=" * 45)
    
    # Check credentials
    if "your-endpoint" in ENDPOINT_ID or "your-api" in API_KEY:
        print("❌ Please update ENDPOINT_ID and API_KEY in the code")
        print("Get these from: https://app.landing.ai/")
        return
    
    # Initialize GPS
    gps_tracker = GPSTracker(GPS_METHOD)
    
    # Create output directories
    output_dir = "pothole_detections"
    screenshots_dir = os.path.join(output_dir, "screenshots")
    logs_dir = os.path.join(output_dir, "logs")
    
    for directory in [output_dir, screenshots_dir, logs_dir]:
        os.makedirs(directory, exist_ok=True)
    
    print(f"Saving data to: {output_dir}")
    print(f"  Images: {screenshots_dir}")
    print(f"  Logs: {logs_dir}")
    
    # Initialize Landing AI
    try:
        predictor = Predictor(
            endpoint_id=ENDPOINT_ID,
            api_key=API_KEY
        )
        print("✅ Connected to Landing AI")
    except Exception as e:
        print(f"❌ Failed to connect to Landing AI: {e}")
        return
    
    # Initialize camera
    print(f"🔍 Opening camera {CAMERA_ID}...")
    cap = cv2.VideoCapture(CAMERA_ID)
    
    if not cap.isOpened():
        print(f"❌ Cannot open camera {CAMERA_ID}")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print(f"✅ Camera {CAMERA_ID} opened successfully")
    print(f"Capturing every {CAPTURE_INTERVAL} seconds")
    print("Camera feed will be displayed with GPS info")
    print("Press 'q' in camera window or Ctrl+C to stop")
    
    # Create camera display window
    if SHOW_CAMERA:
        cv2.namedWindow('Pothole Detection with GPS', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Pothole Detection with GPS', 900, 700)
    
    frame_count = 0
    detection_count = 0
    last_capture_time = 0
    analysis_count = 0
    
    # Create daily log file
    daily_log_filename = f"detection_log_{datetime.now().strftime('%Y%m%d')}.log"
    daily_log_filepath = os.path.join(logs_dir, daily_log_filename)
    
    def log_to_daily_file(message):
        """Write message to daily log file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(daily_log_filepath, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    # Log session start
    log_to_daily_file(f"Session started - Camera {CAMERA_ID}, Interval {CAPTURE_INTERVAL}s")
    print(f"Daily log: {daily_log_filename}")
    
    try:
        while True:
            # Read frame from camera
            ret, opencv_frame = cap.read()
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            # Get current GPS location
            current_location = gps_tracker.get_location()
            
            # Show live camera feed with GPS overlay
            if SHOW_CAMERA:
                display_frame = opencv_frame.copy()
                
                # Add text overlays
                cv2.putText(display_frame, f"Frames: {frame_count} | Analyzed: {analysis_count} | Detections: {detection_count}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                next_analysis = max(0, CAPTURE_INTERVAL - (time.time() - last_capture_time))
                cv2.putText(display_frame, f"Next analysis in: {next_analysis:.1f}s", 
                           (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                
                # GPS information overlay
                if current_location:
                    gps_text = f"GPS: {current_location['latitude']:.6f}, {current_location['longitude']:.6f}"
                    cv2.putText(display_frame, gps_text, 
                               (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    
                    sat_text = f"Satellites: {current_location.get('satellites', 'N/A')} | Quality: {current_location.get('fix_quality', 'N/A')}"
                    cv2.putText(display_frame, sat_text, 
                               (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                else:
                    cv2.putText(display_frame, "GPS: No fix", 
                               (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
                cv2.putText(display_frame, "Press 'q' to quit", 
                           (10, display_frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.imshow('Pothole Detection with GPS', display_frame)
                
                # Check for quit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("User pressed 'q' to quit")
                    break
            
            frame_count += 1
            
            # Check if it's time to analyze
            current_time = time.time()
            if current_time - last_capture_time < CAPTURE_INTERVAL:
                continue
            
            last_capture_time = current_time
            analysis_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            
            print(f"Analysis {analysis_count} (Frame {frame_count}): {timestamp}")
            if current_location:
                print(f"   Location: {current_location['latitude']:.6f}, {current_location['longitude']:.6f}")
            
            try:
                # Save frame temporarily
                temp_filename = f"temp_frame_{timestamp}.jpg"
                temp_filepath = os.path.join(screenshots_dir, temp_filename)
                cv2.imwrite(temp_filepath, opencv_frame)
                
                # Create Landing AI Frame
                frame = Frame.from_image(temp_filepath)
                
                # Send to Landing AI with retry logic
                max_retries = 3
                retry_delay = 5
                
                for attempt in range(max_retries):
                    try:
                        frame.run_predict(predictor=predictor)
                        print("   Sent to Landing AI")
                        break
                    except Exception as e:
                        if "429" in str(e) or "Too Many Requests" in str(e):
                            if attempt < max_retries - 1:
                                print(f"   Rate limited, waiting {retry_delay} seconds...")
                                time.sleep(retry_delay)
                                retry_delay *= 2
                            else:
                                print("   ❌ Rate limit exceeded, skipping frame")
                                os.remove(temp_filepath)
                                continue
                        else:
                            print(f"   ❌ Analysis failed: {e}")
                            os.remove(temp_filepath)
                            break
                
                # Process results
                if hasattr(frame, 'predictions') and frame.predictions:
                    potholes_found = 0
                    detections_data = []
                    
                    for pred in frame.predictions:
                        confidence = getattr(pred, 'score', 0)
                        if confidence >= CONFIDENCE_THRESHOLD:
                            potholes_found += 1
                            
                            # Extract bounding box if available
                            bbox = None
                            if hasattr(pred, 'bboxes') and pred.bboxes:
                                try:
                                    bbox_obj = pred.bboxes[0] if isinstance(pred.bboxes, list) else pred.bboxes
                                    
                                    # Handle different bbox formats
                                    if hasattr(bbox_obj, 'x1'):  # Object with attributes
                                        bbox = {
                                            'x1': int(bbox_obj.x1),
                                            'y1': int(bbox_obj.y1),
                                            'x2': int(bbox_obj.x2),
                                            'y2': int(bbox_obj.y2)
                                        }
                                    elif isinstance(bbox_obj, (list, tuple)) and len(bbox_obj) >= 4:  # List/tuple format
                                        bbox = {
                                            'x1': int(bbox_obj[0]),
                                            'y1': int(bbox_obj[1]),
                                            'x2': int(bbox_obj[2]),
                                            'y2': int(bbox_obj[3])
                                        }
                                    elif isinstance(bbox_obj, dict):  # Dictionary format
                                        bbox = {
                                            'x1': int(bbox_obj.get('x1', bbox_obj.get('left', 0))),
                                            'y1': int(bbox_obj.get('y1', bbox_obj.get('top', 0))),
                                            'x2': int(bbox_obj.get('x2', bbox_obj.get('right', 0))),
                                            'y2': int(bbox_obj.get('y2', bbox_obj.get('bottom', 0)))
                                        }
                                    else:
                                        print(f"   Unknown bbox format: {type(bbox_obj)}")
                                        bbox = None
                                except Exception as e:
                                    print(f"   Bbox parsing error: {e}")
                                    bbox = None
                            
                            detection_data = {
                                'confidence': confidence,
                                'label': getattr(pred, 'label_name', 'pothole'),
                                'bbox': bbox,
                                'gps_location': current_location,
                                'timestamp': timestamp,
                                'analysis_id': analysis_count
                            }
                            detections_data.append(detection_data)
                    
                    if potholes_found > 0:
                        detection_count += potholes_found
                        print(f"   POTHOLE DETECTED! Found {potholes_found} pothole(s)")
                        
                        # Print detection details
                        for i, detection in enumerate(detections_data):
                            print(f"      Detection {i+1}: {detection['confidence']:.2f} confidence")
                            if current_location:
                                print(f"         GPS: {current_location['latitude']:.6f}, {current_location['longitude']:.6f}")
                        
                        # Save detection image and data
                        final_filename = f"pothole_{timestamp}.jpg"
                        final_filepath = os.path.join(screenshots_dir, final_filename)
                        os.rename(temp_filepath, final_filepath)
                        
                        # Save detailed JSON data
                        data_filename = f"pothole_{timestamp}_data.json"
                        data_filepath = os.path.join(logs_dir, data_filename)
                        
                        full_data = {
                            'timestamp': timestamp,
                            'analysis_id': analysis_count,
                            'image_file': final_filename,
                            'gps_location': current_location,
                            'detections': detections_data,
                            'total_detections': potholes_found,
                            'camera_settings': {
                                'width': 640,
                                'height': 480,
                                'camera_id': CAMERA_ID
                            }
                        }
                        
                        with open(data_filepath, 'w') as f:
                            json.dump(full_data, f, indent=2)
                        
                        # Log to daily file
                        log_message = f"POTHOLE DETECTED - Count: {potholes_found}, Image: {final_filename}"
                        if current_location:
                            log_message += f", GPS: {current_location['latitude']:.6f},{current_location['longitude']:.6f}"
                        log_to_daily_file(log_message)
                        
                        print(f"   Saved: {final_filename}")
                        print(f"   Data: {data_filename}")
                        
                    else:
                        print("   ✅ No potholes detected")
                        log_to_daily_file(f"Frame analyzed - No detections (Analysis #{analysis_count})")
                        if os.path.exists(temp_filepath):
                            os.remove(temp_filepath)
                else:
                    print("   ✅ No potholes detected")
                    log_to_daily_file(f"Frame analyzed - No detections (Analysis #{analysis_count})")
                    if os.path.exists(temp_filepath):
                        os.remove(temp_filepath)
                        
            except Exception as e:
                print(f"   ❌ Analysis failed: {e}")
                log_to_daily_file(f"Analysis failed - Error: {str(e)}")
                if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
            
            # Print summary every 5 analyses
            if analysis_count % 5 == 0:
                summary_msg = f"Summary: {analysis_count} analyses, {detection_count} potholes found"
                print(f" {summary_msg}")
                log_to_daily_file(summary_msg)
                
    except KeyboardInterrupt:
        print(f"\nStopped by user")
        log_to_daily_file("Session stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        log_to_daily_file(f"Session error: {str(e)}")
    finally:
        cap.release()
        if SHOW_CAMERA:
            cv2.destroyAllWindows()
        
        # Close GPS connections
        if gps_tracker.serial_connection:
            gps_tracker.serial_connection.close()
        
        # Log session end
        log_to_daily_file(f"Session ended - Total: {detection_count} potholes in {analysis_count} analyses")
    
    # Final summary
    print("\n" + "=" * 50)
    print(f"FINAL SUMMARY:")
    print(f"Total frames captured: {frame_count}")
    print(f"Frames analyzed by Landing AI: {analysis_count}")
    print(f"Potholes detected: {detection_count}")
    if os.path.exists(screenshots_dir):
        saved_images = len([f for f in os.listdir(screenshots_dir) if f.endswith('.jpg') and not f.startswith('temp_')])
        print(f"Images saved: {saved_images}")
    if os.path.exists(logs_dir):
        data_files = len([f for f in os.listdir(logs_dir) if f.endswith('.json')])
        log_files = len([f for f in os.listdir(logs_dir) if f.endswith('.log')])
        print(f"Data files created: {data_files}")
        print(f"Log files: {log_files}")
    print("=" * 50)

def main():
    """Main function with GPS setup options"""
    
    print("JETSON POTHOLE DETECTION WITH GPS")
    print("=" * 40)
    print("1. Start Detection with GPS")
    print("2. Test Camera Only")
    print("3. Test GPS Only")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        capture_with_opencv_and_gps()
    elif choice == "2":
        test_camera_only()
    elif choice == "3":
        test_gps_only()
    else:
        print("Invalid choice")

def test_camera_only():
    """Test camera without GPS"""
    print("Testing camera...")
    
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print(f"❌ Cannot open camera {CAMERA_ID}")
        return
    
    print("Showing 5-second preview (press 'q' to skip)")
    start_time = time.time()
    
    while (time.time() - start_time) < 5:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Camera Test', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Camera test complete")

def test_gps_only():
    """Test GPS functionality"""
    print("Testing GPS...")
    
    gps_tracker = GPSTracker(GPS_METHOD)
    
    print("Getting GPS readings for 30 seconds...")
    start_time = time.time()
    reading_count = 0
    
    while (time.time() - start_time) < 30:
        location = gps_tracker.get_location()
        if location:
            reading_count += 1
            print(f"Reading {reading_count}: {location['latitude']:.6f}, {location['longitude']:.6f} "
                  f"(Sats: {location.get('satellites', 'N/A')})")
        else:
            print("No GPS fix available")
        
        time.sleep(2)
    
    print(f"✅ GPS test complete - {reading_count} successful readings")

if __name__ == "__main__":
    main()
