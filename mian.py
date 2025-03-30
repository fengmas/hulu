import hashlib
import json
import random
import time
import requests
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pytz import timezone
import os

# 修复时区为上海时区
def Shanghai(sec, what):
    tz = timezone('Asia/Shanghai')
    timenow = datetime.now(tz)
    return timenow.timetuple()

logging.Formatter.converter = Shanghai

# 日志设置
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]:  %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# 静态配置
platform = '2'
gkey = '000000'
app_version = '4.3.1.5.2'
versioncode = '398'
market_id = 'floor_web'
headers = {
    "Connection": "close",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent": "okhttp/3.8.1",
    "Host": 'floor.huluxia.com'
}

# 加载版块信息
cat_id_dict = {
    "1":"3楼公告版",
    "2":"泳池",
    "3":"自拍",
    "4":"游戏",
    "6":"意见反馈",
    "15":"葫芦山",
    "16":"玩机广场",
    "21":"穿越火线",
    "22":"英雄联盟",
    "29":"次元阁",
    "43":"实用软件",
    "44":"玩机教程",
    "45":"原创技术",
    "57":"头像签名",
    "58":"恶搞",
    "60":"未知版块",
    "63":"我的世界",
    "67":"MC贴子",
    "68":"资源审核",
    "69":"优秀资源",
    "70":"福利活动",
    "71":"王者荣耀",
    "76":"娱乐天地",
    "81":"手机美化",
    "82":"3楼学院",
    "84":"3楼精选",
    "92":"模型玩具",
    "94":"三楼活动",
    "96":"技术分享",
    "98":"制图工坊",
    "102":"LOL手游",
    "107":"三两影",
    "108":"新游推荐",
    "110":"原神",
    "111":"Steam",
    "115":"金铲铲之战",
    "119":"爱国爱党",
    "125":"妙易堂"
}

# 从环境变量中获取账号和密码
accounts = []
if "HULUXIA_ACCOUNTS" in os.environ:
    accounts_env = os.environ["HULUXIA_ACCOUNTS"]
    accounts = [tuple(acc.split(":")) for acc in accounts_env.split(",")]

# 读取邮箱配置
with open("config.json", "r") as f:
    config = json.load(f)

email_config = config.get("email", {})

# 邮件推送函数
def email_push(subject, content):
    smtp_server = email_config.get("smtp_server")
    port = email_config.get("port")
    sender_email = email_config.get("sender_email")
    password = email_config.get("password")
    receiver_email = email_config.get("receiver_email")

    if not smtp_server or not sender_email or not password or not receiver_email:
        logger.warning("邮件推送配置不完整，无法发送邮件")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(content, "plain"))
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            logger.info("邮件推送成功")
    except Exception as e:
        logger.error(f"邮件推送失败：{e}")

