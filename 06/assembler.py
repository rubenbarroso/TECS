import re
import sys

# [dest=]comp[;jump]
c_instr_pattern = re.compile('(\w+=)?([|&!\+\w-]+)(;\w+)?')

class Command:
    """
    """

    def _get_type(self, line, n):
        if line[0] == '@':
            return "A_COMMAND"
        if line[0] == '(':
            return "L_COMMAND"
        if c_instr_pattern.match(line):
            return "C_COMMAND"
        raise ValueError('Invalid command at line %s: %s' % (n, line))

    def _get_symbol(self, line, n):
        if self._get_type(line, n) == "A_COMMAND":
            return line[1:]
        if self._get_type(line, n) == "L_COMMAND":
            return line.translate(None, '()')
        raise ValueError('Invalid command at line %s: %s' % (n, line))

    def _get_dest(self, line, n):
        dest = c_instr_pattern.match(line).group(1)
        return dest if dest is None else dest[:-1]

    def _get_comp(self, line, n):
        return c_instr_pattern.match(line).group(2)

    def _get_jump(self, line, n):
        jump = c_instr_pattern.match(line).group(3)
        return jump if jump is None else jump[1:]

    def __init__(self, line, n):
        self.type = self._get_type(line.strip(), n)
        if self.type in ('A_COMMAND', 'L_COMMAND'):
            self.symbol = self._get_symbol(line.strip(), n)
        if self.type == 'C_COMMAND':
            self.dest = self._get_dest(line.strip(), n)
            self.comp = self._get_comp(line.strip(), n)
            self.jump = self._get_jump(line.strip(), n)


class Code:
    def __init__(self):
        self.dests = {'M': '001', 'D': '010', 'MD': '011',
                      'A': '100', 'AM': '101', 'AD': '110',
                      'AMD': '111'}
        self.comps = {'0': '0101010',
                      '1': '0111111',
                      '-1': '0111010',
                      'D': '0001100',
                      'A': '0110000',
                      '!D': '0001101',
                      '!A': '0110001',
                      '-D': '0001111',
                      '-A': '0110011',
                      'D+1': '0011111',
                      'A+1': '0110111',
                      'D-1': '0001110',
                      'A-1': '0110010',
                      'D+A': '0000010',
                      'D-A': '0010011',
                      'A-D': '0000111',
                      'D&A': '0000000',
                      'D|A': '0010101',
                      'M': '1110000',
                      '!M': '1110001',
                      '-M': '1110011',
                      'M+1': '1110111',
                      'M-1': '1110010',
                      'D+M': '1000010',
                      'D-M': '1010011',
                      'M-D': '1000111',
                      'D&M': '1000000',
                      'D|M': '1010101'}
        self.jumps = {'JGT': '001', 'JEQ': '010', 'JGE': '011',
                      'JLT': '100', 'JNE': '101', 'JLE': '110',
                      'JMP': '111'}

    def dest(self, mnemonic):
        if mnemonic is None:
            return "000"
        return self.dests[mnemonic]

    def comp(self, mnemonic):
        return self.comps[mnemonic]

    def jump(self, mnemonic):
        if mnemonic is None:
            return "000"
        return self.jumps[mnemonic]


class Parser:
    """
    """

    def __init__(self, file):
        self.commands = []
        with open(file) as f:
            n = 0
            for line in f.readlines():
                if not (line.startswith('//') or line.isspace()):
                    self.commands.append(Command(line, n))
                    n += 1
        self.iterator = self.__iter__()
        self.next = self.iterator.next()

    def __iter__(self):
        for command in self.commands:
            yield command

parser = Parser(sys.argv[1])
code = Code()

#first pass
symbol_table = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
                'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5,
                'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
                'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384,
                'KBD': 24576}
rom_address = 0
for command in parser:
    if command.type in ('A_COMMAND', 'C_COMMAND'):
        rom_address += 1
    else:
        # L_COMMAND
        symbol_table[command.symbol] = rom_address

#second pass
ram_adress = 16

for command in parser:
    if command.type == 'A_COMMAND':
        if command.symbol.isdigit():
            a_command = command.symbol
        else:
            if command.symbol not in symbol_table:
                symbol_table[command.symbol] = ram_adress
                ram_adress += 1
            a_command = symbol_table[command.symbol]
        print '0%s' % str(bin(int(a_command)))[2:].zfill(15)
    elif command.type == 'C_COMMAND':
        print '111%s%s%s' % (code.comp(command.comp), code.dest(command.dest), code.jump(command.jump))
