#!/usr/bin/env python
# -*- coding: utf8 -*-

__version__ = "5.0"
__author__  = "Mr.tao"
__doc__     = "https://www.saintic.com/blog/204.html"

import re, os, sys, json, logging, requests
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
import Queue
import json
import urlparse
reload(sys)
sys.setdefaultencoding('utf-8')
BASE_URL = 'http://login.meiwu.co'
AUTH_URL = BASE_URL + '/auth'

logging.basicConfig(level=logging.INFO,
                format='[ %(levelname)s ] %(asctime)s %(filename)s:%(threadName)s:%(process)d:%(lineno)d %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filemode='a')
debug = True
request = requests.Session()
request.verify = False
request.headers.update({'X-Request': 'JSON', 'X-Requested-With': 'XMLHttpRequest', 'Referer': BASE_URL, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'})
MESSAGE_QUEUE = Queue.Queue()


def update_cookies(cookies):
    for cookie in cookies:
        request.cookies.set(cookie['name'], cookie['value'])


def printcolor(msg, color=None):
    if color == "green":
        pmsg = '\033[92m{}\033[0m'.format(str(msg))
    elif color == "blue":
        pmsg = '\033[94m{}\033[0m'.format(str(msg))
    elif color == "yellow":
        pmsg = '\033[93m{}\033[0m'.format(str(msg))
    elif color == "red":
        pmsg = '\033[91m{}\033[0m'.format(str(msg))
    else:
        pmsg = str(msg)
    print pmsg
    MESSAGE_QUEUE.put(str(msg))


def rename(fr, to):
    if not os.path.exists(fr):
        return
    os.rename(fr, to)


def makedir(d):
    d = str(d)
    if not os.path.exists(d):
        os.makedirs(d)
    if os.path.exists(d):
        return True
    else:
        return False

def _post_login(email, password):
    """登录函数"""
    res = dict(success=False)
    url = BASE_URL + "/auth/"
    try:
        resp = request.post(url, data=dict(email=email, password=password), headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}).json()
    except Exception,e:
        logging.error(e, exc_info=True)
    else:
        # printcolor("_post_login: " + str(resp))
        if "user" in resp:
            # 登录成功
            res.update(success=True, data=resp["user"])
        else:
            res.update(resp)
    return res

def _download_img(pin, retry=True):
    """ 下载单个原图
    @param pin dict: pin的数据，要求： {'pin_id': xx, 'suffix': u'png|jpg|jpeg...', 'key': u'xxx-xx', 'board_id': xx}
    @param retry bool: 是否失败重试
    """
    if pin and isinstance(pin, dict) and "pin_id" in pin and "suffix" in pin and "key" in pin and "board_id" in pin:
        imgurl = "http://hbimg.b0.upaiyun.com/{}".format(pin["key"])
        imgdir = pin['board_id']
        imgname = os.path.join(imgdir, '{}.{}'.format(pin["pin_id"], pin["suffix"]))
        if os.path.isfile(imgname):
            return
        try:
            makedir(imgdir)
            req = request.get(imgurl)
            with open(imgname, 'wb') as fp:
                fp.write(req.content)
        except Exception,e:
            logging.warn(e, exc_info=True)
            if retry is True:
                _download_img(pin, False)
            else:
                printcolor("Failed download for {}".format(imgurl), "yellow")
        else:
            if debug:
                printcolor("Successful download for {}, save as {}".format(pin["pin_id"], imgname), "blue")

def _crawl_board(board_id):
    """ 获取画板下所有pin """
    if not board_id:
        return
    retry = limit = 100
    board_url = BASE_URL + '/boards/{}/'.format(board_id)
    try:
        #get first pin data
        r = request.get(board_url).json()
    except Exception,e:
        printcolor("Crawl first page error, board_id: {}".format(board_id), "yellow")
        logging.error(e, exc_info=True)
    else:
        if "board" in r:
            board_data = r["board"]
        else:
            printcolor(r.get("msg"))
            return
        printcolor("开始下载画板「{}」...".format(board_data['title']), "green")
        pin_number = board_data["pin_count"]
        board_pins = board_data["pins"]
        retry = 2 * pin_number / limit
        printcolor("Current board <{}> pins number is {}, first pins number is {}".format(board_id, pin_number, len(board_pins)), 'red')
        if len(board_pins) < pin_number:
            last_pin = board_pins[-1]['pin_id']
            while 1 <= retry:
                #get ajax pin data
                board_next_url = BASE_URL + "/boards/{}/?max={}&limit={}&wfl=1".format(board_id, last_pin, limit)
                try:
                    board_next_data = request.get(board_next_url).json()["board"]
                except Exception,e:
                    logging.error(e, exc_info=True)
                    continue
                else:
                    board_pins += board_next_data["pins"]
                    printcolor("ajax load board with pin_id {}, get pins number is {}, merged".format(last_pin, len(board_next_data["pins"])), "blue")
                    if len(board_next_data["pins"]) == 0:
                        break
                    last_pin = board_next_data["pins"][-1]["pin_id"]
                retry -= 1
        #map(lambda pin: dict(pin_id=pin['pin_id'], suffix=pin['file']['type'].split('/')[-1], key=pin['file']['key'], board_id=board_id), board_pins)
        board_pins = [ dict(pin_id=pin['pin_id'], suffix=pin['file']['type'].split('/')[-1], key=pin['file']['key'], board_id=board_id) for pin in board_pins ]
        pool = ThreadPool()
        pool.map(_download_img, board_pins)
        pool.close()
        pool.join()
        printcolor("画板「{}」下载完成".format(board_data['title']), "green")

def _crawl_user(user_id):
    """ 查询user的画板 """
    if not user_id:
        return

    if os.path.exists('重要文件勿删.json'):
        with open('重要文件勿删.json', 'r') as f:
            data = json.load(f)
            for b in data:
                rename(b['title'], str(b['board_id']))

    retry = limit = 5
    user_url = BASE_URL + "/{}".format(user_id)
    try:
        #get first board data
        r = request.get(user_url).json()
    except Exception,e:
        printcolor("Crawl first page error, user_id: {}".format(user_id), "yellow")
        logging.error(e, exc_info=True)
    else:
        if "user" in r:
            user_data = r["user"]
        else:
            printcolor(r.get("msg"))
            return
        board_number = int(user_data['board_count'])
        retry = 2 * board_number / limit
        board_ids = user_data['boards']
        printcolor("Current user <{}> boards number is {}, first boards number is {}".format(user_id, board_number, len(board_ids)), 'red')
        # printcolor("Current collect board ids: " + str([b['board_id'] for b in board_ids]))
        if len(board_ids) < board_number:
            last_board = user_data['boards'][-1]['board_id']
            while 1 <= retry:
                #get ajax pin data
                user_next_url = BASE_URL + "/{}?jhhft3as&max={}&limit={}&wfl=1".format(user_id, last_board, limit)
                try:
                    res = request.get(user_next_url).json()
                    user_next_data = res["user"]
                except Exception as e:
                    printcolor("异常: " + str(e) + " res: " + str(res))
                    logging.error(e, exc_info=True)
                    continue
                else:
                    board_ids += user_next_data["boards"]
                    printcolor("ajax load user with board_id {}, get boards number is {}, merged total {}".format(last_board, len(user_next_data["boards"]), len(board_ids)), "blue")
                    # printcolor("Current collect another board ids: " + str([b['board_id'] for b in user_next_data["boards"]]))
                    if len(user_next_data["boards"]) == 0:
                        break
                    last_board = user_next_data["boards"][-1]["board_id"]
                retry -= 1
        board_ids_list = map(str, [ board['board_id'] for board in board_ids ])

        with open('重要文件勿删.json', 'w') as f:
            json.dump(board_ids, f)
        # double check for json file delete
        for b in board_ids:
            rename(b['title'], str(b['board_id']))

        pool = ThreadPool()  #创建进程池
        pool.map(_crawl_board, board_ids_list) #board_ids：要处理的数据列表； _crawl_board：处理列表中数据的函数
        pool.close()#关闭进程池，不再接受新的进程
        pool.join()#主进程阻塞等待子进程的退出
        for b in board_ids:
            rename(str(b['board_id']), b['title'])
        printcolor("Current user {}, download over".format(user_id), "green")

def auth_login(user, password):
    if user and password:
        auth = _post_login(user, password)
        if not auth["success"]:
            return False, '登陆失败: ' + auth.get("msg", '')
        # for k, v in auth['data'].items():
        #     printcolor(str(k) + ": " + str(v))
        return True, auth['data']
    else:
        return False, "您未设置账号密码，将处于未登录状态，抓取的图片可能有限；设置账号密码后，图片抓取率可达99.99%！"

def main(args):
    if not args.action:
        parser.print_help()
        return
    action     = args.action or "getBoard"
    user       = args.user
    password   = args.password
    version    = args.version
    board_id   = args.board_id
    user_id    = args.user_id
    execute(user, password, user_id, board_id, action, version)


def execute(user, password, user_id=None, board_id=None, action=None, version=None):
    action = action or 'getUser'
    if version:
        printcolor("https://github.com/staugur/grab_huaban_board, v{}".format(__version__))
        return
    # 用户登录
    ok, msg = auth_login(user, password)
    if not ok:
        printcolor(msg)
        return
    printcolor("登陆成功")
    user_id = msg['urlname']

    # 主要动作-功能
    if action == "getBoard":
        # 抓取单画板
        if not board_id:
            printcolor("请设置board_id参数", "yellow")
            return
        makedir("boards")
        os.chdir("boards")
        _crawl_board(board_id)
    elif action == "getUser":
        getUserAction(user_id)
    else:
        parser.print_help()


def parse_user(user):
    if str(user).startswith('http://'):
        return urlparse.urlparse(user).path.strip('/')
    return user


def getUserAction(user_id):
    user_id = parse_user(user_id)
    printcolor("登陆后花瓣用户名：" + user_id)
    if not user_id:
        printcolor("请设置user_id参数", "yellow")
        return
    makedir(user_id)
    os.chdir(user_id)
    _crawl_user(user_id)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", help="脚本动作 -> 1. getBoard: 抓取单画板(默认); 2. getUser: 抓取单用户")
    parser.add_argument("-u", "--user", help="花瓣网账号-手机/邮箱")
    parser.add_argument("-p", "--password", help="花瓣网账号对应密码")
    parser.add_argument("-v", "--version", help="查看版本号", action='store_true')
    parser.add_argument("--board_id", help="花瓣网单个画板id, action=getBoard时使用")
    parser.add_argument("--user_id", help="花瓣网单个用户id, action=getUser时使用")
    args = parser.parse_args()
    main(args)
