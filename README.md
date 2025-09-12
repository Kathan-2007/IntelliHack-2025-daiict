## Login Anomaly Detector (Flask)

A simple demo web app that flags suspicious logins based on geo-location. If a user logs in from outside India, they are redirected to an OTP verification step. All login attempts (success, failed, OTP required) are appended to `data/users.csv` for audit and analysis.

### Features
- **Email/password login** with country selection
- **Anomaly rule**: any country other than India is treated as suspicious
- **OTP flow**: suspicious logins get redirected to an OTP page (demo OTP `123456`)
- **Logging**: appends each login attempt to `data/users.csv`
- **Geo-detection**: attempts best-effort IP-based country lookup using `ipapi.co` (with graceful fallback)
- **Clean UI**: Tailwind CSS + Bootstrap Icons via CDN

### Tech Stack
- **Backend**: Flask 3
- **Views**: Jinja2 templates (`templates/`)
- **Data**: CSV file at `data/users.csv` managed with pandas

### Project Structure
```
login-anomaly-detector/
  app.py                 # Flask app with routes and basic geo lookup
  rules.py               # Simple anomaly rule (non-India => suspicious)
  utils.py               # CSV load and login-attempt logging helpers
  data/users.csv         # Seed data + grows with new attempts
  templates/             # Jinja2 templates (login, dashboard, otp, suspicious)
  static/style.css       # (optional) custom styles (minimal)
  requirements.txt       # Python dependencies
```

### Prerequisites
- Python 3.10+
- Internet access (for `ipapi.co` demo geolocation; app still works without it)

### Setup
```powershell
# from the project root (where app.py is inside login-anomaly-detector)
cd login-anomaly-detector

# create & activate virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

### Run
```powershell
# run development server
python app.py
```
- The app starts in debug mode at `http://127.0.0.1:5000/`.
- Open the URL in a browser to access the login page.

### Usage
1. Go to `/` (login page)
2. Enter a username and password present in `data/users.csv` (e.g., `alice / pass123`)
3. Select a country:
   - **India** → direct to dashboard (success)
   - **Not India** → redirected to suspicious page then OTP page
4. On OTP page, enter `123456` to continue to the dashboard

### Routes
- `GET /` — Login form, attempts to pre-select country via IP lookup
- `POST /` — Authenticates user against `data/users.csv`, applies anomaly rule, logs result
- `GET /dashboard` — Shows a success screen with username and location
- `GET|POST /otp` — OTP verification (demo code `123456`)
- `GET /suspicious` — Warning screen; links to OTP

### Data Model (`data/users.csv`)
Columns:
- `user_id` (int)
- `username` (string)
- `password` (string)
- `ip_address` (string)
- `login_time` (YYYY-MM-DD HH:MM:SS)
- `device_id` (string)
- `geo_location` (string)
- `login_result` (enum: `SUCCESS`, `FAILED`, `OTP_REQUIRED`)

Notes:
- `utils.log_attempt(...)` appends new rows with masked password (`-`).
- The file doubles as seed user store and audit log. Keep initial rows for demo users.

### Anomaly Logic
- Defined in `rules.py`:
  - If `location.lower() != "india"` → suspicious → OTP required
- You can extend this to include device fingerprinting, time-of-day patterns, IP reputation, etc.

### Geo-location Behavior
- `app.py` tries `ipapi.co/<ip>/json/` (2.5s timeout). If the client IP is local (127.x) or any error occurs, it falls back to `"Unknown"`.
- On the login page, client-side JS also tries `ipapi.co/json/` to pre-select the country.
- You can replace this with your preferred provider or local GeoIP database.

### Security Disclaimer
- This project is for demo/learning only:
  - Passwords are stored in plain text in the CSV for demonstration.
  - OTP is hardcoded (`123456`).
  - Flask `secret_key` is hardcoded in `app.py`.
- Do not use as-is in production.

### Customization Ideas
- Replace CSV with a database (SQLite/Postgres)
- Implement proper password hashing and user registration
- Real OTP via email/SMS
- Smarter anomaly detection (country velocity, ASN, device history)
- Admin dashboard to review audit logs

### Troubleshooting
- "`data/users.csv not found`": ensure the file exists and the working directory is `login-anomaly-detector/` when running
- IP-based country shows `Unknown`: network blocked or API timed out → proceed with manual country selection; app still works
- Pip install errors on Windows: upgrade pip `python -m pip install -U pip`

### License
MIT (for educational/demo purposes).
