import logging
import os
import re
import smtplib
from bs4 import BeautifulSoup
import requests
from secrets import secrets

PATH = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=f'{PATH}/error.log', filemode='a', format='[%(asctime)s] %(message)s', datefmt='%y-%m-%d %H:%M:%S')

headers = {'user-agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'}
url = 'https://www.google.com/search?q=INDEXSP:.INX'
THRESHOLD = 0


def sendText(data):
    email = secrets['email']
    password = secrets['password']
    smtp = 'smtp.gmail.com'
    port = 587

    try:
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(email, password)

        sms_gate = secrets['to']
        body = f'S&P 500 Dropped\n{data}'

        server.sendmail(email, sms_gate, body)
        server.quit()
    except Exception:
        logging.exception('Exception was thrown in sending text')


if __name__ == '__main__':
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, features='lxml')
        data = soup.find('span', {'class': re.compile('WlRRw IsqQVc*')})
        if not data: raise ValueError
        if data.text.split(' ')[0][0] == '+' or data.text.split(' ')[0][0] == u'\u2212':
            if int(data.text.split(' ')[1].split('.')[0][-1]) >= THRESHOLD:
                sendText(data.text.replace(u'\u2212', '-'))
    except ValueError:
        logging.exception('Data returned None')
    except Exception:
        logging.exception('Exception was thrown')
