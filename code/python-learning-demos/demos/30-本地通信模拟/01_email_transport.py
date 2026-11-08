"""Day30：把邮件内容与发送动作分开，用本地替身验证发送逻辑。"""

from email.message import EmailMessage


class FakeMailTransport:
    """只保存邮件，不连接 SMTP 服务器。"""

    def __init__(self) -> None:
        self.sent: list[EmailMessage] = []

    def send_message(self, message: EmailMessage) -> None:
        self.sent.append(message)


def build_notice(recipient: str, report: str) -> EmailMessage:
    if "@" not in recipient:
        raise ValueError("收件地址格式不正确")
    message = EmailMessage()
    message["From"] = "teacher@example.invalid"
    message["To"] = recipient
    message["Subject"] = "学习报告"
    message.set_content(report)
    return message


def send_notice(transport: FakeMailTransport, recipient: str, report: str) -> None:
    # 把传输对象作为参数传入，测试时可替换为不联网的 Fake。
    transport.send_message(build_notice(recipient, report))


def main() -> None:
    transport = FakeMailTransport()
    send_notice(transport, "student@example.invalid", "本周学习 6 小时。")
    print("输入：student@example.invalid，本周学习 6 小时。")
    print("本地模拟发送数：", len(transport.sent))
    print("草稿正文：", transport.sent[0].get_content().strip())


if __name__ == "__main__":
    main()

# 练习：给 FakeMailTransport 增加一个“模拟失败”开关，观察调用方如何处理异常。
