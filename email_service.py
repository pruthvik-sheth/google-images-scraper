import smtplib
from email_details import email, email_to, password

def send_email(message):
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com',587)
        smtp_object.ehlo()
        smtp_object.starttls()

        smtp_object.login(email,password)

        from_address = email
        to_address = email_to
        subject = "Scraping images updates!!"
        msg = "Subject: " + subject + '\n' + message
        smtp_object.sendmail(from_address,to_address,msg)

        smtp_object.quit()

    except Exception as e:
        print("Error while sending email!")