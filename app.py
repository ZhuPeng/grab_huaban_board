# -*- coding: utf8 -*-
import wx
import thread
import grab_huaban_board

passwd_file = 'password.conf'


def read_input():
    with open(passwd_file) as f:
        l = [x.strip() for x in f.readlines()]
        return l[0] if len(l) > 0 else '', l[1] if len(l) > 1 else '', l[2] if len(l) > 2 else ''
    return '', '', ''


def save_file(*args):
    raw = open(passwd_file, "r+")
    raw.seek(0)
    raw.truncate()
    for a in args:
        raw.write(a + '\n')


def main():
    def sync(event):
        usertext = user.GetValue()
        passwdtext = passwd.GetValue()
        huabanusertext = huabanuser.GetValue()
        save_file(usertext, passwdtext, huabanusertext)
        grab_huaban_board.windows_sender = content_text
        thread.start_new_thread(grab_huaban_board.execute, (usertext, passwdtext, huabanusertext))

    app = wx.App()
    width = 800
    frame = wx.Frame(None, title="Gui Test Editor", pos=(80, 80), size=(width, width))
    wx.StaticText(frame, -1, "用户名：", pos=(5, 5))
    user = wx.TextCtrl(frame, pos=(80, 5), size=(250, 24))

    wx.StaticText(frame, -1, "密码：", pos=(5, 40))
    passwd = wx.TextCtrl(frame, pos=(80, 40), size=(250, 24))

    wx.StaticText(frame, -1, "花瓣用户名：", pos=(5, 80))
    huabanuser = wx.TextCtrl(frame, pos=(80, 80), size=(250, 24))
    u, p, h = read_input()
    user.write(u)
    passwd.write(p)
    huabanuser.write(h)

    sync_button = wx.Button(frame, label="开始备份", pos=(5, 120), size=(100, 50))
    sync_button.Bind(wx.EVT_BUTTON, sync)
    content_text = wx.TextCtrl(frame, pos=(5, 160), size=(width, width-200), style=wx.TE_MULTILINE)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
