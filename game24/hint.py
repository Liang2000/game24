"""24 点提示模块逻辑。"""
from .solver import solve


class HintModel:
    def __init__(self):
        self.selected = [None, None, None, None]  # 4 个数字槽

    def pick(self, value):
        """把 value 填入第一个空槽；已满则返回 False。"""
        for i in range(4):
            if self.selected[i] is None:
                self.selected[i] = value
                return True
        return False

    def clear(self, index):
        """清空指定槽位。"""
        if 0 <= index < 4:
            self.selected[index] = None

    def is_full(self):
        return all(v is not None for v in self.selected)

    def numbers(self):
        return [v for v in self.selected if v is not None]

    def solve(self):
        """4 个槽填满时返回解法列表，否则返回空列表。"""
        if not self.is_full():
            return []
        return solve(self.numbers())
