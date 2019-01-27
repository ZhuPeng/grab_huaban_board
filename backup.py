#!/usr/bin/env pythonw
# -*- coding: utf8 -*-
import wx
import thread
import time
import os
import getpass
from grab_huaban_board import execute, MESSAGE_QUEUE, printcolor, makedir
passwd_file = 'password.conf'
sync_flag = False
user_name = getpass.getuser()
BASE_PATH = '/Users/%s/Documents/花瓣网备份/' % user_name


def exception_run(f):
    def wrapper(*args, **kws):
        try:
            return f(*args, **kws)
        except Exception as e:
            printcolor(os.getcwd() + ' 程序运行出错：' + str(e))
    return wrapper


@exception_run
def change_workspace():
    makedir(BASE_PATH)
    os.chdir(BASE_PATH)
    printcolor("更改工作目录到：" + BASE_PATH)
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
                if msg.startswith('Successful download for'):
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
        save_file(usertext, passwdtext)

        @exception_run
        def _sync():
            global sync_flag
            sync_flag = True
            MESSAGE_QUEUE.put("开始同步...")
            execute(usertext, passwdtext)
            MESSAGE_QUEUE.put("操作完成")
            sync_flag = False
        thread.start_new_thread(_sync, ())
        # thread.start_new_thread(test_msg, ())

    app = wx.App()
    width = 800
    frame = wx.Frame(None, title="花瓣本地备份", pos=(80, 80), size=(width, width))
    wx.StaticText(frame, -1, "用户名：", pos=(5, 10))
    user = wx.TextCtrl(frame, pos=(80, 10), size=(250, 24))

    wx.StaticText(frame, -1, "密码：", pos=(5, 40))
    passwd = wx.TextCtrl(frame, pos=(80, 40), size=(250, 24))

    u, p = read_input()
    user.write(u)
    passwd.write(p)

    sync_button = wx.Button(frame, label="开始备份", pos=(5, 80), size=(100, 50))
    sync_button.Bind(wx.EVT_BUTTON, sync)

    content_text = wx.TextCtrl(frame,  pos=(5, 120), size=(width, width-200), style=wx.TE_MULTILINE)
    thread.start_new_thread(sync_msg, (content_text, ))
    printcolor("当前执行目录：" + os.getcwd())

    frame.Show()
    app.MainLoop()

if __name__ == '__main__' : main()
