"""Day20：用类、数据类、随机数和集合实现一个简化扑克发牌程序。"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass


SUITS = ("Clubs", "Diamonds", "Hearts", "Spades")
RANK_NAMES = {11: "J", 12: "Q", 13: "K", 14: "A"}


@dataclass(frozen=True)
class Card:
    """frozen=True 让牌不可修改，创建后点数和花色保持稳定。"""

    suit: str
    rank: int

    def __post_init__(self) -> None:
        if self.suit not in SUITS:
            raise ValueError(f"未知花色：{self.suit}")
        if not 2 <= self.rank <= 14:
            raise ValueError("点数必须在 2 到 14 之间")

    def __str__(self) -> str:
        rank_text = RANK_NAMES.get(self.rank, str(self.rank))
        return f"{rank_text} of {self.suit}"


class Deck:
    """一副 52 张牌，负责洗牌和发牌。"""

    def __init__(self) -> None:
        self._cards = [Card(suit, rank) for suit in SUITS for rank in range(2, 15)]

    def shuffle(self, random_source: random.Random | None = None) -> None:
        source = random_source or random.SystemRandom()
        source.shuffle(self._cards)

    def deal(self, count: int) -> list[Card]:
        if count < 0:
            raise ValueError("count 不能是负数")
        if count > len(self._cards):
            raise ValueError("剩余牌数不足")
        # 每 pop 一次都真正从牌堆移除一张，所以不会重复发同一张牌。
        return [self._cards.pop() for _ in range(count)]

    def __len__(self) -> int:
        return len(self._cards)


def hand_category(cards: list[Card]) -> str:
    """识别五张牌的基础牌型。"""
    if len(cards) != 5:
        raise ValueError("牌型判断需要恰好五张牌")

    ranks = sorted(card.rank for card in cards)
    counts = sorted(Counter(ranks).values(), reverse=True)
    is_flush = len({card.suit for card in cards}) == 1
    is_straight = ranks == list(range(ranks[0], ranks[0] + 5)) or ranks == [2, 3, 4, 5, 14]

    if is_straight and is_flush:
        return "同花顺"
    if counts == [4, 1]:
        return "四条"
    if counts == [3, 2]:
        return "葫芦"
    if is_flush:
        return "同花"
    if is_straight:
        return "顺子"
    if counts == [3, 1, 1]:
        return "三条"
    if counts == [2, 2, 1]:
        return "两对"
    if counts == [2, 1, 1, 1]:
        return "一对"
    return "高牌"


def main() -> None:
    deck = Deck()
    deck.shuffle(random.Random(2026))
    hand = sorted(deck.deal(5), key=lambda card: (card.rank, card.suit))

    print("玩家手牌：")
    for card in hand:
        print(f"  {card}")
    print(f"牌型：{hand_category(hand)}")
    print(f"牌堆剩余：{len(deck)} 张")


if __name__ == "__main__":
    main()

# 练习：创建两个玩家，每人发五张牌，并比较双方牌型等级。
