class Type:
    def __init__(self, name: str, expression: type):
        self.name = name
        self.expression = expression

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
