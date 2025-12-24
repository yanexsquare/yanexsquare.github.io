from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app) # Allows your website to communicate with this API

# --- CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "yaseenaidev@gmail.com"
SENDER_PASSWORD = "ejxeewpwdcnepesa" # Use a Google App Password

def log_lead(email):
    """Saves the lead email to a CSV file."""
    with open('leads.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email])

@app.route('/send-blueprint', methods=['POST'])
def send_blueprint():
    data = request.get_json()
    recipient_email = data.get('email')

    if not recipient_email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    # 1. Create the Email
    message = MIMEMultipart()
    message["From"] = f"Yanex Square <{SENDER_EMAIL}>"
    message["To"] = recipient_email
    message["Subject"] = "Your 2026 Sovereign Wealth Blueprint"

    body = f"""
    Welcome to the Yanex Square Ecosystem.
    
    You have successfully requested the 2026 AI Wealth Stack. 
    This is your first step toward engineering sovereign wealth.
    
    Access your blueprint here: https://drive.google.com/file/d/1_XX0BxdzClc-phVnGs1Oe5Xkk_gLJYuS/view?usp=sharing
    
    Regards,
    The Yanex System Agent
    """
    message.attach(MIMEText(body, "plain"))

    try:
        # 2. Send the Email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        
        # 3. Log the Lead
        log_lead(recipient_email)
        
        return jsonify({"status": "success", "message": "Blueprint delivered"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)