# AI Real-Time GYM Trainer

An AI-powered real-time workout trainer that uses computer vision, pose estimation, Large Language Models, and Text-to-Speech to analyze exercises and provide personalized feedback during workouts.

The application uses the webcam to detect body posture, count repetitions, identify incorrect exercise form, and provide AI-generated coaching feedback.

---

## Features

- Real-time exercise detection
- Human pose estimation using MediaPipe
- Automatic repetition counting
- Exercise form analysis
- AI-powered workout coaching
- Voice feedback using Text-to-Speech
- Real-time exercise metrics
- Incorrect-form detection
- Workout progress tracking
- Workout history storage
- User authentication
- Real-time video processing using WebRTC
- Streamlit-based interactive interface

---

## Supported Exercises

| Exercise | Form Analysis | Rep Counting |
|----------|---------------|--------------|
| Squats | Yes | Yes |
| Push-ups | Yes | Yes |
| Biceps Curls | Yes | Yes |
| Shoulder Press | Yes | Yes |
| Lunges | Yes | Yes |

---

## How It Works

```text
Webcam
   |
   v
WebRTC Video Stream
   |
   v
MediaPipe Pose Landmarker
   |
   v
Exercise Detector
   |
   v
Exercise Metrics
   |
   v
Form Analysis
   |
   v
AI Coach (Groq)
   |
   v
Text-to-Speech (gTTS)
   |
   v
WebRTC Audio
   |
   v
Voice Feedback
```

The system continuously processes the user's pose and calculates exercise-specific metrics. When an incorrect movement or form issue is detected, the AI coach generates appropriate feedback.

---

## Tech Stack

### Programming Language

- Python

### AI and Machine Learning

- MediaPipe
- Groq LLM
- Llama-based AI model

### Computer Vision

- OpenCV
- MediaPipe Pose Landmarker

### Voice

- gTTS (Google Text-to-Speech)
- WebRTC Audio Streaming

### Framework

- Streamlit
- streamlit-webrtc

### Data Processing

- NumPy
- Pandas

### Database

- SQLite

### Other Libraries

- PyAV
- python-dotenv
- Threading

---

## Project Structure

```text
AI-GYM-Trainer/
│
├── main.py
│
├── detectors/
│   ├── squat.py
│   ├── pushup.py
│   ├── biceps_curl.py
│   ├── shoulder_press.py
│   └── lunges.py
│
├── services/
│   ├── auth/
│   │   └── login.py
│   │
│   ├── coaching/
│   │   ├── llm.py
│   │   ├── tts.py
│   │   └── voice_pipeline.py
│   │
│   ├── config/
│   │   └── workout_config.py
│   │
│   ├── persistence/
│   │   └── exercise_repository.py
│   │
│   ├── state/
│   │   └── session_defaults.py
│   │
│   ├── tracking/
│   │   └── metrics.py
│   │
│   ├── ui/
│   │   └── style_loader.py
│   │
│   └── vision/
│       └── exercise_video_processor.py
│
├── ml_models/
│   └── pose_landmarker_full.task
│
├── static/
│   ├── style.css
│   └── AdobeClean.otf
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ishu2293/AI-GYM-Trainer.git
```

```bash
cd AI-GYM-Trainer
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If required, update WebRTC:

```bash
pip install -U streamlit-webrtc
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

The Groq API is used to generate personalized workout coaching feedback.

## Running the Application

Start the Streamlit application:

```bash
streamlit run main.py
```

The application will be available at:

```text
http://localhost:8501
```

Open the URL in your browser and allow camera access.

---

## How to Use

### Step 1: Login

Login to the application using the provided authentication system.

### Step 2: Select Exercise

Choose an exercise from the sidebar.

Available exercises:

```text
Squats
Push-ups
Biceps Curls
Shoulder Press
Lunges
```

### Step 3: Set Workout Plan

Select:

```text
Sets
Reps per Set
```

Then click:

```text
Start Session
```

### Step 4: Start Workout

Allow camera access and position yourself so that your body is clearly visible.

The application will automatically analyze your movements.

### Step 5: Receive Feedback

The AI trainer provides:

- Repetition count
- Exercise metrics
- Form analysis
- AI-generated feedback
- Voice coaching

---

## Exercise Analysis

### Squats

The system analyzes:

- Knee angle
- Back angle
- Squat depth
- Repetition movement

Example feedback:

```text
Your squat is not deep enough.
```

## Real-Time Metrics

The application displays exercise-specific metrics while the workout is running.

Example:

```text
Squat Metrics

Knee Angle:     92°
Back Angle:     165°
Depth Status:   GOOD
```

Shoulder Press:

```text
Shoulder Press Metrics

Elbow Angle:       175°
Arm Extension:     FULL
Back Arch:         Slight Arch
```

---

## Rep Counting

Each exercise detector analyzes pose landmarks and determines the movement phase.

```text
Starting Position
       |
       v
Movement
       |
       v
Target Position
       |
       v
Return Movement
       |
       v
Rep Completed
```

The completed repetitions are then updated in the workout session.

---

## Workout History

Workout information is stored using SQLite.

The application records:

- User
- Exercise
- Repetitions
- Sets
- Workout duration
- Date

The history section allows users to review their previous workouts.

---

## Authentication

The application includes a login system that allows users to access the workout trainer.

User session information is maintained using Streamlit session state and the application's local database.

---

## Author

**Ishwari Daphal**

B.Tech Information Technology  
D. Y. Patil College of Engineering, Akurdi, Pune

---

## Repository

GitHub:

https://github.com/ishu2293/AI-GYM-Trainer
