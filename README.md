# 🔒 Login Anomaly Detector (Flask) 🛡️

<div align="center">

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-FF6B6B?style=for-the-badge&logo=shield&logoColor=white)

**🌍 Geo-location based anomaly detection for suspicious login attempts**

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [⚡ Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [📋 Prerequisites](#-prerequisites)
- [🚀 Setup & Installation](#-setup--installation)
- [🏃‍♂️ Running the Application](#️-running-the-application)
- [💡 Usage Guide](#-usage-guide)
- [🛣️ API Routes](#️-api-routes)
- [📊 Data Model](#-data-model)
- [🧠 Anomaly Detection Logic](#-anomaly-detection-logic)
- [🌍 Geo-location Behavior](#-geo-location-behavior)
- [⚠️ Security Disclaimer](#️-security-disclaimer)
- [🎨 Customization Ideas](#-customization-ideas)
- [🔧 Troubleshooting](#-troubleshooting)
- [📄 License](#-license)

---

## 🎯 Overview

A **sophisticated demo web application** that intelligently flags suspicious login attempts based on geo-location analysis. When a user attempts to login from outside India, they are automatically redirected to a secure OTP verification step. All authentication attempts are meticulously logged to `data/users.csv` for comprehensive audit trails and security analysis.

---

## ✨ Features

🔐 **Secure Authentication**
- Email/password login with dynamic country selection
- Real-time geo-location detection and validation

🚨 **Smart Anomaly Detection** 
- Intelligent rule engine: non-India locations flagged as suspicious
- Automatic threat response with OTP verification flow

📱 **Multi-Factor Authentication**
- Seamless OTP integration (demo code: `123456`)
- Enhanced security for suspicious login attempts

📊 **Comprehensive Logging**
- Detailed audit trail in `data/users.csv`
- Track success, failed, and OTP-required attempts

🌐 **Advanced Geo-Detection**
- Best-effort IP-based country lookup via `ipapi.co`
- Graceful fallback mechanisms for network issues

🎨 **Modern UI/UX**
- Clean, responsive design with Tailwind CSS
- Bootstrap Icons for enhanced visual appeal

---

## ⚡ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | ![Flask](https://img.shields.io/badge/Flask_3-000000?style=flat-square&logo=flask&logoColor=white) |
| **Templates** | ![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat-square&logo=jinja&logoColor=white) |
| **Data Management** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) CSV Storage |
| **Styling** | ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) + Bootstrap Icons |

---

## 📁 Project Structure

```
login-anomaly-detector/
├── 📱 app.py                 # Main Flask application & geo lookup
├── 🧠 rules.py               # Anomaly detection rules engine  
├── 🛠️ utils.py               # CSV utilities & logging helpers
├── 📊 data/users.csv         # User database & audit logs
├── 🎨 templates/             # Jinja2 HTML templates
│   ├── login.html           # Authentication interface
│   ├── dashboard.html       # Success dashboard
│   ├── otp.html            # OTP verification
│   └── suspicious.html     # Security warning
├── 💅 static/style.css       # Custom styling (minimal)
└── 📦 requirements.txt       # Python dependencies
```

---

## 📋 Prerequisites

| Requirement | Version |
|-------------|---------|
| 🐍 **Python** | 3.10+ |
| 🌐 **Internet Access** | Required for `ipapi.co` geolocation |

> ⚠️ **Note**: Application functions with limited features if offline

---

## 🚀 Setup & Installation

### 1️⃣ Navigate to Project Directory
```
cd login-anomaly-detector
```

### 2️⃣ Create Virtual Environment 
```
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

---

## 🏃‍♂️ Running the Application

```
python app.py
```

🎉 **Success!** Navigate to [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/) in your browser

---

## 💡 Usage Guide

### 🔑 Authentication Flow

1. **🏠 Access Login Page** → Navigate to `/` (root endpoint)
2. **👤 Enter Credentials** → Use existing users from `data/users.csv`
   - Example: `alice` / `pass123`
3. **🌍 Select Country**:
   - 🇮🇳 **India** → Direct dashboard access (✅ SUCCESS)
   - 🌏 **Other Countries** → Security verification flow (🚨 OTP_REQUIRED)
4. **🔐 OTP Verification** → Enter `123456` to proceed to dashboard

---

## 🛣️ API Routes

| Method | Endpoint | Purpose | Response |
|---------|----------|---------|----------|
| `GET` | `/` | 🏠 Login interface with IP-based country detection | HTML Form |
| `POST` | `/` | 🔐 Authentication & anomaly rule processing | Redirect based on location |
| `GET` | `/dashboard` | ✅ Success screen with user details | Dashboard view |
| `GET/POST` | `/otp` | 📱 Multi-factor authentication | OTP verification form |
| `GET` | `/suspicious` | ⚠️ Security warning interface | Warning + OTP redirect link |

---

## 📊 Data Model

### 📁 `data/users.csv` Structure

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | Integer | Unique user identifier |
| `username` | String | User login name |
| `password` | String | Authentication credential |
| `ip_address` | String | Client IP address |
| `login_time` | DateTime | Timestamp (YYYY-MM-DD HH:MM:SS) |
| `device_id` | String | Device fingerprint |
| `geo_location` | String | Detected country/region |
| `login_result` | Enum | `SUCCESS` \| `FAILED` \| `OTP_REQUIRED` |

> 💡 **Note**: `utils.log_attempt()` appends audit entries with masked passwords (`-`)

---

## 🧠 Anomaly Detection Logic

### 🎯 Current Rule Set (`rules.py`)

```
🔍 if location.lower() != "india":
    return "suspicious"  # 🚨 Triggers OTP verification
```

### 🚀 **Future Enhancement Opportunities**:
- 🖥️ Device fingerprinting analysis
- ⏰ Time-of-day pattern recognition  
- 🌐 IP reputation scoring
- 📈 Behavioral velocity tracking

---

## 🌍 Geo-location Behavior

### 🔍 **Server-Side Detection**
- **API**: `ipapi.co/<ip>/json/` with 2.5s timeout
- **Fallback**: "Unknown" for localhost (127.x) or API failures

### 💻 **Client-Side Enhancement**  
- **JavaScript**: `ipapi.co/json/` for dynamic country pre-selection
- **Flexibility**: Easily replaceable with alternative providers

> 💡 **Pro Tip**: Consider local GeoIP databases for production deployments

---

## ⚠️ Security Disclaimer

> 🚨 **EDUCATIONAL USE ONLY** - This demonstration project contains intentional security vulnerabilities:

| ⚠️ Issue | 🔧 Production Fix |
|----------|-------------------|
| Plain-text password storage | Implement bcrypt/Argon2 hashing |
| Hard-coded OTP (`123456`) | SMS/Email OTP integration |
| Static Flask `secret_key` | Environment-based configuration |
| CSV-based storage | Database migration (PostgreSQL/MongoDB) |

---

## 🎨 Customization Ideas

### 🗄️ **Database Migration**
- Replace CSV with SQLite/PostgreSQL
- Implement proper schema design

### 🔐 **Enhanced Security**
- Password hashing with salt
- User registration workflow
- Session management

### 📱 **Real Authentication**
- SMS/Email OTP integration
- TOTP/Hardware token support

### 🤖 **Advanced ML Detection**
- Country velocity analysis
- ASN-based risk scoring
- Device history profiling

### 📊 **Admin Dashboard**
- Real-time security monitoring
- Audit log visualization
- Risk assessment reports

---

## 🔧 Troubleshooting

### 🚫 **Common Issues & Solutions**

| 🔴 Problem | 💚 Solution |
|------------|-------------|
| `data/users.csv not found` | Ensure working directory is `login-anomaly-detector/` |
| Country shows "Unknown" | Check network connectivity; manual selection still works |
| Pip install errors (Windows) | Upgrade pip: `python -m pip install -U pip` |
| Port 5000 already in use | Kill existing Flask processes or change port in `app.py` |

### 🆘 **Need More Help?**
Check the [Issues](https://github.com/Kathan-2007/IntelliHack-2025-daiict/issues) section or create a new issue with detailed error information.

---

## 📄 License

📜 **MIT License** - Educational and demonstration purposes

---

<div align="center">

### 🌟 Star this repository if you found it helpful! 

**Made with ❤️ for cybersecurity education**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=IntelliHack-2025.login-anomaly-detector)

</div>
```

