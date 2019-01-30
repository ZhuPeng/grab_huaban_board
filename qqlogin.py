#! encoding: utf-8
import time
from selenium import webdriver


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
    url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&client_id=100240394&response_type=code&redirect_uri=http%3A%2F%2Flogin.meiwu.co%2Foauth%2Fcallback&scope=get_user_info%2Cadd_topic%2Cget_info%2Cget_fanslist%2Cget_idolist%2Cadd_idol%2Ccheck_page_fans'
    name = ""
    password = ""
    cookies = login(url, name, password)
    print(cookies)
