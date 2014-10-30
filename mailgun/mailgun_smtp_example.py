# Example of using mailgun.com to send
# email via SMTP. Sign up for a mailgun
# account to provide your own crediantals
# 
# example:
# python mailgun_example.py -e mailgun_test@mailinator.com -f postmaster@samples.mailgun.org -l postmaster@samples.mailgun.org -p 3kh9umujora5

import smtplib
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--toEmail', default='mailgun_test@mailinator.com')
parser.add_argument('-f', '--fromEmail', default='postmaster@samples.mailgun.org')
parser.add_argument('-l', '--loginSmtp', default='postmaster@samples.mailgun.org')
parser.add_argument('-p', '--passwordSmtp', default='3kh9umujora5')
args = parser.parse_args()


def send_message_via_smtp(email, subject, message):
    global args
    msg = "Subject: "+ subject + "\n" + message
    smtp = smtplib.SMTP("smtp.mailgun.org", 587)
    smtp.login(args.loginSmtp, args.passwordSmtp)
    smtp.sendmail(args.fromEmail, email, msg)
    smtp.quit()

send_message_via_smtp(args.toEmail, "Test Subject" + str(datetime.datetime.now()), "Test body" + str(datetime.datetime.now()) )
