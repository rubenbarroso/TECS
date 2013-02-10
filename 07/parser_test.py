import unittest
from command import Push, Add
from parser import create_command, Parser

class TestParser(unittest.TestCase):
    def test_create_command_push(self):
        push = create_command('test', 'push constant 7', 0)
        self.assertTrue(isinstance(push, Push))
        self.assertEquals(push.arg1, 'constant')
        self.assertEquals(push.arg2, 7)

    def test_create_command_add(self):
        push = create_command('test', 'add', 0)
        self.assertTrue(isinstance(push, Add))
        self.assertIsNone(push.arg1)
        self.assertIsNone(push.arg2)

    def test_parser(self):
        parser = Parser('test', ['// testing push',
                         'push constant 7'])
        commands = [command for command in parser]
        self.assertTrue(len(commands) == 1)
        push = commands[0]
        self.assertTrue(isinstance(push, Push))
        self.assertEquals(push.arg1, 'constant')
        self.assertEquals(push.arg2, 7)

