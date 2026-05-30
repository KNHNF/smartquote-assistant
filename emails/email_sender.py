import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body, sender_email, sender_password):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [to_email], msg.as_string())
        return "Email sent successfully."
    except Exception as e:
        return f"Email sending failed: {e}"
