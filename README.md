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

### System Used
- **JetPack 4.6.1** (includes Ubuntu 18.04 LTS, CUDA 10.2, cuDNN 8.2)
- **Python 3.6.9** (pre-installed with JetPack)
- **OpenCV 4.1.1** with CUDA support (pre-installed with JetPack)

## Contact

**Author**: Tejas Bharadwaj
**Project Link**: [https://github.com/tejas991/pothole-detection-jetson](https://github.com/YOUR_USERNAME/pothole-detection-jetson)

---

*For detailed technical documentation and advanced configuration options, see the `docs/` directory.*
