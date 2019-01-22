# TODO: implement the below
# http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email
import smtplib
import configparser
from email.message import EmailMessage


def send_email(msg):
    """
    This function sends an email to a specified email addresss.
    Details are taken from a user created config.ini file.
    :param msg: The message to be sent
    :return: None
    """

    # email addresses to be used
    config = configparser.ConfigParser()
    from_address = config["details"]["from address"]
    to_address = config["details"]["to address"]

    # Create the email to be sent
    email = EmailMessage()
    email.set_content(msg)
    email["Subject"] = "Dell Monitor price has changed"
    email["From"] = from_address
    email["To"] = to_address

    # Connect to hotmail servers and authenticate to send the email
    with smtplib.SMTP(host="smtp.live.com", port=587) as smtp:
        # smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_address, config["details"]["password"])
        smtp.send_message(email, from_address, to_address)
