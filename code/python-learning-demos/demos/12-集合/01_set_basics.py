"""Day12：集合只保留不重复元素，且不保证业务顺序。"""


def main() -> None:
    languages = {"Python", "Java", "Python", "Go"}
    print(f"自动去重后的集合：{sorted(languages)}")

    languages.add("Rust")
    languages.add("Rust")             # 再次添加不会产生重复元素
    print(f"添加后：{sorted(languages)}")

    languages.discard("Go")           # 不存在时也不会报错
    languages.discard("Kotlin")
    print(f"删除后：{sorted(languages)}")
    print(f"是否包含 Python：{'Python' in languages}")

    numbers = [3, 1, 3, 2, 1, 2]
    unique_numbers = set(numbers)
    print(f"列表去重：{sorted(unique_numbers)}")


if __name__ == "__main__":
    main()

# 练习：比较 remove 和 discard 删除不存在元素时的行为。
