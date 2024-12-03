from email.message import EmailMessage
import smtplib

EMAIL = "Enter you mail OR Path "
PASSWORD = "passkey"


def send_emails(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    email1 = input("email: \n")
    sub = input("subject: \n")
    mess = input("mess: \n")
    send_emails(email1,sub,mess)