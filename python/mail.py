import yagmail
from email.mime.text import MIMEText
from operator import truth

import time

def OR(*args):
    expression = ' or '.join(['{}'.format(k) for k in args])
    expression = 'truth({})'.format(expression)
    return eval(expression)
def email(dir):
    yag = yagmail.SMTP(user = 'xxxx@xxx.xxx', password = 'xxxxxxx', host = 'smtp.exmail.qq.com')
    subject = "This is a test"
    mes = "定时测试，当前时间：%s"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    file = "文件路径"
    content = []
    content.append(file)
    receiver = ["xxxxx@qq.com","xxxx@outlook.com","xxxxx@126.com"]
    yag.send(to=receiver,subject=subject,attachments=content,contents=mes)
    yag.close()