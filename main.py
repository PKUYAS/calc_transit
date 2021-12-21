from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from argparse import ArgumentParser
import smtplib
from email.mime.text import MIMEText

LAT = 39.99149 #纬度
LON = 116.30812 #经度
ALT = 50 #海拔
DAY = 7 #需要获取多少天以内的信息
DIS = 50

if __name__=="__main__":

    nowBJtime = datetime.utcnow()+timedelta(hours=8)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options,executable_path='/usr/bin/chromedriver',service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])

    print('Getting the main page...')
    driver.get("https://transit-finder.com/")



    form_lat = driver.find_element_by_id("form_lat")
    form_lon = driver.find_element_by_id("form_lon")
    form_elev = driver.find_element_by_id("form_elev")
    form_lat.send_keys(LAT)
    form_lon.send_keys(LON)
    form_elev.send_keys(ALT)


    
    form_elev.send_keys(Keys.RETURN)


    soup = BeautifulSoup(driver.page_source, features='lxml')
    for br in soup.find_all("br"):
        br.replace_with("\n")


    driver.close()


    events = soup.find(id="results").find_all("div","result")


    event_list = []
    sun_transit = 0
    moon_transit = 0
    for event in events:
        paras = event.find_all("p")
        space_station_name = paras[0].get_text() #飞行器名字
        if "Hubble" in space_station_name:
            continue
        time_list = paras[1].get_text().split(",")
        date = time_list[0].split()[1]
        time = time_list[1].split("•")[0].strip()
        date_time = datetime.fromisoformat("{} {}0".format(date, time)) #datetime对象
        date_time = date_time + timedelta(hours=8)
        if date_time - nowBJtime > timedelta(days=7):
            continue
        transit_type = time_list[1].split("•")[1].strip() #事件类型
        is_sun = 1 if "Sun" in transit_type else 0 #太阳=1，月亮=0
        is_transit = 1 if "transit" in transit_type else 0 #相交=1，不相交=0
        if is_sun:
            if is_transit:
                type_str = "凌日"
            else:
                type_str = "接近太阳"
        else:
            if is_transit:
                type_str = "凌月"
            else:
                type_str = "接近月亮"
        if is_transit:
            sun_transit += is_sun
            moon_transit += (1-is_sun)
        content1 = paras[2].get_text()
        content2 = paras[3].get_text()
        content = '''
        {} {}{}
        详细信息:
        {}
        {}
        ----------------------------
        '''.format(date_time.isoformat(sep=" ", timespec="milliseconds"), "国际空间站" if "ISS" in space_station_name else "中国空间站", type_str, content1, content2 )
        event_list.append({"space_station_name": space_station_name, "date_time": date_time, "is_sun":is_sun, "is_transit":is_transit, "content":content})


    today_str = "{}年{}月{}日".format(nowBJtime.year, nowBJtime.month, nowBJtime.day)
    title = "{} 未来一周空间站五可见凌日凌月".format(today_str)
    if sun_transit>0 and moon_transit>0:
        title = "{} 未来一周空间站凌日{}次，凌月{}次".format(today_str, sun_transit, moon_transit)
    if sun_transit==0 and moon_transit>0:
        title = "{} 未来一周空间站凌月{}次".format(today_str, moon_transit)
    if moon_transit==0 and sun_transit>0:
        title = "{} 未来一周空间站凌日{}次".format(today_str, sun_transit)


    mail_content = "".join([x["content"] for x in event_list])


    parser = ArgumentParser()
    parser.add_argument('--USERNAME', type=str)
    parser.add_argument('--PASSWORD', type=str)
    argconf = parser.parse_args()
    mail_host = "smtp.126.com"
    mail_username = argconf.USERNAME
    mail_password = argconf.PASSWORD
    sender = argconf.USERNAME
    receivers = [argconf.USERNAME]

    message = MIMEText(mail_content,'plain','utf-8')
    message['Subject'] = title
    message['From'] = sender
    message['To'] = receivers[0]

    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_username,mail_password) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误



