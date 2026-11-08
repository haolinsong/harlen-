"""Day30：构造短信 API 请求，用本地函数模拟响应；不访问外部服务。"""

import json
from urllib.request import Request


def build_sms_request(phone: str, message: str) -> Request:
    if not phone.startswith("+") or not phone[1:].isdigit():
        raise ValueError("号码应为示例格式：+国家码与数字")
    if not message.strip():
        raise ValueError("短信内容不能为空")
    payload = json.dumps({"to": phone, "message": message}, ensure_ascii=False).encode("utf-8")
    return Request(
        "https://sms.example.invalid/messages",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )


def fake_gateway(request: Request) -> dict[str, str]:
    """只检查请求内容，不调用 urlopen，因此不会发出真实短信。"""
    payload = json.loads(request.data.decode("utf-8"))
    if request.get_method() != "POST" or not payload["message"]:
        raise ValueError("请求不符合短信接口约定")
    return {"status": "accepted-locally", "to": payload["to"]}


def main() -> None:
    request = build_sms_request("+40123456789", "Python 学习提醒")
    print("输入：+40123456789，Python 学习提醒")
    print("请求方法：", request.get_method())
    print("本地模拟响应：", fake_gateway(request))


if __name__ == "__main__":
    main()

# 练习：增加短信长度上限，并在构造请求前拒绝超长内容。
