import ast
from ast import AST, BinOp, boolop, operator
from typing import Dict, Iterator, Type, Union

from ..types import Mutation

Operator = Union[boolop, operator]

MAPPING: Dict[Type[Operator], Type[Operator]] = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.Div,
    ast.Div: ast.Mult,
    ast.FloorDiv: ast.Div,
    ast.Or: ast.And,
    ast.And: ast.Or,
}


def _switch_op(op: Operator) -> Operator:
    return MAPPING[type(op)]()


def switch_bin_ops(node: AST) -> Iterator[Mutation]:
    if isinstance(node, BinOp) and type(node.op) in MAPPING:
        yield Mutation(BinOp(left=node.left, op=_switch_op(node.op), right=node.right))
