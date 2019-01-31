#! encoding: utf-8
import time
from selenium import webdriver
import urllib
import wx
from cStringIO import StringIO
QRCODE_URL = ''
LOGIN_URL = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&client_id=100240394&response_type=code&redirect_uri=http://login.meiwu.co/oauth/callback&scope=get_user_info,add_topic,get_info,get_fanslist,get_idolist,add_idol,check_page_fans'
EMPTYIMAGE = wx.Image(100, 100)


def get_qrcode():
    if QRCODE_URL == '':
        return EMPTYIMAGE

    try:
        fp = urllib.urlopen(QRCODE_URL)
        data = fp.read()
        fp.close()
        return wx.Image(StringIO(data))
    except Exception as e:
        print str(e)
    return EMPTYIMAGE


def login(login_url=LOGIN_URL, interval=5):
    driver = webdriver.Chrome()
    driver.get(login_url)
    driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.frame("ptlogin_iframe")  # iframe必须逐级切入

    while True:
        try:
            qrcode = driver.find_element_by_id('qrlogin_img')
            tmp = qrcode.get_attribute("src")
            global QRCODE_URL
            if tmp != '' and tmp != QRCODE_URL:
                print 'qrcode url change: ' + tmp
                QRCODE_URL = tmp
        except Exception as e:
            print str(e)
        # check if qrcode scan
        print u"当前网页：" + driver.title + " => " + driver.current_url
        time.sleep(interval)
    return cookies

if __name__ == '__main__':
    url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&client_id=100240394&response_type=code&redirect_uri=http://login.meiwu.co/oauth/callback&scope=get_user_info,add_topic,get_info,get_fanslist,get_idolist,add_idol,check_page_fans'
    cookies = login(url)
    print(cookies)
