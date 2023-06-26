import re

class Lexer:
    pattern = '[\w.]+|<=|>=|[,()=<>]'

    def __init__(self, sql_query):
        self.tokens = re.findall(self.pattern, sql_query)    

    def peek(self):
        if len(self.tokens) == 0:
            return None
        return self.tokens[0]

    def has_next(self):
        return len(self.tokens) > 0 and self.tokens[0]

    def get_next(self):
        if len(self.tokens) == 0:
            return None
        return self.tokens.pop(0)
