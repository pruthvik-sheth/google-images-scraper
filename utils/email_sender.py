import smtplib

class EmailSender:

    def __init__(self, sender, receiver, sender_password, mail_server = "smtp.gmail.com") -> None:
        self.__sender = sender
        self.__receiver = receiver
        self.__sender_password = sender_password
        self.__mail_server = mail_server

    def send_email(self, subject = "Scraping Updates!", message = ""):
        try:
            smtp_object = smtplib.SMTP(self.__mail_server, 587)
            smtp_object.ehlo()
            smtp_object.starttls()

            smtp_object.login(self.__sender, self.__sender_password)

            from_address = self.__sender
            to_address = self.__receiver
            msg = "Subject: " + subject + '\n' + message
            smtp_object.sendmail(from_address, to_address,msg)
            smtp_object.quit()

        except Exception as e:
            print("Error while sending email!")