import command

commands = {'push': lambda name, n, arg1, arg2: command.Push(name, arg1, arg2),
            'pop': lambda name, n, arg1, arg2: command.Pop(name, arg1, arg2),
            'add': lambda name, n, arg1, arg2: command.Add(),
            'sub': lambda name, n, arg1, arg2: command.Sub(),
            'and': lambda name, n, arg1, arg2: command.And(),
            'or': lambda name, n, arg1, arg2: command.Or(),
            'not': lambda name, n, arg1, arg2: command.Not(),
            'neg': lambda name, n, arg1, arg2: command.Neg(),
            'eq': lambda name, n, arg1, arg2: command.Eq(n),
            'lt': lambda name, n, arg1, arg2: command.Lt(n),
            'gt': lambda name, n, arg1, arg2: command.Gt(n)}

def create_command(name, line, n):
    line_tokens = line.split()
    command_tokens = [line_tokens[0].lower(),
                      line_tokens[1].lower() if len(line_tokens) > 1 else None,
                      line_tokens[2].lower() if len(line_tokens) > 2 else None]
    return commands[command_tokens[0]](name, n, command_tokens[1], command_tokens[2])


class Parser:
    def __init__(self, name, lines):
        self.name = name
        self.lines = [line.strip() for line in lines
                      if not (line.startswith('//') or line.isspace())]
        self.iterator = self.__iter__()
        self.next = self.iterator.next()

    def __iter__(self):
        n = 0
        for line in self.lines:
            yield create_command(self.name, line, n)
            n += 1


