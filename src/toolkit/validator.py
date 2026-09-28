from toolkit.errors import (
    EmptyExpressionError,
    MissingOperandError,
    MissingOperatorError,
)


def validate(tokens):

    if not tokens:
        raise EmptyExpressionError()

    """ Проверка на баланс скобок """
    balance = 0
    for kind, _ in tokens:
        if kind == 'L_PAREN':
            balance += 1
        elif kind == 'R_PAREN':
            balance -= 1
            if balance < 0:
                raise MissingOperandError(
                    'Ошибка: лишняя закрывающая скобка'
                )
    if balance != 0:
        raise MissingOperandError('Ошибка: не закрыта скобка')

    """ Пары соседей """
    for i in range(len(tokens) - 1):
        left_kind = tokens[i][0]
        right_kind, right_val = tokens[i+1]

        """ Число и число """
        if left_kind == 'NUMBER' and right_kind == 'NUMBER':
            raise MissingOperatorError()

        """ Пустые скобки () """
        if left_kind == 'L_PAREN' and right_kind == 'R_PAREN':
            raise MissingOperandError('Ошибка: пустые скобки')

        """ Скобка ( и оператор """
        if left_kind == 'L_PAREN' and right_kind == 'OPERATOR' and right_val in ['*', '/', '//', '%']:
            raise MissingOperandError()

        """ Оператор и скобка ) """ 
        if left_kind == 'OPERATOR' and right_kind == 'R_PAREN':
            raise MissingOperandError()

        """ Число и скобка ( """  
        if left_kind == 'NUMBER' and right_kind == 'L_PAREN':
            raise MissingOperatorError()

        """ Скобка ) и число """
        if left_kind == 'R_PAREN' and right_kind == 'NUMBER':
            raise MissingOperatorError()