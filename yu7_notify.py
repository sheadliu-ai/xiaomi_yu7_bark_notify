import requests
import json
import os
from datetime import datetime
import toml
import os
import sys
import argparse

BIN = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(BIN, "config.toml")


def load_config():
    config = toml.load(config_path)

    if args.cookie:
        print("使用命令行参数传入账号参数...")
        return (
            args.orderId,
            args.userId,
            args.cookie,
            args.device_token,
            config["api"]["error_times"],
        )

    try:
        print("使用config.toml传入账号参数...")
        return (
            config["api"]["orderId"],
            config["api"]["userId"],
            config["api"]["Cookie"],
            config["api"]["device_token"],
            config["api"]["error_times"],
        )
    except:
        print("请检查config.toml文件的参数是否完整/正确！")
        sys.exit()


def get_delivery_time(orderId, userId, Cookie):
    url = "https://api.retail.xiaomiev.com/mtop/car-order/order/detail"

    payload = [{"orderId": orderId, "userId": userId}]

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c31) NetType/4G Language/zh_CN",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Content-Type": "application/json",
        "configSelectorVersion": "2",
        "content-type": "application/json; charset=utf-8",
        "deviceappversion": "1.16.0",
        "x-user-agent": "channel/car platform/car.wxlite",
        "Referer": "https://servicewechat.com/wx183d85f5e5e273c6/93/page-frame.html",
        "Cookie": Cookie,
    }
    print(json.dumps(payload))
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    data = response.json().get("data", {})
    logo_link = data.get("backdropPictures", {}).get("backdropPicture", None)
    statusInfo = data.get("statusInfo", {})
    orderTimeInfo = data.get("orderTimeInfo", {})
    orderStatusName = statusInfo.get("orderStatusName")

    delivery_time = orderTimeInfo.get("deliveryTime")
    if not delivery_time:
        delivery_time = "请检查参数是否正确！"
        error_times_update = error_times + 1
        message = f"失败次数：{error_times_update}\norderId：{orderId}\nuserId：{userId}\nCookie：{Cookie}\n【失败次数超过3次后将停止发送】"

        save_delivery_time(delivery_time, error_times=error_times_update)
        if error_times_update <= 3:
            send_bark_message(device_token, message)
        sys.exit()
    add_time = orderTimeInfo.get("addTime")
    pay_time = orderTimeInfo.get("payTime")
    lock_time = orderTimeInfo.get("lockTime")
    goods_names = "|".join(
        item.get("goodsName", "") for item in data.get("orderItem", [])
    )
    text = f"📦 交付进度：{orderStatusName}，{delivery_time}\n\n📅 下定时间：{add_time}\n💳 支付时间：{pay_time}\n🔒 锁单时间：{lock_time}\n\n🛍️ 配置：{goods_names}"
    # 保存交付时间到文件
    save_delivery_time(delivery_time)

    return delivery_time, text, logo_link


def save_delivery_time(delivery_time, error_times=0):
    # 先加载当前的配置
    config = toml.load(config_path)
    if args.cookie:
        config["api"]["orderId"] = ""
        config["api"]["userId"] = ""
        config["api"]["Cookie"] = ""
        config["api"]["device_token"] = ""

    # 更新 deliveryTimeLatest
    config["api"]["deliveryTimeLatest"] = delivery_time
    config["api"]["error_times"] = error_times

    # 写入更新后的配置到文件
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config, f)


def load_delivery_time():
    if not os.path.exists(config_path):
        import shutil

        print("正在初始化配置文件...")
        shutil.copy("configBAK.toml", "config.toml")
    config = toml.load(config_path)  # 加载配置文件
    return config["api"].get(
        "deliveryTimeLatest", None
    )  # 获取 deliveryTimeLatest 的值，默认为 None


def send_bark_message(token, message, logo_link=None):
    icon_link = "https://upload.wikimedia.org/wikipedia/commons/4/4f/Xiaomi_EV_New.jpg"
    if logo_link:
        icon_link = logo_link
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = f"https://api.day.app/{token}"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }

    data = {
        "body": message,
        "title": f"小米汽车交付进度查询({current_time})",
        "icon": icon_link,
        "group": "test",
        "isArchive": 1,
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        print("请检查Bark的token是否正确！")
        sys.exit()


def main():
    if delivery_time != old_delivery_time:
        save_delivery_time(delivery_time)  # 更新配置文件
        if send_bark_message(device_token, message, logo_link):
            print("消息已发送成功！")
        else:
            print("消息发送失败。")
    else:
        print("交付时间没有更新。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load configuration from command line."
    )
    parser.add_argument("--orderId", type=str, help="Order ID")
    parser.add_argument("--userId", type=str, help="User ID")
    parser.add_argument("--cookie", type=str, help="User Cookie")
    parser.add_argument(
        "--device_token",
        type=str,
        help="Device Token",
    )

    args = parser.parse_args()
    # print(args)
    orderId, userId, Cookie, device_token, error_times = load_config()

    old_delivery_time = load_delivery_time()
    # print("old_delivery_time:", old_delivery_time)
    delivery_time, message, logo_link = get_delivery_time(orderId, userId, Cookie)

    main()
