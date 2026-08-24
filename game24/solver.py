"""24 点求解器：枚举所有本质不同的解法，并判定无解。

用精确有理数（fractions.Fraction）运算，中间结果允许分数与负数。
"""
from fractions import Fraction

_OPS = ("+", "-", "*", "/")


def _apply(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return a / b  # b != 0 由调用方保证


def _prec(op):
    return 2 if op in ("*", "/") else 1


def _canon(node):
    """规范化表达式树：合并 + 与 * 的交换律、结合律。"""
    if isinstance(node, int):
        return node
    op, l, r = node
    l = _canon(l)
    r = _canon(r)
    if op in ("+", "*"):
        atoms = []

        def collect(n):
            if isinstance(n, tuple) and n[0] == op:
                collect(n[1])
                collect(n[2])
            else:
                atoms.append(n)

        collect(l)
        collect(r)
        atoms.sort(key=_render)
        result = atoms[0]
        for a in atoms[1:]:
            result = (op, result, a)
        return result
    return (op, l, r)


def _render(node):
    if isinstance(node, int):
        return str(node)
    op, l, r = node
    return f"{_render_l(l, op)} {op} {_render_r(r, op)}"


def _render_l(child, parent_op):
    if isinstance(child, int):
        return str(child)
    if _prec(child[0]) < _prec(parent_op):
        return f"({_render(child)})"
    return _render(child)


def _render_r(child, parent_op):
    if isinstance(child, int):
        return str(child)
    if _prec(child[0]) < _prec(parent_op):
        return f"({_render(child)})"
    if _prec(child[0]) == _prec(parent_op) and parent_op in ("-", "/"):
        return f"({_render(child)})"
    return _render(child)


def solve(numbers):
    """返回至多 20 条本质不同的解法（中缀字符串），无解返回空列表。"""
    found = set()

    def rec(items):
        # items: list of (Fraction, node)
        if len(items) == 1:
            val, node = items[0]
            if val == 24:
                found.add(node)
            return
        for i in range(len(items)):
            for j in range(len(items)):
                if i == j:
                    continue
                a_val, a_node = items[i]
                b_val, b_node = items[j]
                rest = [items[k] for k in range(len(items)) if k != i and k != j]
                for op in _OPS:
                    if op == "/" and b_val == 0:
                        continue
                    node = (op, a_node, b_node)
                    rec(rest + [(_apply(op, a_val, b_val), node)])

    rec([(Fraction(n), n) for n in numbers])

    canonical = {_render(_canon(node)) for node in found}
    return sorted(canonical)[:20]


def is_solvable(numbers):
    """返回给定 4 个数是否存在至少一种解法。"""

    def rec(vals):
        if len(vals) == 1:
            return vals[0] == 24
        for i in range(len(vals)):
            for j in range(len(vals)):
                if i == j:
                    continue
                rest = [vals[k] for k in range(len(vals)) if k != i and k != j]
                a, b = vals[i], vals[j]
                for op in _OPS:
                    if op == "/" and b == 0:
                        continue
                    if rec(rest + [_apply(op, a, b)]):
                        return True
        return False

    return rec([Fraction(n) for n in numbers])
