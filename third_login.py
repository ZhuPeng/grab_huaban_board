#! encoding: utf-8
import time
LOGIN_URL = 'http://login.meiwu.co/login'
OPTIONS = {
    "QQ 登录": 'qq',
    "Weibo 登录": 'weibo',
    "微信": 'wechat',
}


def login(logintype, driver=None, interval=3):
    if driver is None:
        from selenium import webdriver
        driver = webdriver.Chrome()
    driver.get(LOGIN_URL)
    time.sleep(interval)
    weibo = driver.find_element_by_class_name(OPTIONS[logintype])
    weibo.click()
    print 'Current url:', driver.current_url
    while True:
        print 'Current url:', driver.current_url
        if u'画板' in driver.page_source and u'采集' in driver.page_source:
            break
        time.sleep(interval)

    cookies = driver.get_cookies()
    return driver.current_url, cookies

if __name__ == '__main__':
    login('qq')
