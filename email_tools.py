from contextlib import contextmanager
import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import Settings


@contextmanager
def smtp_server():
    s = smtplib.SMTP(Settings.SMTP_HOST, Settings.SMTP_PORT)
    s.starttls()
    s.login(Settings.SMTP_USERNAME, Settings.SMTP_PASSWORD)
    yield s
    s.quit()


def send_email(s, sender, msg_subject, html_content):
    msg = MIMEMultipart()
    recipients = [Settings.SMTP_USERNAME]
    msg['Subject'] = msg_subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    part_html = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(part_html)

    try:
        if not Settings.DRY_RUN:
            s.sendmail(msg['From'], recipients, msg.as_string())
        logging.info('sent email to "%s" about "%s"' % (recipients, msg_subject))

    except Exception as e:
        logging.error('An error occurred while sending email: %s - %s' % (e.__class__, e))
        logging.debug(u'email:\n%s' % html_content)
        raise
