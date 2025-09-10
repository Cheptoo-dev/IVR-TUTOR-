# 🎓 IVR Tutor - Inclusive Education for All

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Africa's Talking](https://img.shields.io/badge/Powered%20by-Africa's%20Talking-blue.svg)](https://africastalking.com/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Accessibility](https://img.shields.io/badge/accessibility-first-success.svg)]()

> **Democratizing education through voice-first learning** - Making quality education accessible to visually impaired students, those with dyslexia, and learners in low-resource settings across Africa.

## 🌟 Why This Matters

**1.2 million** children in Sub-Saharan Africa are visually impaired, and **millions more** struggle with dyslexia and reading difficulties. Yet 99% of e-learning platforms require visual interaction and high-speed internet.

**IVR Tutor changes this.**

Just dial a number. No smartphone needed. No internet required. No visual barriers.

---

## 🚀 The Solution

IVR Tutor is a voice-first educational platform that transforms any basic phone into a powerful learning tool. Students access interactive lessons, quizzes, and progress tracking through simple phone calls.

### ✨ Key Features

🎯 **Inclusive by Design**
- Fully accessible for visually impaired learners
- Supports students with dyslexia and reading difficulties
- Works on any phone - feature phones included

📱 **Zero-Barrier Access**
- No app downloads or internet required
- Local language support (English + Swahili + more)
- Works in areas with poor internet connectivity

🎮 **Engaging Learning Experience**
- Interactive audio lessons with immediate feedback
- Gamified quizzes with keypad responses
- Progress tracking via SMS notifications
- Motivational content and study reminders

👥 **Community Integration**
- Parent/guardian progress updates
- Teacher dashboard for content management
- Peer learning group features

---

## 📞 How It Works

### For Students:
```
1. 📞 Dial +254XXXXXXXX
2. 🎵 Listen to menu: "Press 1 for Math, 2 for English..."
3. 📚 Engage with audio lessons
4. ✏️  Answer quizzes using keypad (1,2,3,4)
5. 📈 Receive SMS progress updates
6. 🔄 Continue learning journey
```

### The Magic Behind the Scenes:
```
Student Call → IVR Menu → Audio Content → Interactive Quiz → 
Progress Tracking → SMS Notifications → Learning Analytics
```

---

## 🛠️ Technical Architecture

### Core Technologies
- **🎙️ Africa's Talking Voice API** - IVR system and audio delivery
- **📱 Africa's Talking SMS API** - Progress notifications and reminders
- **⚡ FastAPI Backend** - Core learning logic and user management
- **🗄️ PostgreSQL Database** - Student progress and content management
- **☁️ AWS S3** - Audio content storage and delivery
- **🧠 ML Pipeline** - Adaptive learning recommendations

### System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   📞 Phone Call  │───▶│   🎙️ IVR Engine   │───▶│  📚 Content API  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                         │
                                ▼                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  📱 SMS Service  │◀───│  🧠 Learning AI   │───▶│  📊 Analytics    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.9+
- Africa's Talking API credentials
- PostgreSQL database

### Installation
```bash
git clone https://github.com/yourusername/ivr-tutor.git
cd ivr-tutor

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your Africa's Talking credentials

# Run database migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

### Test the System
```bash
# Call the test number
curl -X POST http://localhost:8000/test-call \
  -H "Content-Type: application/json" \
  -d '{"phone": "+254700000000"}'
```

---

## 📊 Demo & Impact

### 🎬 Live Demo
**Call +254XXXXXXXX** to experience IVR Tutor yourself!

### 📈 Projected Impact
- **500,000+ students** could be reached in Year 1
- **80% cost reduction** compared to traditional assistive technology
- **24/7 availability** in remote areas
- **Multiple language support** for diverse communities

### 🎯 Success Metrics (Hackathon Build)
- ✅ Complete IVR lesson flow
- ✅ SMS progress notifications
- ✅ Multi-language support (EN/SW)
- ✅ Real-time analytics dashboard
- ✅ Teacher content management
- ✅ Adaptive learning recommendations

---

## 🗂️ Project Structure

```
ivr-tutor/
├── 📁 api/                  # FastAPI backend
│   ├── models/             # Database models
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   └── utils/              # Helper functions
├── 📁 content/             # Audio lessons and scripts
├── 📁 dashboard/           # Teacher/admin web interface
├── 📁 ml/                  # Learning recommendation engine
├── 📁 scripts/             # Database setup and utilities
├── 📁 tests/               # Test suites
├── 📄 requirements.txt     # Python dependencies
├── 📄 docker-compose.yml   # Container orchestration
└── 📄 README.md           # This file
```

---

## 🧪 Testing

### Run the Full Test Suite
```bash
pytest tests/ -v
```

### Test Specific Components
```bash
# Test IVR flow
pytest tests/test_ivr.py -v

# Test SMS notifications
pytest tests/test_sms.py -v

# Test learning analytics
pytest tests/test_analytics.py -v
```

---

## 🌍 Roadmap

### 🎯 Phase 1 
- [x] Core IVR functionality
- [x] SMS progress notifications
- [x] Basic analytics dashboard
- [x] Multi-language support

### 🚀 Phase 2 
- [ ] AI-powered voice tutoring
- [ ] Advanced speech recognition
- [ ] Offline content download
- [ ] Parent mobile app companion

### 🌟 Phase 3 
- [ ] Government partnership integration
- [ ] Advanced learning analytics
- [ ] Content marketplace
- [ ] Multi-country deployment

---

## 🤝 Contributing

We welcome contributors who are passionate about inclusive education!

### Ways to Contribute:
1. **🐛 Bug fixes** - Help us improve stability
2. **✨ New features** - Add functionality for different learning needs
3. **🌍 Translations** - Add support for more local languages
4. **📚 Content** - Create audio lessons and educational content
5. **📖 Documentation** - Help others understand and use the platform

### Getting Started:
```bash
# Fork the repository
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ivr-tutor.git

# Create a feature branch
git checkout -b feature/amazing-new-feature

# Make your changes and commit
git commit -m "Add amazing new feature"

# Push and create a pull request
git push origin feature/amazing-new-feature
```

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Africa's Talking](https://africastalking.com/)** - For providing the powerful APIs that make this possible
- **EdTech Hackathon Organizers** - For creating a platform to address educational inequality
- **Accessibility Advocates** - For inspiring inclusive design practices
- **The Open Source Community** - For the tools and libraries that power this project

---



<div align="center">

**Built with ❤️ for inclusive education in Africa** during the Afrika's Talking Edtech Hackathon

*"Education is the most powerful weapon which you can use to change the world."* - Nelson Mandela

[⭐ Star this repo](https://github.com/cheptoo-dev/ivr-tutor) if you believe in accessible education for all!

</div># IVR-TUTOR-
