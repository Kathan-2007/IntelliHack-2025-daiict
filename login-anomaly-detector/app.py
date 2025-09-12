from flask import Flask, render_template, request, redirect, url_for, session
import socket
from utils import load_users, log_attempt
from rules import detect_anomaly
import json
from urllib.request import urlopen
from urllib.error import URLError

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session


# Mock: get IP and location (for testing purpose only)
def get_client_ip():
    return request.remote_addr or "127.0.0.1"

def get_mock_location(ip):
    """
    Demo logic:
    - If username is 'alice' → India
    - If username is 'bob' or others → USA
    (You can replace this with real geo-lookup using ipinfo/geoip later)
    """
    username = session.get("username", "").lower()
    if username == "alice":
        return "India"
    return "USA"


def geolocate_ip_country(ip_address: str) -> str:
    """
    Fetch country name for the given IP using a public API.
    Falls back to "Unknown" on errors or local IPs.
    """
    try:
        # If running locally, API with specific IP won't help; let API infer from requester
        endpoint = f"https://ipapi.co/{'' if ip_address.startswith('127.') else ip_address}/json/"
        with urlopen(endpoint, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            country_name = data.get("country_name")
            if isinstance(country_name, str) and country_name.strip():
                return country_name.strip()
    except URLError:
        pass
    except Exception:
        pass
    return "Unknown"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        selected_country = request.form.get("country", "Unknown")

        df = load_users()
        user = df[(df["username"] == username) & (df["password"] == password)]

        ip = get_client_ip()
        device_id = socket.gethostname()

        if not user.empty:
            session["username"] = username
            # Prefer user-selected country; otherwise fall back to server IP geolocation
            location = selected_country or geolocate_ip_country(ip) or "Unknown"
            session["location"] = location

            # Non-India → OTP page
            if detect_anomaly(location):
                log_attempt(username, ip, device_id, location, "OTP_REQUIRED")
                return redirect(url_for("suspicious"))
            else:
                log_attempt(username, ip, device_id, location, "SUCCESS")
                return redirect(url_for("dashboard"))
        else:
            log_attempt(username, ip, device_id, "Unknown", "FAILED")
            return render_template("login.html", error="Invalid Credentials")

    # GET: pre-detect country to preselect in dropdown
    ip = get_client_ip()
    detected_country = geolocate_ip_country(ip)
    return render_template("login.html", detected_country=detected_country)


@app.route("/dashboard")
def dashboard():
    username = session.get("username", "Guest")
    location = session.get("location", "Unknown")
    return render_template("dashboard.html", username=username, location=location)


@app.route("/otp", methods=["GET", "POST"])
def otp():
    if request.method == "POST":
        otp_entered = request.form.get("otp")
        # Hardcoded OTP = 123456 for demo
        if otp_entered == "123456":
            return redirect(url_for("dashboard"))
        else:
            return render_template("otp.html", error="Invalid OTP. Try again.")
    return render_template("otp.html")


@app.route("/suspicious")
def suspicious():
    username = session.get("username", "User")
    location = session.get("location", "Unknown")
    return render_template("suspicious.html", user=username, location=location)


if __name__ == "__main__":
    app.run(debug=True)
