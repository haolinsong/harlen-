"""Day04：使用运算符完成摄氏度与华氏度转换。"""


def celsius_to_fahrenheit(celsius: float) -> float:
    """摄氏度转华氏度：F = C * 9 / 5 + 32。"""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """华氏度转摄氏度：C = (F - 32) * 5 / 9。"""
    return (fahrenheit - 32) * 5 / 9


def main() -> None:
    celsius = 25.0
    fahrenheit = celsius_to_fahrenheit(celsius)
    print(f"{celsius:.1f} 摄氏度 = {fahrenheit:.1f} 华氏度")
    print(f"{fahrenheit:.1f} 华氏度 = {fahrenheit_to_celsius(fahrenheit):.1f} 摄氏度")


if __name__ == "__main__":
    main()

# 练习：计算 0、37、100 摄氏度分别对应多少华氏度。
