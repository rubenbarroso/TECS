import unittest
from assembler import Command, Code

class TestAssembler(unittest.TestCase):

    def test_command(self):
        a_command = Command('@1000', 0)
        self.assertEqual(a_command.type, "A_COMMAND")
        self.assertEqual(a_command.symbol, "1000")

        a_command = Command('@0', 0)
        self.assertEqual(a_command.type, "A_COMMAND")
        self.assertEqual(a_command.symbol, "0")

        a_command = Command('    @0', 0)
        self.assertEqual(a_command.type, "A_COMMAND")
        self.assertEqual(a_command.symbol, "0")

        a_command = Command('@i', 0)
        self.assertEqual(a_command.type, "A_COMMAND")
        self.assertEqual(a_command.symbol, "i")

        l_command = Command('(xxx)', 0)
        self.assertEqual(l_command.type, "L_COMMAND")
        self.assertEqual(l_command.symbol, "xxx")

        c_command = Command('A', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "A")
        self.assertIsNone(c_command.dest)
        self.assertIsNone(c_command.jump)

        c_command = Command('A;JMP', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "A")
        self.assertIsNone(c_command.dest)
        self.assertEqual(c_command.jump, "JMP")

        c_command = Command('D=A', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "A")
        self.assertEqual(c_command.dest, "D")
        self.assertIsNone(c_command.jump)

        c_command = Command('D=A;JGE', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "A")
        self.assertEqual(c_command.dest, "D")
        self.assertEqual(c_command.jump, "JGE")

        c_command = Command('D=D-M', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "D-M")
        self.assertEqual(c_command.dest, "D")
        self.assertIsNone(c_command.jump)

        c_command = Command('D=D-M // comment', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "D-M")
        self.assertEqual(c_command.dest, "D")
        self.assertIsNone(c_command.jump)

        c_command = Command('D;JGE // comment', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "D")
        self.assertIsNone(c_command.dest)
        self.assertEqual(c_command.jump, "JGE")

        c_command = Command('D=D+A', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "D+A")
        self.assertEqual(c_command.dest, "D")
        self.assertIsNone(c_command.jump)

        c_command = Command('M=!M', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "!M")
        self.assertEqual(c_command.dest, "M")
        self.assertIsNone(c_command.jump)

        c_command = Command('D=D&A', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "D&A")
        self.assertEqual(c_command.dest, "D")
        self.assertIsNone(c_command.jump)

        c_command = Command('D=D|A', 0)
        self.assertEqual(c_command.type, "C_COMMAND")
        self.assertEqual(c_command.comp, "D|A")
        self.assertEqual(c_command.dest, "D")
        self.assertIsNone(c_command.jump)

    def test_code(self):
        code = Code()
        self.assertEqual(code.dest(None), '000')
        self.assertEqual(code.dest('AD'), '110')

        self.assertEqual(code.comp('D-M'), '1010011')
        self.assertEqual(code.dest('D'), '010')