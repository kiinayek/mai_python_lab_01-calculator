from toolkit.errors import (
    ConsecutiveOperatorsError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
    TooManyDotsError,
)


def make_number(char, sign):

    """ Преобразует строку числа в токен 
    ('NUMBER', значение int/float с учетом знака) """

    try:
        if '.' in char:
            return ('NUMBER', float(char) * sign)
        return ('NUMBER', int(char) * sign)
    except ValueError:
        raise TooManyDotsError()


def tokenize_fsm(expr):
    
    """ Разбивает выражение на токены 
    (числа int/float, операторы ['+','-','*','/','%'], скобки ())
    Состояния: START, NUMBER, OPERATOR, AFTER_NUM
    unary_sign - унарный +/-,
    flag = True - только что был унарный знак """
    
    tokens = []
    state = 'START'
    current_token = ''
    unary_sign = 1
    flag = False

    for char in expr:

        if char == ' ':
            if state == 'NUMBER':
                tokens.append(make_number(current_token, unary_sign))
                unary_sign = 1
                flag = False
                state = 'AFTER_NUM'
            continue

        elif state == 'START':
            if char.isdigit():
                state = 'NUMBER'
                current_token = char
            elif char in ['+','-']:
                if flag:
                    raise ConsecutiveOperatorsError()
                if char == '-':
                    unary_sign = -1
                flag = True
            elif char == '(':
                tokens.append(('L_PAREN', '('))
                flag = False
            elif char == ')':
                raise InvalidCharacterError(char)
            else:
                raise InvalidCharacterError(char)

        elif state == 'NUMBER':
            if char.isdigit() or char == '.':
                current_token += char
            elif char in ['+','-','*','/','%']:
                tokens.append(make_number(current_token, unary_sign))
                unary_sign = 1
                flag = False
                state = 'OPERATOR'
                current_token = char
            elif char == ')':
                tokens.append(make_number(current_token, unary_sign))
                unary_sign = 1
                flag = False
                tokens.append(('R_PAREN', ')'))
                state = 'AFTER_NUM'
            elif char == '(':
                raise ConsecutiveOperatorsError()
            else:
                raise InvalidCharacterError(char)

        elif state == 'AFTER_NUM':
            if char.isdigit() or char == '.':
                raise MissingOperandError()
            elif char in ['+','-','*','/','%']:
                state = 'OPERATOR'
                current_token = char
            elif char == ')':
                tokens.append(('R_PAREN', ')'))
            elif char == '(':
                raise MissingOperandError()
            else:
                raise InvalidCharacterError(char)    

        elif state == 'OPERATOR':
            if char == '/' and current_token == '/':
                current_token = '//'          
            elif char.isdigit() or char == '.':
                tokens.append(('OPERATOR', current_token))
                state = 'NUMBER'
                current_token = char
            elif char in ['+','-']:
                tokens.append(('OPERATOR', current_token))
                current_token = ''
                if char == '-':
                    unary_sign = -1
                state = 'START'
                flag = True
            elif char in ['*','/','%']:
                raise ConsecutiveOperatorsError()
            elif char == '(':
                tokens.append(('OPERATOR', current_token))
                tokens.append(('L_PAREN', '('))
                state = 'START'
                flag = False
            elif char == ')':
                raise InvalidCharacterError(char)
            else:
                raise InvalidCharacterError(char)

    if state == 'NUMBER':
        tokens.append(make_number(current_token, unary_sign))
    elif state == 'OPERATOR' or (state == 'START' and flag):
        raise MissingOperandError(
            'Ошибка: выражение не может заканчиваться знаком'
            )
    elif state == 'START' and not tokens:
        raise EmptyExpressionError()
    
    return tokens
