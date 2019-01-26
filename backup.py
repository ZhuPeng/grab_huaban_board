#!/usr/bin/env pythonw
# -*- coding: utf8 -*-
import wx
import thread
import time
from grab_huaban_board import execute, MESSAGE_QUEUE
passwd_file = 'password.conf'
sync_flag = False


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
        save_file(usertext, passwdtext)
        def _sync():
            global sync_flag
            sync_flag = True
            MESSAGE_QUEUE.put("开始同步...")
            execute(usertext, passwdtext)
            MESSAGE_QUEUE.put("同步完成")
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

    frame.Show()
    app.MainLoop()

if __name__ == '__main__' : main()
