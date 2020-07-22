"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 7 + [244] # empty stack pointer starts at F4
        self.ram = [0] * 256
        self.pc = 0
        self.running = True
        self.branchtable = {
            #ALU operations
            0b10100000: self.add,
            0b10100001: self.sub,
            0b10100010: self.mul,
            0b10100011: self.div,
            0b10100100: self.mod,
            # 0b01100101: self.inc,
            # 0b01100110: self.dec,
            # 0b10100111: self.cmp,
            # 0b10101000: self.AND,
            # 0b01101001: self.NOT,
            # 0b10101010: self.OR,
            # 0b10101011: self.XOR,
            # 0b10101100: self.SHL,
            # 0b10101101: self.SHR

            #PC mutators
            0b01010000: self.call,
            0b00010001: self.ret,

            #Other
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b00000001: self.halt
        }
        pass

    def load(self, file_name):
        """Load a program into memory."""

        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    self.ram[address] = instruction

                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == 'DIV':
            self.reg[reg_a] //= self.reg[reg_b]
            self.pc += 3
        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def add(self, op1, op2):
        self.alu('ADD', op1, op2)

    def sub(self, op1, op2):
        self.alu('SUB', op1, op2)

    def mul(self, op1, op2):
        self.alu('MUL', op1, op2)

    def div(self, op1, op2):
        self.alu('DIV', op1, op2)

    def mod(self, op1, op2):
        self.alu('MOD', op1, op2)

    def call(self, op1, op2):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.pc + 2
        self.pc = self.reg[op1]

    def ret(self, op1, op2):
        self.pc = self.ram[self.reg[7]]
        self.reg[7] += 1

    def ldi(self, op1, op2):
        self.reg[op1] = op2
        self.pc += 3

    def push(self, op1, op2):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[op1]
        self.pc += 2

    def pop(self, op1, op2):
        self.reg[op1] = self.ram[self.reg[7]]
        self.reg[7] += 1
        self.pc += 2

    def prn(self, op1, op2):
        print(self.reg[op1])
        self.pc += 2

    def halt(self, op1, op2):
        self.running = False

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.branchtable[ir](operand_a, operand_b)
        pass
