# SnapClass 📸

## AI-Powered Attendance System

Making classroom attendance faster, smarter, and hands-free using Face Recognition & Voice Identification.
# About the Project
SnapClass is a Streamlit-based web application that automates classroom attendance using AI. Teachers can take attendance by simply uploading a class photo or a bulk audio recording. Students self-register with their face and voice, and the system identifies them automatically.
No roll calls. No manual entry. Just snap and go.
##Features

🧑‍🏫 Teacher Portal — Register/login, create subjects, take attendance via face or voice
🧑‍🎓 Student Portal — Self-register with face photo and voice sample, enroll in subjects via QR code
📸 Face Recognition — Uses dlib + SVM classifier on 128-dimensional face embeddings
🎙️ Voice Identification — Uses Resemblyzer for speaker embedding and cosine similarity matching
📊 Attendance Records — Per-subject attendance logs with session history
🔗 QR Code Enrollment — Teachers share a join link/QR; students auto-enroll on scan
☁️ Cloud Backend — Supabase (PostgreSQL) stores all users, embeddings, subjects, and logs
🔒 Secure Auth — Passwords hashed with bcrypt
##🛠️ Tech Stack

- 🎨 **Frontend & App:** Streamlit
- 👤 **Face Recognition:** dlib, face_recognition_models, scikit-learn (SVM)
- 🎙️ **Voice Recognition:** Resemblyzer, librosa
- 🗄️ **Database:** Supabase (PostgreSQL)
- 🖼️ **Image Processing:** Pillow, NumPy
- 🔐 **Authentication:** bcrypt
- 📱 **QR Code Generation:** segno

##Project Structure

snapclass_deploy/
├── app.py                         
├── requirements.txt
├── assets/
│   ├── teacher.png
│   ├── student.png
│   └── download.png                
└── src/
    ├── screens/
    │   ├── home_screen.py          
    │   ├── teacher_screen.py       
    │   └── student_screen.py       
    ├── pipelines/
    │   ├── face_pipeline.py        
    │   └── voice_pipeline.py       
    ├── componets/
    │   ├── header.py
    │   ├── subject_card.py
    │   ├── dialog_create_subject.py
    │   ├── dialog_share_subject.py
    │   ├── dialog_enroll.py
    │   ├── dialog_auto_enroll.py   
    │   ├── dialog_add_photo.py
    │   ├── dialog_attendance_results.py
    │   └── dialog_voice_attendance.py
    ├── ui/
    │   └── base_layout.py         
    └── database/
        ├── config.py               
        └── db.py   
## 🗄️ Database

The system uses **Supabase (PostgreSQL)** as the backend database.

### Main Tables

- **teachers** – Stores teacher account information and authentication details.
- **students** – Stores student profiles along with face and voice embeddings.
- **subjects** – Stores subject information and teacher assignments.
- **subject_students** – Maps students to their enrolled subjects.
- **attendance_logs** – Records attendance status for each student and session.
## 🚀 Getting Started

### Prerequisites

- Python 3.10 or 3.11
- A Supabase account and project
- CMake
- C++ Build Tools (required for dlib installation)
- Git

> **Note:** dlib requires CMake and a C++ compiler to build successfully.

##On Ubuntu/Debian:

sudo apt-get install cmake build-essential libopenblas-dev liblapack-dev

##On macOS:

brew install cmake

On Windows: Install CMake and Visual Studio Build Tools.
##Installation

##1.Clone the repository

git clone https://github.com/your-username/snapclass.git
   cd snapclass
   
##2.Create and activate a virtual environment

python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
##3.Install dependencies

pip install setuptools==69.0.0   # must come first (dlib requirement)
pip install -r requirements.txt
 ⚠️ dlib and face_recognition_models take a few minutes to build/install. This is normal.
##Environment Setup

SnapClass uses Streamlit secrets for credentials. Create the file .streamlit/secrets.toml in the project root:
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-supabase-anon-or-service-role-key"
🔒 Never commit this file. It is (or should be) listed in .gitignore.
##Running the App

##streamlit run app.py

The app will open at http://localhost:8501.

##How It Works

##Face Recognition Pipeline

1.Student uploads a photo during registration → dlib extracts a 128-dimensional face embedding.

2.Embeddings are stored in Supabase.

3.When teacher uploads a class photo → all student embeddings are loaded and an SVM classifier is trained on the fly (cached with st.cache_resource).

4.Faces in the class photo are encoded and matched. Students within a distance threshold of 0.40 are marked present.
##Voice Identification Pipeline

1.Student records a voice sample during registration → Resemblyzer extracts a speaker embedding.

2.Teacher uploads a bulk audio recording of the class.

3.Audio is segmented using librosa silence detection.

4.Each segment's embedding is compared against all stored embeddings using cosine similarity. Students above a threshold of 0.65 are marked present.

##QR Code Enrollment

1.Teacher generates a shareable link with a ?join-code=<subject_code> query parameter.

2.When a student opens that link, the app auto-detects the join code, switches to the student portal, and opens the enrollment dialog immediately.

##Usage Guide

##As a Teacher

1.Open the app → click Teacher Portal

2.Register an account or log in

3.Go to Manage Subjects → create a subject with a code, name, and section

4.Share the subject's QR code or link with students

5.Go to Take Attendance → upload a class photo (face) or audio (voice)

6.View results in Attendance Records

##As a Student

1.Open the app → click Student Portal

2.Register with your name, a clear face photo, and a short voice clip

3.Log in and go to Enroll in Subject → enter the subject code (or scan the QR link)

4.Your attendance will be tracked automatically when teachers run recognition

##Deployment

##Deploy on Streamlit Community Cloud (Free)

1.Push your code to a public GitHub repository

2.Go to share.streamlit.io and connect your repo

3.Set the main file path to app.py

4.Under Advanced Settings → Secrets, add:

SUPABASE_URL = "..."
   SUPABASE_KEY = "..."
   
5.Click Deploy
⚠️ dlib requires build tools. Streamlit Cloud supports it, but the first deploy may take 5–10 minutes.
##Notes for Production

1.Use the service role key (not anon key) if you need to bypass RLS in Supabase, or configure proper Row Level Security policies.

2.Add Supabase RLS policies to restrict students from reading other students' embeddings.

3.Consider caching embeddings locally to avoid re-fetching on every session.

##Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

Fork the repo

1.Create your branch: git checkout -b feature/your-feature

2.Commit your changes: git commit -m 'Add your feature'

3.Push to the branch: git push origin feature/your-feature

4.Open a Pull Request

##License

This project is licensed under the MIT License.



