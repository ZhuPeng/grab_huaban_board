#! encoding: utf-8
import time
LOGIN_URL = 'http://login.meiwu.co/login'
OPTION = "Weibo 登录"


def login(login_name, login_passwd, driver=None, interval=3):
    if driver is None:
        from selenium import webdriver
        driver = webdriver.Chrome()
    driver.get(LOGIN_URL)
    time.sleep(interval)
    weibo = driver.find_element_by_class_name('weibo')
    weibo.click()
    print 'Current url:', driver.current_url
    time.sleep(interval)

    account = driver.find_element_by_id('userId')
    password = driver.find_element_by_id('passwd')
    account.clear()
    password.clear()
    account.send_keys(login_name)
    time.sleep(interval)
    password.send_keys(login_passwd)
    time.sleep(interval)

    submit = driver.find_element_by_class_name('WB_btn_login')
    submit.click()
    time.sleep(interval)
    print 'Current url:', driver.current_url

    count = 5
    while count > 0:
        time.sleep(interval)
        driver.get('http://login.meiwu.co/')
        print 'Current url:', driver.current_url
        if '画板' in driver.page_source:
            break
        count -= 1
    else:
        raise Exception("未成功登录，请稍后再试")

    cookies = driver.get_cookies()
    return driver.current_url, cookies

if __name__ == '__main__':
    name = ""
    password = ""
    current_url, cookies = login(name, password)
    print current_url, cookies
