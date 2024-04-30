import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email Account Infos 
def sendmail(recepients, body):
    email_sender_account = "harunulukaya@gmail.com"
    email_sender_password = "fihz kdpc kgwi wayo "
    email_smtp_server = "smtp.gmail.com"
    email_smtp_port = 587
    # Email Content
    email_subject = "Very important message"

    # Convert file content to string
    body_content = body.read()
    body.close()  # Close the file after reading

    # login to email server
    server = smtplib.SMTP(email_smtp_server, email_smtp_port)
    server.starttls()
    server.login(email_sender_account, email_sender_password)
    for recipient in recepients:
        print(f"Sending email to {recipient}")
        message = MIMEMultipart("alternative")
        message['From'] = email_sender_account
        message['To'] = recipient
        message['Subject'] = email_subject
        message.attach(MIMEText(body_content, 'html'))
        text = message.as_string()
        server.sendmail(email_sender_account, recipient, text)

    server.quit()

if __name__=="__main__":
    recipients = ["harunulukaya@gmail.com"]
    with open("_04_25_2024_updated.csv", "r",encoding="utf-8") as f:
        sendmail(recipients, body=f)
