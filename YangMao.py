import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

"""
https://zhuanlan.zhihu.com/p/397792864
"""

def get_content():
     url = 'https://ym.today/yangmao'
     ret = requests.get(url)
     test = ret.text
     comments = []
     soup = BeautifulSoup(test, 'lxml')
     liTags = soup.find_all('li', attrs={'class': 'grid-item post-list-item'})
     for li in liTags:
          comment = {}
          try:
               comment['content'] = li.find('a').text.strip()

               comment['URL'] = li.find('a')['href']
               comment['time'] = li.find('time')['datetime']
               comments.append(comment)
          except:
               print('出了点小问题')

     return comments


def Out2File(dict):
    df = pd.DataFrame()
    list_content = []
    list_url = []
    list_time = []
    for comment in dict:
        list_content.append(comment['content'])
        list_url.append(comment['URL'])
        list_time.append(comment['time'])
    df['content'] = list_content
    df['url'] = list_url
    df['time'] = list_time
    df = df.head(6)
    df.to_csv('羊毛.csv', index=False)  # 输出为csv文本格式
    return df


def email():
     df = pd.read_csv('羊毛.csv')
     number = ''
     smtp = ''
     to = ''  # 可以是非QQ的邮箱
     mer = MIMEMultipart()
     # 设置邮件正文内容
     head = '''
    <p>羊毛最新信息</p>
    <p><a href="{}">{}--{}</a></p>
    <p>羊毛最新前五条信息</p>
    <p><a href="{}">{}--{}</a></p>
    <p><a href="{}">{}--{}</a></p>
    <p><a href="{}">{}--{}</a></p>
    <p><a href="{}">{}--{}</a></p>
    <p><a href="{}">{}--{}</a></p>
    '''.format(df.iloc[0, :]['url'], df.iloc[0, :]['content'],df.iloc[0, :]['time'],
               df.iloc[1, :]['url'], df.iloc[1, :]['content'],df.iloc[1, :]['time'],
               df.iloc[2, :]['url'], df.iloc[2, :]['content'],df.iloc[2, :]['time'],
               df.iloc[3, :]['url'], df.iloc[3, :]['content'],df.iloc[3, :]['time'],
               df.iloc[4, :]['url'], df.iloc[4, :]['content'],df.iloc[4, :]['time'],
               df.iloc[5, :]['url'], df.iloc[5, :]['content'],df.iloc[5, :]['time'])
     mer.attach(MIMEText(head, 'html', 'utf-8'))

     fujian = MIMEText(open('羊毛.csv', 'rb').read(), 'base64', 'utf-8')
     fujian["Content-Type"] = 'application/octet-stream'  # 附件内容
     fujian.add_header('Content-Disposition', 'file', filename=('utf-8', '', '羊毛.csv'))
     mer.attach(fujian)

     mer['Subject'] = '每日羊毛信息'  # 邮件主题
     mer['From'] = number  # 发送人
     mer['To'] = to  # 接收人

     # 5.发送邮件
     s = smtplib.SMTP_SSL('smtp.qq.com', 465)
     s.login(number, smtp)
     s.send_message(mer)  # 发送邮件
     s.quit()
     print('成功发送')


if __name__ == '__main__':

    schedule.every().day.at("19:21").do(email)
    while True:
         schedule.run_pending()
         time.sleep(5)
    content = get_content()
    data = Out2File(content)
    email(data)




