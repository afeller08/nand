from collections import defaultdict
from sly import Lexer, Parser

class NandLexer(Lexer):
    tokens = { NAME, INT, ASSIGN, RBRACKET, LBRACKET }
    ignore = ' \t'
    literals = set('[]=:(),') | {r'\[', r'\]'} # TODO: I think this or is not actually necessary; test and delete.

    ASSIGN = ':='
    RBRACKET = r'-_'
    LBRACKET = r'_-'
    NAME = r'[a-zA-Z][a-zA-Z_0-9]*'

    @_(r'[0-9]+')
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newlines(self, t):
        self.lineno += len(t.value)


    def error(self, t):
        print(f"Bad: {t.value}")
        self.index += 1

class NandParser(Parser):
    tokens = NandLexer.tokens

    def __init__(self):
        self.names = {
            'nand': Nand,
        }

    @_('NAME "(" params ")" ASSIGN expr')
    def statement(self, p):
        print('in statement', p.params, p.expr)
        self.names[p.NAME] = p.expr

    @_('NAME "(" params ")" slice ASSIGN expr')
    def statement(self, p):
        print('in statement', p.params, p.slice)
        self.names[p.NAME] = p.expr

    @_('"[" INT "]"')
    def slice(self, p):
        print('in slice', p.INT)
        return (p.INT,)

    @_('"[" INT ":" INT "]"')
    def slice(self, p):
        print('in slice', p.INT0, p.INT1)
        return (p.INT0, p.INT1)

    @_('NAME')
    def params(self, p):
        print('in NAME params', p.NAME)
        return [p.NAME]

    @_('params "," NAME')
    def params(self, p):
        p.params.append(p.NAME)
        return p.params
        
    @_('INT')
    def expr(self, p):
        print('in INT expr')
        return p.INT

    @_('NAME')
    def expr(self, p):
        print('in NAME expr', p.NAME)
        return p.NAME

    @_('NAME "(" arguments ")"')
    def expr(self, p):
        print('in expr')
        return p.arguments

    @_('expr')
    def arguments(self, p):
        print("in expr arguments", p.expr)
        return [p.expr]

    @_('expr slice')
    def expr(self, p):
        print(p.expr, p.slice)
        return p.expr

    @_('arguments "," expr')
    def arguments(self, p):
        print("in arguments expr", p.expr)
        p.arguments.append(p.expr)
        return p.arguments
    

class Nand:
    def __init__(self, left, right):
        self.left = left
        self.right = right

def main():
    lexer = NandLexer()
    parser = NandParser()
    while True:
        try:
            text = input('nand > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
            print('hmm...', parser.names)

main()
