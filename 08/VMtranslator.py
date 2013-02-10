import os
import sys
import parser

vm_file = sys.argv[1]
with open(vm_file) as f:
    parser = parser.Parser(os.path.splitext(f.name)[0], f.readlines())
    for command in parser:
        print '\n'.join(command.translate())
