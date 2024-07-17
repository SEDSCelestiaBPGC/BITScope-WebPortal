#This script is used to send emails to the users who have requested for the images of celestial objects.

#Importing the required libraries, variables and connecting to the database
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
load_dotenv()
db_host = os.getenv('DB_HOST')
db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('DB_NAME')
sender_email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

#function to send email
def send_email(recipient_email, subject, body_html):
    message = MIMEMultipart("alternative")
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message['Content-Type'] = 'text/html'
    message.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

    print("Email sent successfully")


#Fetching the data from the database and sending all the emails with a captured status and updating the status of the request in the database.
cursor.execute("""
    SELECT id, name, obj, email 
    FROM data 
    WHERE status = 'captured'
""")
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
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto; padding: 20px; background-color: #00000007;">
        <div style="background-color: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);">
            <div style="text-align: center; margin-bottom: 0px;">
                <!-- Replace with your actual logo -->
                <img src="https://lh3.googleusercontent.com/drive-viewer/AKGpihZ6wjWmyaaLQpSyf2raB4wysmIuAgDdzk-D65ct5TDTgy5hMfp9adGDRWReK3ln0NuXqomomBkCVzoxKEBB8ze_wVFLXReh8F8=s1600-rw-v1" alt="SEDS Celestia Logo" style="max-width: 150px;">
            </div>
            
            <h1 style="color: #000000; border-bottom: 2px solid #000000; padding-bottom: 10px; margin-top: 10px; margin-bottom: 30px;">Your Astronomy Images Are Here!</h1>
            
            <p>Dear {name},</p>
            
            <p>We hope this email finds you well and full of wonder for the cosmos. We're thrilled to deliver your requested astronomy image of <strong>{obj}</strong>. This captivating view of the universe is now yours to explore and enjoy.</p>
            
            <p>You'll find the following attached to this email:</p>
            <ul>
                <li>{obj} - CCD Camera Image 4032 x 2268</li>
            </ul>
            
            <p>We hope this image inspires your curiosity and deepens your appreciation for the vastness and beauty of our universe. If you would like to order more, <a href="https://www.bitscope-observatory.com" style="color: #1a237e; text-decoration: underline;">click here</a>. if you have any doubts or issues feel free to <a href="mailto:contact@bitscope-observatory.com" style="color: #1a237e; text-decoration: underline;">mail us</a>.</p>
            
            <p>Thank you for choosing BITScope for your astronomical journey!</p>
            
            <p>Clear skies,<br>The BITScope Team@SEDS Celestia</p>
            
            <div style="text-align: center; margin-top: 30px; font-size: 0.9em; color: #666;">
                <p>BITScope | SEDS Cestia | BITS Goa | Exploring the Universe, One Image at a Time<br>
                <p><a href="https://www.instagram.com/sedscelestia/" style="color: #1a237e;">Instagram</a> | <a href="https://www.bitscope-observatory.com" style="color: #1a237e;">www.bitscope-observatory.com</a></p>
            </div> 
        </div>
    </body>
    </html>
    """
    send_email(recipient_email, subject, body_html)
    cursor.execute("""
        UPDATE data 
        SET status = 'mailed' 
        WHERE id = %s
    """, (id,))
    conn.commit()

    
cursor.close()
conn.close()