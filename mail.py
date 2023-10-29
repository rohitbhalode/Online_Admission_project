import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyotp

def send_otp(email):
    # Generate a new secret key for the user (store this securely)
    
    secret_key = pyotp.random_base32()
    print('email.',email)
    # Create a TOTP instance (Time-based OTP)
    totp = pyotp.TOTP(secret_key)

    # Generate the OTP (typically done on the server)
    otp = totp.now()
    print(otp)
    
    # Send the OTP to the user via email, SMS, or another method


    message="Your OTP:"+ str(otp)

    msg = MIMEMultipart()
    
    # Set the sender, recipient, and subject
    msg['From'] = "rohitbhalode@gmail.com"
    msg['To'] = email
    msg['Subject'] = "This is system generated code"
    
    # Add the message body
    msg.attach(MIMEText(message, 'plain'))
    
    # Create an SMTP connection
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start the TLS encryption
        server.starttls()
        
        # Login to the email account
        server.login("rohitbhalode@gmail.com", 'tzdfsoqlvyuvwvcm')
         
        
        # Send the email
        server.send_message(msg)

    return otp