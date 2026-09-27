from toolkit.errors import (
    AbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError
    )

LEN_M = {'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0} # длина в метрах
MASS_G = {'g': 1.0, 'kg': 1000.0} # масса в граммах
TEMP = {'c', 'f', 'k'}
ABS_ZERO_TEMP = {'c': -273.15, 'f': -459.67, 'k': 0.0}
ALL_UNITS = set(LEN_M) | set(MASS_G) | set(TEMP)

def convert(value, from_unit, to_unit):

    """ Конвертер: переводит value из from_unit в to_unit. 
    Группы: длина (mm/cm/m/km), масса (g/kg), температура (c/f/k).
    Регистр не важен. Между группами конвертировать нельзя.
    Температура ниже абсолютного нуля - ошибка"""
    
    from_unit, to_unit = from_unit.lower(), to_unit.lower()

    if from_unit not in ALL_UNITS:
        raise UnknownUnitError(from_unit)
    if to_unit not in ALL_UNITS:
        raise UnknownUnitError(to_unit)

    if not (
        (from_unit in LEN_M and to_unit in LEN_M) or 
        (from_unit in MASS_G and to_unit in MASS_G) or
        (from_unit in TEMP and to_unit in TEMP)
    ):
        raise IncompatibleUnitsError(from_unit, to_unit)
    
    if from_unit in LEN_M:
        result = value * LEN_M[from_unit] / LEN_M[to_unit]

    elif from_unit in MASS_G:
        result = value * MASS_G[from_unit] / MASS_G[to_unit]

    elif from_unit in TEMP:

        if value < ABS_ZERO_TEMP[from_unit]:
            raise AbsoluteZeroError()

        if from_unit == to_unit:
            return value
        
        elif from_unit == 'c':
            if to_unit == 'k':
                result = value + 273.15
            elif to_unit == 'f':
                result = value * 9 / 5 + 32

        elif from_unit == 'k':
            if to_unit == 'c':
                result = value - 273.15
            elif to_unit == 'f':
                result = (value - 273.15) * 9 / 5 + 32
    
        else:
            if to_unit == 'c':
                result = (value - 32) * 5 / 9
            elif to_unit == 'k':
                result = (value - 32) * 5 / 9 + 273.15

    return result
