import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sqlite3
conn = sqlite3.connect('databasemailer.db')
cursor = conn.cursor()

load_dotenv("../env")
sender_email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

def send_email(recipient_email, subject, body_html):
    message = MIMEMultipart("alternative")
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message['Content-Type'] = 'text/html'
    message.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

    print("Email sent successfully")

cursor.execute("SELECT id, name, obj, email FROM data WHERE id=?", (5,))
rows  = cursor.fetchall()
for row in rows:
    id, name, obj, recipient_email = row
    print (name)
    print(obj)
    print(recipient_email) 
    print(id)

subject = f"Test Email| Order ID:{id}"
body_html = f"""\
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your BITScope Astronomy Images</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f0f5ff;">
    <div style="background-color: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);">
        <div style="text-align: center; margin-bottom: 20px;">
            <!-- Replace with your actual logo -->
            <img src="https://example.com/bitscope-logo.png" alt="BITScope Observatory Logo" style="max-width: 150px;">
        </div>
        
        <h1 style="color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 10px;">Your Astronomy Images Are Here!</h1>
        
        <p>Dear {name},</p>
        
        <p>We hope this email finds you well and full of wonder for the cosmos. We're thrilled to deliver your requested astronomy images of <strong>{obj}</strong>. These captivating views of the universe are now yours to explore and enjoy.</p>
        
        <p>You'll find the following attached to this email:</p>
        <ul>
            <li>{obj} - High Resolution Image</li>
            <li>{obj} - Wide Field View</li>
            <li>{obj} - Detailed Information Sheet</li>
        </ul>
        
        <p>We hope these images inspire your curiosity and deepen your appreciation for the vastness and beauty of our universe. If you have any questions about your images or would like to order more, please don't hesitate to contact us.</p>
        
        <p>Thank you for choosing BITScope Observatory for your astronomical journey!</p>
        
        <p>Clear skies,<br>The BITScope Team</p>
        
        <div style="text-align: center; margin-top: 30px; font-size: 0.9em; color: #666;">
            <p>BITScope Observatory | Exploring the Universe, One Image at a Time<br>
            <a href="https://www.bitscope-observatory.com" style="color: #1a237e;">www.bitscope-observatory.com</a></p>
        </div>
    </div>
</body>
</html>
"""

send_email(recipient_email, subject, body_html)