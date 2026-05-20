import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

def send_report_email(recipient_email: str, lead_name: str, pdf_path: str):
    """
    Safely connects to an SMTP server (like Gmail) and emails the 
    generated PDF report directly to the prospect.
    """
    # 1. Pull credentials safely from your hidden environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD") # This will be your Google App Password

    # Fallback/Safety Check: If email credentials aren't set up yet, don't crash!
    if not sender_email or not sender_password:
        print("[Email Service] Warning: Email credentials missing in .env. Skipping email delivery step.")
        print(f"[Email Service] Simulated: Email would have been sent to {recipient_email} with file {pdf_path}")
        return

    try:
        # 2. Setup the structured Email Header
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Your Personalized Business Optimization Audit Brief"

        # 3. Create a polite, professional Email Body
        body = f"""Hi {lead_name},

Thank you for requesting an intake audit via our automated gateway. 

Our system has finished analyzing public signals and digital properties tied to your organization. We have compiled our foundational optimization notes, technological considerations, and growth insights into a streamlined PDF document.

Please find your custom report attached to this email. 

Best regards,
The Automation Engine Team
"""
        msg.attach(MIMEText(body, 'plain'))

        # 4. Attach the generated PDF file safely
        # We read the file in binary mode ('rb') and encode it so it travels across the web cleanly
        with open(pdf_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(pdf_path)}",
            )
            msg.attach(part)

        # 5. Connect to Gmail's Secure SMTP Server and send
        print(f"[Email Service] Connecting to mail server to reach {recipient_email}...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() # Secure the connection with encryption
        server.login(sender_email, sender_password)
        
        # Convert the whole message setup into a string block and fire it off
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print(f"[Email Service] Success! Email delivered cleanly to {recipient_email}")

    except Exception as e:
        # Fallback if your internet drops or authentication fails
        print(f"[Email Service] Failed to send email due to an exception: {e}")