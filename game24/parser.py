"""解析玩家输入的 24 点表达式并校验。"""
from collections import Counter
from fractions import Fraction


class ParseError(ValueError):
    """表达式非法（语法错误、除以 0、用了不对的数字等）。"""


def _build_trans():
    d = {}
    for i in range(10):
        d[chr(0xFF10 + i)] = chr(0x30 + i)  # 全角数字 ０-９ → 0-9
    d.update(
        {
            "＋": "+",
            "－": "-",
            "−": "-",
            "–": "-",
            "—": "-",
            "×": "*",
            "＊": "*",
            "·": "*",
            "⋅": "*",
            "÷": "/",
            "／": "/",
            "（": "(",
            "）": ")",
            "　": " ",
        }
    )
    return str.maketrans(d)


_TRANS = _build_trans()


def _tokenize(s):
    tokens = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            tokens.append(("num", int(s[i:j])))
            i = j
            continue
        if c in "+-*/()":
            tokens.append((c, c))
            i += 1
            continue
        raise ParseError(f"无法识别的字符：{c}")
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.numbers_used = []

    def _peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (None, None)

    def _advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        val = self._expr()
        if self.pos != len(self.tokens):
            raise ParseError("表达式末尾有多余内容")
        return val, self.numbers_used

    def _expr(self):
        val = self._term()
        while self._peek()[0] in ("+", "-"):
            op = self._advance()[0]
            rhs = self._term()
            val = val + rhs if op == "+" else val - rhs
        return val

    def _term(self):
        val = self._factor()
        while self._peek()[0] in ("*", "/"):
            op = self._advance()[0]
            rhs = self._factor()
            if op == "/":
                if rhs == 0:
                    raise ParseError("除数不能为 0")
                val = val / rhs
            else:
                val = val * rhs
        return val

    def _factor(self):
        typ, tok = self._peek()
        if typ == "num":
            self._advance()
            self.numbers_used.append(tok)
            return Fraction(tok)
        if typ == "(":
            self._advance()
            val = self._expr()
            if self._peek()[0] != ")":
                raise ParseError("缺少右括号")
            self._advance()
            return val
        if typ is None:
            raise ParseError("表达式不完整")
        raise ParseError(f"此处不应出现 {tok}")


def _parse(expression):
    s = expression.translate(_TRANS)
    tokens = _tokenize(s)
    if not tokens:
        raise ParseError("表达式为空")
    return _Parser(tokens).parse()


def evaluate(expression):
    """解析并求值，返回 Fraction；非法则抛 ParseError。"""
    val, _ = _parse(expression)
    return val


def is_solution(expression, numbers):
    """expression 是否恰好使用给定 numbers 各一次、且结果为 24。"""
    val, used = _parse(expression)
    return val == 24 and Counter(used) == Counter(numbers)
