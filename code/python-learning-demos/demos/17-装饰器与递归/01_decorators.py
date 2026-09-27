"""Day17：装饰器在不修改原函数代码的情况下包裹额外行为。"""

from collections.abc import Callable
from functools import wraps
from typing import Any


def log_call(function: Callable[..., Any]) -> Callable[..., Any]:
    """装饰器：调用前后打印函数名和结果。"""

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"准备调用 {function.__name__}，args={args}, kwargs={kwargs}")
        result = function(*args, **kwargs)
        print(f"{function.__name__} 返回 {result!r}")
        return result

    return wrapper


def repeat(times: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """带参数装饰器：让函数重复执行指定次数。"""
    if times <= 0:
        raise ValueError("times 必须大于 0")

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result: Any = None
            for _ in range(times):
                result = function(*args, **kwargs)
            return result

        return wrapper

    return decorator


@log_call
def add(left: int, right: int) -> int:
    return left + right


@repeat(3)
def cheer() -> None:
    print("继续学习 Python！")


def main() -> None:
    add(3, 5)
    cheer()
    print(f"被 wraps 保留的函数名：{add.__name__}")


if __name__ == "__main__":
    main()

# 练习：编写一个 require_positive 装饰器，拒绝负数参数。
