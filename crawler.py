import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import base64
import json

IDENTIFY = 1  # 验证码输入方式:        1:看截图aa.png，手动输入     2:云打码
COOKIE_GETWAY = 0 # 0 代表从https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18) 获取cookie   # 1 代表从https://weibo.cn/login/获取Cookie
dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人


"""
输入你的微博账号和密码，可去淘宝买。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [
    {'no': 'jiadieyuso3319@163.com', 'psw': 'a123456'},
    {'no': 'shudieful3618@163.com', 'psw': 'a123456'},
]

def get_cookie_from_login_sina_com_cn(account, password):
    '''获取一个账号的cookie'''
    loginURL = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode("gbk")
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        logger.warning("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        return json.dumps(cookie)
    else:
        logger.warning("Failed!( Reason:%s )" % info["reason"])
        return ""


def getCookie(account, password):
    if COOKIE_GETWAY == 0:
        return get_cookie_from_login_sina_com_cn(account, password)
    elif COOKIE_GETWAY == 1:
        return get_cookie_from_weibo_cn(account, password)
    else:
        logger.error("COOKIT_GETWAY Error!")

if __name__ == "__main__":
    nick_name = ''
    password = ''
    print(getCookie(nick_name, password))