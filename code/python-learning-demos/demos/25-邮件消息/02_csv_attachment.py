"""Day25：给邮件对象添加 CSV 附件并读取附件内容。"""

from email import policy
from email.message import EmailMessage
from email.parser import BytesParser


def build_message_with_csv(csv_text: str) -> EmailMessage:
    """把 CSV 文本作为附件加入邮件草稿。"""
    message = EmailMessage()
    message["From"] = "teacher@example.com"
    message["To"] = "student@example.com"
    message["Subject"] = "学习记录"
    message.set_content("附件是本周学习时长。")
    # 明确设置 UTF-8，邮件解析器才能把中文 CSV 还原成文本。
    message.add_attachment(
        csv_text,
        subtype="csv",
        charset="utf-8",
        filename="learning.csv",
    )
    return message


def main() -> None:
    csv_text = "name,hours\nAlice,3\nBob,5\n"
    message = build_message_with_csv(csv_text)
    parsed = BytesParser(policy=policy.default).parsebytes(message.as_bytes())
    print(f"邮件主题：{parsed['Subject']}")
    print(f"正文：{parsed.get_body(preferencelist=('plain',)).get_content().strip()}")
    for attachment in parsed.iter_attachments():
        print(f"附件：{attachment.get_filename()} ({attachment.get_content_type()})")
        # text/csv 的 get_content 已按 charset 解码，返回 str。
        print(attachment.get_content().strip())


if __name__ == "__main__":
    main()

# 练习：再附加一个 JSON 文件，并分别读取两个附件的文件名与内容。
