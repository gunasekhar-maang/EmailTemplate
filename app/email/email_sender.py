import aiosmtplib
from jinja2 import Environment, FileSystemLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.config import Config
from typing import List

# Load the email template
env = Environment(loader=FileSystemLoader("app/email/templates"))
template = env.get_template("email_template.html")

async def send_email(subject: str, to_email: str, message_body: str, attachments: List[str] = None):
    # Render the email template with the provided message body
    html_content = template.render(message=message_body.replace("\n", "<br />"))
    
    # Create the MIMEMultipart object for the email
    message = MIMEMultipart()
    message["From"] = f"Guna Sekhar Neeluri <{Config.FROM_EMAIL}>"
    message["To"] = to_email
    message["Subject"] = subject
    
    # Attach the HTML content
    message.attach(MIMEText(html_content, "html"))

    # Attach each file with a user-friendly name
    if attachments:
        for index, file_path in enumerate(attachments, start=1):
            with open(file_path, "rb") as file:
                file_content = MIMEApplication(file.read())
                # Set the attachment name as "attachment-1", "attachment-2", etc.
                file_content.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=f"attachment-{index}.{file_path.split('.')[-1]}"
                )
                message.attach(file_content)
    
    # Send the email
    await aiosmtplib.send(
        message,
        hostname=Config.SMTP_SERVER,
        port=Config.SMTP_PORT,
        username=Config.SMTP_USERNAME,
        password=Config.SMTP_PASSWORD,
        start_tls=True
    )
