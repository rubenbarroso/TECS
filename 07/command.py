from abc import ABCMeta, abstractmethod

class Command:
    __metaclass__ = ABCMeta

    def __init__(self, n, arg1=None, arg2=None):
        # line number in the original source
        self.n = str(n) if n is not None else ''
        self.arg1 = arg1
        self.arg2 = arg2

    @abstractmethod
    def translate(self):
        pass


class Add(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'D=M',
                'A=A-1',
                'M=D+M',
                '@SP',
                'M=M-1']

    def __str__(self):
        return 'add'


class Sub(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'D=M',
                'A=A-1',
                'M=M-D',
                '@SP',
                'M=M-1']

    def __str__(self):
        return 'sub'


class Neg(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'M=-M']

    def __str__(self):
        return 'neg'


class Eq(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'D=M', #y
                'A=A-1',
                'D=D-M', #y-x
                '@EQ' + self.n,
                'D;JEQ',
                '@SP',
                'A=M-1',
                'A=A-1',
                'M=0', # x != y
                '@EQ' + self.n + '_CONT',
                '0;JMP',
                '(EQ' + self.n + ')', # x == y
                '@SP',
                'A=M-1',
                'A=A-1',
                'M=-1',
                '(EQ' + self.n + '_CONT)',
                '@SP',
                'D=M-1',
                'M=D']

    def __str__(self):
        return 'eq'


class Lt(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'D=M', #y
                'A=A-1',
                'D=D-M', #y - x
                '@LT' + self.n,
                'D;JGT', #x < y
                '@SP',
                'A=M-1',
                'A=A-1',
                'M=0', # x >= y
                '@LT' + self.n + '_CONT',
                '0;JMP',
                '(LT' + self.n + ')', # x < y
                '@SP',
                'A=M-1',
                'A=A-1',
                'M=-1',
                '(LT' + self.n + '_CONT)',
                '@SP',
                'D=M-1',
                'M=D']

    def __str__(self):
        return 'lt'


class Gt(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'D=M', #y
                'A=A-1',
                'D=M-D', #x - y
                '@GT' + self.n,
                'D;JGT', #x > y
                '@SP',
                'A=M-1',
                'A=A-1',
                'M=0', # x <= y
                '@GT' + self.n + '_CONT',
                '0;JMP',
                '(GT' + self.n + ')', # x < y
                '@SP',
                'A=M-1',
                'A=A-1',
                'M=-1',
                '(GT' + self.n + '_CONT)',
                '@SP',
                'D=M-1',
                'M=D']

    def __str__(self):
        return 'gt'


class And(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'D=M',
                'A=A-1',
                'M=D&M',
                '@SP',
                'M=M-1']

    def __str__(self):
        return 'and'


class Or(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'D=M',
                'A=A-1',
                'M=D|M',
                '@SP',
                'M=M-1']

    def __str__(self):
        return 'or'


class Not(Command):
    def __init__(self, n=None):
        Command.__init__(self, n)

    def translate(self):
        return ['// ' + self.__str__(),
                '@SP',
                'A=M-1',
                'M=!M']

    def __str__(self):
        return 'not'


def push_value_for(name, segment, index):
    if segment == 'constant':
        return ['@' + index,
                'D=A']
    return {'local': ['@' + index,
                      'D=A',
                      '@LCL',
                      'A=D+M',
                      'D=M'],
            'argument': ['@' + index,
                         'D=A',
                         '@ARG',
                         'A=D+M',
                         'D=M'],
            'this': ['@' + index,
                     'D=A',
                     '@THIS',
                     'A=D+M',
                     'D=M'],
            'that': ['@' + index,
                     'D=A',
                     '@THAT',
                     'A=D+M',
                     'D=M'],
            'temp': ['@' + index,
                     'D=A',
                     '@5',
                     'A=D+A',
                     'D=M'],
            'pointer': ['@' + index,
                        'D=A',
                        '@3',
                        'A=D+A',
                        'D=M'],
            'static': ['@' + name + '.' + index,
                       'D=M']}[segment]


class Push(Command):
    def __init__(self, name, segment, index, n=None):
        Command.__init__(self, n, segment, int(index))
        self.name = name

    def translate(self):
        asm = ['// ' + self.__str__()]
        asm.extend(push_value_for(self.name, self.arg1, str(self.arg2)))
        asm.extend(['@SP',
                    'A=M',
                    'M=D',
                    'D=A+1',
                    '@SP',
                    'M=D'])
        return asm

    def __str__(self):
        return '%s %s %i' % ('push', self.arg1, self.arg2)


def pop_address_for(name, segment, index):
    if segment == 'constant':
        raise ValueError
    return {'local': ['@' + index,
                      'D=A',
                      '@LCL',
                      'D=M+D',
                      '@R5',
                      'M=D'],
            'argument': ['@' + index,
                         'D=A',
                         '@ARG',
                         'D=M+D',
                         '@R5',
                         'M=D'],
            'this': ['@' + index,
                     'D=A',
                     '@THIS',
                     'D=M+D',
                     '@R5',
                     'M=D'],
            'that': ['@' + index,
                     'D=A',
                     '@THAT',
                     'D=M+D',
                     '@R5',
                     'M=D'],
            'temp': ['@' + index,
                     'D=A',
                     '@5',
                     'M=D+A'],
            'pointer': ['@' + index,
                        'D=A',
                        '@3',
                        'D=D+A',
                        '@R5',
                        'M=D'],
            'static': ['@' + name + '.' + index,
                       'D=A',
                       '@R5',
                       'M=D']}[segment]


class Pop(Command):
    def __init__(self, name, segment, index, n=None):
        Command.__init__(self, n, segment, int(index))
        self.name = name

    def translate(self):
        asm = ['// ' + self.__str__()]
        asm.extend(pop_address_for(self.name, self.arg1, str(self.arg2)))
        asm.extend(['@SP',
                    'M=M-1',
                    'A=M',
                    'D=M',
                    '@R5', # the pop address is in @R5
                    'A=M',
                    'M=D'])
        return asm

    def __str__(self):
        return '%s %s %i' % ('pop', self.arg1, self.arg2)