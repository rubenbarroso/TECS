import unittest
from command import Push, Add, Sub, Neg, Eq

class TestCommand(unittest.TestCase):
    def test_add(self):
        add = Add(0)
        self.assertEqual(add.translate(),
                         ['// add',
                          '@SP',
                          'A=M-1',
                          'D=M',
                          'A=A-1',
                          'M=D+M',
                          '@SP',
                          'M=M-1'])

    def test_sub(self):
        sub = Sub(0)
        self.assertEqual(sub.translate(),
                         ['// sub',
                          '@SP',
                          'A=M-1',
                          'D=M',
                          'A=A-1',
                          'M=M-D',
                          '@SP',
                          'M=M-1'])

    def test_neg(self):
        neg = Neg(0)
        self.assertEqual(neg.translate(),
                         ['// neg',
                          '@SP',
                          'A=M-1',
                          'M=-M'])

    def test_push(self):
        push = Push('test', 'constant', '7')
        self.assertEqual(push.translate(),
                         ['// push constant 7',
                          '@7',
                          'D=A',
                          '@SP',
                          'A=M',
                          'M=D',
                          'D=A+1',
                          '@SP',
                          'M=D'])

    def test_eq(self):
        n = 0
        eq = Eq(n)
        self.assertEqual(eq.translate(),
                         ['// eq',
                          '@SP',
                          'A=M-1',
                          'D=M',
                          'A=A-1',
                          'D=D-M',
                          '@EQ' + eq.n,
                          'D;JEQ',
                          '@SP',
                          'A=M-1',
                          'A=A-1',
                          'M=0',
                          '@EQ' + eq.n + '_CONT',
                          '0;JMP',
                          '(EQ' + eq.n + ')',
                          '@SP',
                          'A=M-1',
                          'A=A-1',
                          'M=-1',
                          '(EQ' + eq.n + '_CONT)',
                          '@SP',
                          'D=M-1',
                          'M=D'])
