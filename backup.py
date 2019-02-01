#!/usr/bin/env pythonw
# -*- coding: utf8 -*-
import wx
import thread
import time
import os
import sys
import getpass
from grab_huaban_board import execute, MESSAGE_QUEUE, printcolor, makedir, \
    update_cookies, getUserAction
import third_login
from selenium import webdriver
runtime_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
printcolor("当前运行目录：" + runtime_dir)
passwd_file = 'password.conf'
sync_flag = False
user_name = getpass.getuser()
BASE_PATH = '/Users/%s/Documents/花瓣网备份/' % user_name
DRIVER = None


def exception_run(f):
    def wrapper(*args, **kws):
        try:
            return f(*args, **kws)
        except Exception as e:
            printcolor(os.getcwd() + ' 程序运行出错：' + str(e))
    return wrapper


@exception_run
def run_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    DRIVER = webdriver.Chrome(executable_path=os.path.join(runtime_dir, "./chromedriver"), chrome_options=chrome_options)


@exception_run
def change_workspace():
    makedir(BASE_PATH)
    os.chdir(BASE_PATH)
    printcolor("图片备份目录：文稿 => 花瓣网备份")
change_workspace()


def read_input():
    try:
        return _read_input()
    except:
        return '', ''


def _read_input():
    with open(passwd_file) as f:
        l = [x.strip() for x in f.readlines()]
        return l[0] if len(l) > 0 else '', l[1] if len(l) > 1 else ''
    return '', ''


@exception_run
def save_file(*args):
    raw = open(passwd_file, "w+")
    raw.seek(0)
    raw.truncate()
    for a in args:
        raw.write(a + '\n')


def main():
    def sync_msg(sender):
        while True:
            try:
                msg = MESSAGE_QUEUE.get() + '\n'
                if msg.startswith('Successful download for') or msg.startswith('ajax load ') or \
                        msg.startswith('Current board '):
                    continue
                sender.write(msg)
                time.sleep(0.2)
            except:
                pass

    def test_msg():
        while True:
            MESSAGE_QUEUE.put('xxx'*10)
            time.sleep(0.2)

    def sync(event):
        if sync_flag:
            MESSAGE_QUEUE.put("正在同步，请等待成功后再试")
            return
        usertext = user.GetValue()
        passwdtext = passwd.GetValue()
        MESSAGE_QUEUE.put("读取用户名和密码")
        selectOpt = chooseScoreChoice.GetCurrentSelection()
        save_file(usertext, passwdtext)
        printcolor("当前登录方式：" + options[selectOpt])
        action = execute

        def third_action(u, p):
            printcolor(options[selectOpt] + " 方式耗时较长，请耐心等待一下")
            cururl, cookies = third_login.login(options[selectOpt], driver=DRIVER)
            update_cookies(cookies)
            getUserAction(cururl)

        if options[selectOpt] in third_login.OPTIONS:
            action = third_action

        @exception_run
        def _sync():
            global sync_flag
            sync_flag = True
            MESSAGE_QUEUE.put("开始同步...")
            change_workspace()
            action(usertext, passwdtext)
            MESSAGE_QUEUE.put("操作完成，图片备份目录：文稿 => 花瓣网备份")
            sync_flag = False
        thread.start_new_thread(_sync, ())
        # thread.start_new_thread(test_msg, ())

    def chooseScoreFunc(event):
        index = event.GetEventObject().GetSelection()
        scoreChoosed = options[index]
        printcolor("选择登录方式：" + scoreChoosed)
        selectOpt = index
        if scoreChoosed in third_login.OPTIONS:
            thread.start_new_thread(sync, (event, ))

    app = wx.App()
    width = 800
    gap = 50
    current = 10
    tipCtrlGap = 100
    left_margin = 5

    frame = wx.Frame(None, title="花瓣本地备份", pos=(80, 80), size=(width, width))

    options = ['普通登录']
    options.extend(third_login.OPTIONS.keys())
    wx.StaticText(frame, -1, "登录方式：", pos=(left_margin, current))
    chooseScoreChoice = wx.Choice(frame, -1, choices=options, pos=(tipCtrlGap, current), size=(250, 30))
    frame.Bind(wx.EVT_CHOICE, chooseScoreFunc, chooseScoreChoice)
    chooseScoreChoice.SetSelection(0)
    current += gap

    userTip = wx.StaticText(frame, -1, "用户名：", pos=(left_margin, current))
    user = wx.TextCtrl(frame, pos=(tipCtrlGap, current), size=(250, 24))
    current += gap

    passwdTip = wx.StaticText(frame, -1, "密码：", pos=(left_margin, current))
    passwd = wx.TextCtrl(frame, pos=(tipCtrlGap, current), size=(250, 24))
    current += gap

    u, p = read_input()
    user.write(u)
    passwd.write(p)

    sync_button = wx.Button(frame, label="开始备份", pos=(left_margin, current), size=(100, 50))
    sync_button.Bind(wx.EVT_BUTTON, sync)
    current += gap

    content_text = wx.TextCtrl(frame,  pos=(left_margin, current), size=(width, width-200), style=wx.TE_MULTILINE)
    thread.start_new_thread(sync_msg, (content_text, ))
    thread.start_new_thread(run_browser, ())

    frame.Show()
    app.MainLoop()

if __name__ == '__main__' : main()
