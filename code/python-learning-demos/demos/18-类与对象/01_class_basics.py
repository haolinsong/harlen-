"""Day18：类是创建对象的模板，对象把数据和行为放在一起。"""


class Student:
    """一个最小学生模型。"""

    def __init__(self, name: str, scores: list[float]) -> None:
        # self 指向当前对象，每个对象有各自的 name 和 scores。
        self.name = name
        self.scores = scores

    def average(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def add_score(self, score: float) -> None:
        if not 0 <= score <= 100:
            raise ValueError("成绩必须在 0 到 100 之间")
        self.scores.append(score)

    def __str__(self) -> str:
        return f"Student(name={self.name}, average={self.average():.2f})"


def main() -> None:
    alice = Student("Alice", [88, 92])
    bob = Student("Bob", [75, 80, 85])
    alice.add_score(100)

    print(alice)
    print(bob)
    print(f"两个对象是否相同：{alice is bob}")


if __name__ == "__main__":
    main()

# 练习：增加 passed 方法，平均分不低于 60 时返回 True。
