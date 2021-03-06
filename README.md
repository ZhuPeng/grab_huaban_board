# grab_huaban_board
批量下载花瓣网画板、堆糖网专辑


## 解析

* 查看analyze.txt


## 使用

```
git clone https://github.com/staugur/grab_huaban_board
cd grab_huaban_board
```

### for Python

1. pip install requests

2. python grab_huaban_board.py

```
usage: grab_huaban_board.py [-h] [-a ACTION] [-u USER] [-p PASSWORD] [-v]
                            [--board_id BOARD_ID] [--user_id USER_ID]

optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        脚本动作 -> 1. getBoard: 抓取单画板(默认);
                        2. getUser: 抓取单用户
  -u USER, --user USER  花瓣网账号-手机/邮箱
  -p PASSWORD, --password PASSWORD
                        花瓣网账号对应密码
  -v, --version         查看版本号
  --board_id BOARD_ID   花瓣网单个画板id, action=getBoard时使用
  --user_id USER_ID     花瓣网单个用户id, action=getUser时使用
```

* 详细使用文档请参考: [https://blog.saintic.com/blog/204.html](https://blog.saintic.com/blog/204.html "https://blog.saintic.com/blog/204.html")


### for JavaScript(花瓣、堆糖)

* 详细使用文档请参考：[https://blog.saintic.com/blog/256.html](https://blog.saintic.com/blog/256.html "https://blog.saintic.com/blog/256.html")

* 花瓣网下载脚本主页及安装地址：[请点击我](https://greasyfork.org/zh-CN/scripts/368427-%E8%8A%B1%E7%93%A3%E7%BD%91%E4%B8%8B%E8%BD%BD "请点击我")

* 堆糖网下载脚本主页及安装地址：[请点击我](https://greasyfork.org/zh-CN/scripts/369842-%E5%A0%86%E7%B3%96%E7%BD%91%E4%B8%8B%E8%BD%BD "请点击我")


## TODO

*for grab_huaban_board.py*

1. --board_ids 多画板
2. --user_ids 多用户
3. --igonre 指定忽略画板

*for grab_huaban_board.js*

1. 彩蛋-发送SMS
2. 公告显示
3. 按钮置灰
点击下载的次数越多
抓取的数量越少
有的抓取了几张后下载自动停止
4. 把画板或用户额外信息写入README.txt

## 简单备份花瓣指南
[简单备份花瓣指南](花瓣备份指南.md)
