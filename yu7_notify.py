import requests
import json
import os
from datetime import datetime
import toml
import os
import sys

BIN = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(BIN, "config.toml")


def load_config():
    try:
        config = toml.load(config_path)
        return (
            config["api"]["orderId"],
            config["api"]["userId"],
            config["api"]["Cookie"],
            config["api"]["device_token"],
        )
    except:
        print("请检查config.toml文件的参数是否正确！")
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

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    data = response.json().get("data", {})
    statusInfo = data.get("statusInfo", {})
    orderTimeInfo = data.get("orderTimeInfo", {})
    orderStatusName = statusInfo.get("orderStatusName")

    delivery_time = orderTimeInfo.get("deliveryTime")
    add_time = orderTimeInfo.get("addTime")
    pay_time = orderTimeInfo.get("payTime")
    lock_time = orderTimeInfo.get("lockTime")

    text = f"【{orderStatusName}：{delivery_time}】\n下定时间：{add_time}\n支付时间：{pay_time}\n锁单时间：{lock_time}"

    # 保存交付时间到文件
    save_delivery_time(delivery_time)

    return delivery_time, text


def save_delivery_time(delivery_time):
    # 先加载当前的配置
    config = toml.load(config_path)

    # 更新 deliveryTimeLatest
    config["api"]["deliveryTimeLatest"] = delivery_time

    # 写入更新后的配置到文件
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config, f)


def load_delivery_time():
    config = toml.load(config_path)  # 加载配置文件
    return config["api"].get(
        "deliveryTimeLatest", None
    )  # 获取 deliveryTimeLatest 的值，默认为 None


def send_bark_message(token, message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = f"https://api.day.app/{token}"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }

    data = {
        "body": message,
        "title": f"yu7进度查询({current_time})",
        "icon": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Xiaomi_EV_New.jpg",
        "group": "test",
        "isArchive": 1,
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200


if __name__ == "__main__":
    orderId, userId, Cookie, device_token = load_config()

    old_delivery_time = load_delivery_time()
    # print("old_delivery_time:", old_delivery_time)
    delivery_time, message = get_delivery_time(orderId, userId, Cookie)
    # print("new_delivery_time:", delivery_time)
    if delivery_time != old_delivery_time:
        print("交付时间已更新！")
        save_delivery_time(delivery_time)  # 更新配置文件
        if send_bark_message(device_token, message):
            print("消息已发送成功！")
        else:
            print("消息发送失败。")
    else:
        print("交付时间没有更新。")
