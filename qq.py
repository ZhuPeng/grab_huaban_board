#! encoding: utf-8
import time
from selenium import webdriver
import urllib
import wx
from cStringIO import StringIO

def get_qrcode():
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=716027609&e=2&l=M&s=3&d=72&v=4&t=0.38620931174474316&daid=383&pt_3rd_aid=100240394'

    try:
        fp = urllib.urlopen(url)
        data = fp.read()
        fp.close()
        return wx.ImageFromStream(StringIO(data))
    except Exception as e:
        print str(e)
    return wx.Image(240,240)


def login(login_url, login_name, login_passwd, interval=3):
    driver = webdriver.Chrome()
    driver.get(login_url)
    time.sleep(interval)
    driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.frame("ptlogin_iframe")  # iframe必须逐级切入
    switch = driver.find_element_by_xpath('//*[@id="switcher_plogin"]')
    switch.click()
    time.sleep(interval)

    account = driver.find_element_by_id('u')
    password = driver.find_element_by_id('p')
    account.clear()
    password.clear()
    account.send_keys(login_name)
    time.sleep(interval)
    password.send_keys(login_passwd)
    time.sleep(interval)

    submit = driver.find_element_by_id('login_button')
    submit.click()
    time.sleep(interval)

    cookies = driver.get_cookies()
    time.sleep(30)
    driver.close()
    return cookies

if __name__ == '__main__':
    url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&client_id=100240394&response_type=code&redirect_uri=http://login.meiwu.co/oauth/callback&scope=get_user_info,add_topic,get_info,get_fanslist,get_idolist,add_idol,check_page_fans'
    name = ""
    password = ""
    cookies = login(url, name, password)
    print(cookies)