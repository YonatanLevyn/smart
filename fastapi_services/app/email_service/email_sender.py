import boto3
from botocore.exceptions import NoCredentialsError


# The function to send emails using Amazon SES
async def send_mail_with_ses(email: str, username: str):
    ses_client = boto3.client('ses') 
    SENDER = "johnlevhum@gmail.com"  
    RECIPIENT = email
    SUBJECT = "Welcome to Our Platform"
    BODY_TEXT = (f"Hello {username},\r\n"
                 "Welcome to our platform. We're glad you're here!")
    BODY_HTML = f"""<html>
    <head></head>
    <body>
      <h1>Hello {username},</h1>
      <p>Welcome to our platform. We're glad you're here!</p>
    </body>
    </html>"""

    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except NoCredentialsError as e:
        print(f"Credentials not available: {e}")
    except Exception as e:
        print(f"Error sending email: {e}")
