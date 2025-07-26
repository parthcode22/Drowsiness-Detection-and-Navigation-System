
# 🚘 Drowsiness Detection and Navigation System

An innovative, AI-powered system aimed at **reducing road accidents caused by driver fatigue**, especially designed for **manual and budget-friendly vehicles**. This project offers a real-time drowsiness detection and rest stop navigation feature — bringing safety technology to every driver, not just luxury car owners.

---

## 📌 Project Overview

### 🚗 Drowsiness Detection
- Uses **OpenCV**, **Deep Learning**, and **facial landmark detection** to monitor eye movement and signs of fatigue.
- When drowsiness is detected, the system **triggers an instant sound alert** to wake the driver and avoid potential accidents.

### 🗺️ Navigation to Nearby Rest Stops
- After detection, the system **recommends nearby rest stops** using a map-based navigation module.
- Helps drivers find a **safe location to rest**, thereby reducing risks on the road.

---

## 💡 Why This Project?

While high-end vehicles offer built-in safety systems, **most manual or budget cars lack such features**. This project bridges the gap by offering an affordable, **AI-based safety solution** that works on **any vehicle** using just a webcam and GPS access.

---

## 🎯 Key Features

- ✅ **Real-time Drowsiness Detection** using Computer Vision
- ✅ **AI-based Sound Alert** System to Prevent Microsleep Incidents
- ✅ **Map Integration** to Recommend Nearby Rest Stops
- ✅ **Budget-Friendly & Hardware-Independent** – Works in Any Vehicle
- ✅ **Modular Code Design** for Future Enhancements (e.g., GPS integration, mobile version)

---

## 🧠 Technologies Used

- Python
- OpenCV
- Dlib / Mediapipe (for facial landmarks)
- Deep Learning (Keras/TensorFlow or PyTorch)
- Streamlit (for GUI)
- Folium or Geopy (for rest stop navigation/map rendering)
- Numpy, Pandas

---

## 📂 Project Structure

```bash
Drowsiness-Detection-System/
│
├── drowsiness_detection.py         # Core detection logic
├── navigation_module.py            # Nearby rest stop locator
├── app.py                          # Streamlit app interface
├── assets/                         # Alert sounds, images
├── models/                         # Pre-trained models
├── utils/                          # Helper functions
├── requirements.txt                # List of dependencies
└── README.md                       # You're here!


