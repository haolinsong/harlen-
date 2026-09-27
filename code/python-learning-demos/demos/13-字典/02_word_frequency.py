"""Day13：使用字典统计单词频率。"""

import re


def word_frequency(text: str) -> dict[str, int]:
    """忽略大小写，统计由字母和数字组成的单词。"""
    words = re.findall(r"\w+", text.lower())
    counts: dict[str, int] = {}
    for word in words:
        # get(word, 0) 在键不存在时返回 0。
        counts[word] = counts.get(word, 0) + 1
    return counts


def main() -> None:
    text = "Python is simple, and Python is readable."
    counts = word_frequency(text)

    # sorted 的 key 参数决定排序依据，这里先按次数降序，再按单词升序。
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    for word, count in ordered:
        print(f"{word:<10} {count}")


if __name__ == "__main__":
    main()

# 练习：读取一段更长文本，打印出现次数最多的三个单词。