# 葫芦侠签到类
class HuluxiaSignin:
    def __init__(self):
        self._key = ''
        self.cat_id = ''
        self.userid = ''
        self.signin_continue_days = ''
        self.device_code = f'4EE6665E7AAC4C94B5C744AA82746F72'  # 使用新的 device_code
        self.device_model = 'iPhone14,3'  # 更新为新的设备型号
        self.phone_brand_type = random.choice(["MI", "Huawei", "UN", "OPPO", "VO"])  # 随机选择手机品牌类型
        self.session = requests.Session()

    def psd_login(self, account, password):
        # 使用最新的登录URL和请求参数
        login_url = f'https://floor.huluxia.com/account/login/IOS/1.0'  # 更新为新的登录URL
        login_data = {
            'access_token': '',
            'app_version': app_version,
            'code': '',
            'device_code': self.device_code,
            'device_model': self.device_model,
            'email': account,
            'market_id': market_id,
            'openid': '',
            'password': self.md5(password),  # 密码进行MD5加密
            'phone': '',
            'platform': platform
        }
        try:
            res = self.session.post(url=login_url, data=login_data, headers=headers)
            return res.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"登录请求失败：{e}")
            return {"status": 0}

    def set_config(self, acc, psd):
        data = self.psd_login(acc, psd)
        if data.get('status') == 0:
            logger.error(f"账号 {acc} 登录失败，请检查账号或密码")
            return False
        self._key = data['_key']
        self.userid = data['user']['userID']
        return True

    def user_info(self):
        info_url = f'http://floor.huluxia.com/user/info/ANDROID/4.1.8?platform={platform}&gkey={gkey}&app_version={app_version}&versioncode={versioncode}&market_id={market_id}&_key={self._key}&device_code={self.device_code}&phone_brand_type={self.phone_brand_type}&user_id={self.userid}'
        try:
            res = self.session.get(url=info_url, headers=headers)
            return res.json().get('nick'), res.json().get('level'), res.json().get('exp'), res.json().get('nextExp')
        except Exception as e:
            logger.error(f"获取用户信息失败：{e}")
            return None, None, None, None

    def md5(self, text):
        _md5 = hashlib.md5()
        _md5.update(text.encode())
        return _md5.hexdigest()

    def timestamp(self):
        return int(time.time())

    def sign_get(self):
        n = self.cat_id
        i = str(self.timestamp())
        r = 'fa1c28a5b62e79c3e63d9030b6142e4b'
        return self.md5(f"cat_id{n}time{i}{r}")

    def huluxia_signin(self, acc, psd):
        if not self.set_config(acc, psd):
            return f"账号 {acc} 登录失败，请检查账号或密码\n"

        nick, level, exp, next_exp = self.user_info()
        if not nick:
            return f"用户信息获取失败，跳过账号 {acc}\n"
        logger.info(f"正在为用户 {nick} 签到，等级: Lv.{level}, 当前经验值: {exp}/{next_exp}")
        summary = f"用户 <{nick}> 签到中...\n等级: Lv.{level}\n当前经验值: {exp}/{next_exp}\n"
        exp_get = 0

        for cat_id, cat_name in cat_id_dict.items():
            self.cat_id = cat_id
            sign = self.sign_get().upper()
            sign_url = f'http://floor.huluxia.com/user/signin/ANDROID/4.1.8?platform={platform}&gkey={gkey}&app_version={app_version}&versioncode={versioncode}&market_id={market_id}&_key={self._key}&device_code={self.device_code}&phone_brand_type={self.phone_brand_type}&cat_id={self.cat_id}&time={self.timestamp()}'
            post_data = {'sign': sign}
            try:
                res = self.session.post(url=sign_url, data=post_data, headers=headers)
                res_json = res.json()
                if res_json.get('status') == 0:
                    logger.warning(f"【{cat_name}】签到失败或已经签到")
                    continue
                exp_gain = res_json.get('experienceVal', 0)
                self.signin_continue_days = res_json.get('continueDays', 0)
                logger.info(f"【{cat_name}】签到成功，经验值+{exp_gain}")
                summary += f"【{cat_name}】签到成功，经验值+{exp_gain}\n"
                exp_get += exp_gain
            except Exception as e:
                logger.error(f"【{cat_name}】签到异常：{e}")

            time.sleep(2)  # 限制每次请求间隔

        summary += f"本次签到完成，共获取经验值 {exp_get}\n"
        logger.info(f"本次签到完成，共获取经验值 {exp_get}")
        return summary


def main():
    all_results = "葫芦侠签到结果：\n\n"
    for acc, psd in accounts:
        logger.info(f"开始处理账号 {acc}")
        signin = HuluxiaSignin()
        result = signin.huluxia_signin(acc, psd)
        all_results += result + "\n"
        time.sleep(5)  # 每个账号之间增加休眠

    # 推送所有账号签到结果
    email_push("葫芦侠签到结果", all_results)
    logger.info("所有账号签到已完成")


if __name__ == "__main__":
    main()
