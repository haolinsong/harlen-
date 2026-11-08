"""Day25：在本地构造并解析一封纯文本邮件。"""

from email import policy
from email.message import EmailMessage
from email.parser import BytesParser


def build_message(subject: str, body: str) -> EmailMessage:
    """创建邮件对象；示例地址使用 example.com。"""
    message = EmailMessage()
    message["From"] = "teacher@example.com"
    message["To"] = "student@example.com"
    message["Subject"] = subject
    message.set_content(body)
    return message


def main() -> None:
    message = build_message("Python 第 25 天", "今天练习邮件对象。")
    # as_bytes 把对象序列化为邮件字节；解析后仍可访问邮件头和正文。
    parsed = BytesParser(policy=policy.default).parsebytes(message.as_bytes())
    print(f"收件人：{parsed['To']}")
    print(f"主题：{parsed['Subject']}")
    print(f"正文：{parsed.get_content().strip()}")


if __name__ == "__main__":
    main()

# 练习：增加一个 Reply-To 邮件头，观察解析后能否读回。
