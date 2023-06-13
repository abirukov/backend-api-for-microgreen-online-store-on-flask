from enum import Enum


class SqlAlchemyFiltersOperands(Enum):
    EQUAL = '=='
    NOT_EQUAL = '!='
    MORE = '>'
    MORE_OR_EQUAL = '>='
    LESS_OR_EQUAL = '<='
    NULL = 'is_null'
    NOT_NULL = 'is_not_null'
    LIKE = 'like'
    ILIKE = 'ilike'
    NOT_LIKE = 'not_ilike'
    IN = 'in'
    NOT_IN = 'not_in'
    ANY = 'any'
    NOT_ANY = 'not_any'
