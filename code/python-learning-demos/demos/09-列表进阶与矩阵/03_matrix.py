"""Day09：用嵌套列表表示矩阵。"""


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """交换矩阵的行和列。"""
    if not matrix:
        return []
    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix):
        raise ValueError("每一行必须具有相同长度")

    return [
        [matrix[row_index][column_index] for row_index in range(len(matrix))]
        for column_index in range(column_count)
    ]


def main() -> None:
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    print(f"原矩阵：{matrix}")
    print(f"转置矩阵：{transpose(matrix)}")


if __name__ == "__main__":
    main()

# 练习：编写两个同形矩阵相加的函数。
