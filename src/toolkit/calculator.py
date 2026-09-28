from toolkit.errors import (
    DivisionByZeroError,
    InvalidCharacterError,
    MissingOperandError,
)
from toolkit.tokenizator import tokenize_fsm
from toolkit.validator import validate


class Stack:
    """ Стэк """
    def __init__(self): 
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def is_empty(self):
        return (self.items == [])

    def peek(self):
        return self.items[-1]


def priority_for_RPN(op):
    """ Приоритеты операций """

    if op in ['*', '/', '//', '%']:
        return 2
    if op in ['+', '-']:
        return 1


def to_RPN(tokens):
    """ Перевод токенов в обратную польскую запись """

    rpn = []
    stack = Stack()

    for kind, value in tokens:

        if kind == 'NUMBER':
            rpn.append(value)

        elif kind == 'L_PAREN':
            stack.push(value)

        elif kind == 'R_PAREN':
            while not stack.is_empty() and stack.peek() != '(':
                rpn.append(stack.pop())
            stack.pop()

        elif kind == 'OPERATOR':
            while (
                not stack.is_empty() 
                and stack.peek() != '(' 
                and priority_for_RPN(stack.peek()) >= priority_for_RPN(value)
            ):
                rpn.append(stack.pop())
            stack.push(value)

    while not stack.is_empty():
        op = stack.pop()
        rpn.append(op)

    return rpn  


def eval_RPN(rpn):
    """ Вычисление ОПЗ через стэк. // и % - только для int """

    stack = Stack()

    for char in rpn:
        if char not in ['+', '-', '*', '/', '//', '%']:
            stack.push(char)
        else:
            num_2, num_1 = stack.pop(), stack.pop()
            if char == '+':
                stack.push(round(num_1 + num_2, 10))
            elif char == '-':
                stack.push(round(num_1 - num_2, 10))
            elif char == '*':
                stack.push(round(num_1 * num_2, 10))
            elif char == '/':
                if num_2 in [0, 0.0]:
                    raise DivisionByZeroError()
                stack.push(round(num_1 / num_2, 10))
            elif char == '//':
                if num_2 == 0:
                    raise DivisionByZeroError()
                if type(num_1) != int or type(num_2) != int:
                    raise InvalidCharacterError('//')
                stack.push(round(int(num_1 / num_2), 10))
            elif char == '%':
                if num_2 == 0:
                    raise DivisionByZeroError()
                if type(num_1) != int or type(num_2) != int:
                    raise InvalidCharacterError('%')
                stack.push(round(num_1 % num_2, 10))

    if len(stack.items) != 1:
        raise MissingOperandError('Ошибка: некорректное выражение')
    
    return stack.pop()


def calculate(expression):
    """ Посчитать выражение полностью """
    
    tokens = tokenize_fsm(expression)
    validate(tokens)
    rpn = to_RPN(tokens)
    return eval_RPN(rpn)
