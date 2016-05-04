import smtplib
import dbmanager
import HTML
import time

from smtpd import SMTPServer

from email.mime.text import MIMEText
##list = ['heechul78@gmail.com', 'allautomatics@gmail.com', 'single2malt@gmail.com', 'jwkim@trizcorp.com', 'jyshin@trizcorp.com', 'dayduck@naver.com']
list = ['dayduck@naver.com']

def send_words(textfile):
    msg = MIMEText(textfile, 'html')

    msg['Subject'] = 'Did you know these words?'
    me = 'Word Challenge'
    msg['From'] = me

    """s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()"""

    s = smtplib.SMTP("smtp.gmail.com",587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("heechul78@gmail.com", "slrtm978!#$")
    for you in list:
        msg['To'] = you
        s.sendmail(me, you, msg.as_string())
    s.quit()

def retrive_words():
    t = HTML.Table(header_row=['Word', 'Meaning', 'Frequency Rate'])
    for row in dbmanager.dbm.get_random_words(1, 1000, 5):
        t.rows.append([row[0], row[1], row[2]])

    return str(t)

if __name__ == "__main__":
    while True:
        ##htmlcode = '<!doctype html>\n' + '<meta charset="UTF-8">\n' + retrive_words()
        htmlcode = '<!doctype html>\n' + '<html lang="ko">\n'+ '<meta charset="UTF-8">\n' + retrive_words() + '\n</html>'
        print htmlcode.decode('utf-8').encode('utf-8')
        send_words(htmlcode)
        print('Email Sent : %d'%list.__len__())
        time.sleep(7200)

