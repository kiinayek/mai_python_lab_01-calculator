
# Класс для всех ошибок 
class ToolkitError(Exception):
    pass


# Ошибки калькулятора 
class CalculatorError(ToolkitError):
    pass

class EmptyExpressionError(CalculatorError):
    def __init__(self, message='Ошибка: пустое выражение'):
        super().__init__(message)

class InvalidCharacterError(CalculatorError):
    def __init__(self, char):
        super().__init__(f'Ошибка: недопустимый символ "{char}"')

class MissingOperandError(CalculatorError):
    def __init__(self, message='Ошибка: пропущен операнд'):
        super().__init__(message)

class MissingOperatorError(CalculatorError):
    def __init__(self, message='Ошибка: пропущен оператор'):
        super().__init__(message)

class ConsecutiveOperatorsError(CalculatorError):
    def __init__(self, message='Ошибка: два бинарных оператора подряд'):
        super().__init__(message)

class DivisionByZeroError(CalculatorError):
    def __init__(self, message='Ошибка: деление на ноль'):
        super().__init__(message)

class TooManyDotsError(CalculatorError):
    def __init__(self, message='Ошибка: недопустимое вещественное число'):
        super().__init__(message)


# Ошибки конвертера 
class ConverterError(ToolkitError):
    pass

class UnknownUnitError(ConverterError):
    def __init__(self, unit):
        super().__init__(f'Ошибка: неизвестная единица "{unit}"')

class IncompatibleUnitsError(ConverterError):
    def __init__(self, from_unit, to_unit):
        super().__init__(f'Ошибка: единицы "{from_unit}" и "{to_unit} несовместимы"')

class AbsoluteZeroError(ConverterError):
    def __init__(self, message='Ошибка: температура ниже абсолютного нуля'):
        super().__init__(message)