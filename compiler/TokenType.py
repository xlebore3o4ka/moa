def meta(cls):
    groups = {}
    token_value = {}
    value_token = {}
    for name in cls.__dict__:
        if not name.startswith('__'):
            value = getattr(cls, name)
            if isinstance(value, tuple) and len(value) == 2:
                group_name, symbol = value
                if group_name in groups:
                    groups[group_name].append(symbol)
                else:
                    groups[group_name] = [symbol]
                token_value[name] = symbol
                value_token[symbol] = name
                setattr(cls, name, name)

    cls.group = classmethod(lambda cls_, name_: groups.get(name_, []))
    cls.value = classmethod(lambda cls_, type_: token_value.get(type_, None))
    cls.type = classmethod(lambda cls_, value_: value_token.get(value_, None))

    return cls


class MetaParent:
    @classmethod
    def group(cls, name):
        raise NotImplementedError

    @classmethod
    def value(cls, type):
        raise NotImplementedError

    @classmethod
    def type(cls, value):
        raise NotImplementedError


@meta
class TokenType(MetaParent):
    NUMBER   = ("LITERALS",  "0123456789.")

    PLUS     = ("OPERATORS", '+')
    MINUS    = ("OPERATORS", '-')
    MULTIPLY = ("OPERATORS", '*')
    DIVIDE   = ("OPERATORS", '/')
    MODULO   = ("OPERATORS", '%')

    LPAREN   = ("OPERATORS", '(')
    RPAREN   = ("OPERATORS", ')')

    POINT    = ("OPERATORS", '.')

    NEWLINE  = ("OTHERS",    "\n:")
    EOF      = ("OTHERS",    '\0')
