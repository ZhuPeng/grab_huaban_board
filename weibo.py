#! encoding: utf-8
import time
from selenium import webdriver
LOGIN_URL = 'http://login.meiwu.co/login'


def login(login_name, login_passwd, interval=3):
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)
    time.sleep(interval)
    weibo = driver.find_element_by_class_name('weibo')
    weibo.click()

    account = driver.find_element_by_id('userId')
    password = driver.find_element_by_id('passwd')
    account.clear()
    password.clear()
    account.send_keys(login_name)
    password.send_keys(login_passwd)

    submit = driver.find_element_by_class_name('WB_btn_login')
    submit.click()
    time.sleep(interval)

    driver.get('http://login.meiwu.co/')
    cookies = driver.get_cookies()
    print driver.title, driver.current_url, cookies
    time.sleep(30)
    driver.close()
    return cookies

if __name__ == '__main__':
    name = ""
    password = ""
    cookies = login(name, password)
    print(cookies)
