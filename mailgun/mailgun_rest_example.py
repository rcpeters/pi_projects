# Example using restful mailgun service.
# You have ot install request:
#     sudo pip install requests
#
# http://documentation.mailgun.com/api-sending.html#examples
#
# example
# python mailgun_rest_example.py -u 'https://api.mailgun.net/v2/samples.mailgun.org/messages' -k '3kh9umujora5'

import argparse
import datetime
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--toEmail', default='mailgun_test@mailinator.com')
parser.add_argument('-f', '--fromEmail', default='Postmaster <postmaster@samples.mailgun.org>')
parser.add_argument('-u', '--url', default='https://api.mailgun.net/v2/samples.mailgun.org/messages')
parser.add_argument('-k', '--key', default='3kh9umujora5')
args = parser.parse_args()

def send_complex_message():
    global args
    return requests.post(
        args.url,
        auth=("api", args.key),
        files=[("attachment", open("cat.jpg"))],
        data={"from": args.fromEmail,
              "to": args.toEmail,
              "subject": "subject " + str(datetime.datetime.now()),
              "text": "Test",
              "html": "<html>test</html>"})

r = send_complex_message()
print r.text
