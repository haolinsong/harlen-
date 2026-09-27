"""Day20：通过抽象类、继承和多态计算不同员工的工资。"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Employee(ABC):
    employee_id: str
    name: str

    @abstractmethod
    def monthly_pay(self) -> float:
        """每种员工都必须给出自己的月薪计算方式。"""


@dataclass
class SalariedEmployee(Employee):
    salary: float

    def monthly_pay(self) -> float:
        return self.salary


@dataclass
class HourlyEmployee(Employee):
    hours: float
    hourly_rate: float

    def monthly_pay(self) -> float:
        normal_hours = min(self.hours, 160)
        overtime_hours = max(self.hours - 160, 0)
        # 超过 160 小时的部分按 1.5 倍计算。
        return normal_hours * self.hourly_rate + overtime_hours * self.hourly_rate * 1.5


@dataclass
class CommissionEmployee(Employee):
    base_salary: float
    sales: float
    commission_rate: float

    def monthly_pay(self) -> float:
        return self.base_salary + self.sales * self.commission_rate


def build_payroll(employees: list[Employee]) -> list[tuple[str, float]]:
    """多态：不判断员工类型，统一调用 monthly_pay。"""
    return [(employee.name, employee.monthly_pay()) for employee in employees]


def main() -> None:
    employees: list[Employee] = [
        SalariedEmployee("E001", "Alice", salary=8000),
        HourlyEmployee("E002", "Bob", hours=170, hourly_rate=40),
        CommissionEmployee("E003", "Carol", base_salary=4000, sales=50_000, commission_rate=0.05),
    ]

    total = 0.0
    for name, pay in build_payroll(employees):
        total += pay
        print(f"{name:<8} 月薪：{pay:,.2f}")
    print(f"工资总额：{total:,.2f}")


if __name__ == "__main__":
    main()

# 练习：增加 PieceworkEmployee，按照完成件数计算工资。
