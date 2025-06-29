import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Set your email and app password here or load from .env
EMAIL_ADDRESS = 'pittalasandeep124@gmail.com'
EMAIL_PASSWORD = 'wdua pebe ilyq jxhr'

def send_email(to_email, subject, body, html_body=None, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if html_body:
        msg.attach(MIMEText(html_body, 'html'))

    if attachment_path:
        try:
            with open(attachment_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(img)
        except Exception as e:
            logging.warning(f"Attachment not added: {e}")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Email sending failed to {to_email}: {e}")
        return False