"""Day19：property 在读取或设置属性时加入校验与计算。"""


class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        """只读计算属性，不额外保存一份可能过期的数据。"""
        return self._celsius * 9 / 5 + 32


def main() -> None:
    temperature = Temperature(25)
    print(f"摄氏度：{temperature.celsius:.1f}")
    print(f"华氏度：{temperature.fahrenheit:.1f}")
    temperature.celsius = 100
    print(f"修改后华氏度：{temperature.fahrenheit:.1f}")


if __name__ == "__main__":
    main()

# 练习：为 fahrenheit 增加 setter，使它能反向修改 celsius。
