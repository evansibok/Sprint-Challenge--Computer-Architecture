"""CPU functionality."""

import sys

# Instructions
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
# Arithmetic Operations
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
INC = 0b01100101
DEC = 0b01100110
AND = 0b10101000
OR = 0b10101010
NOT = 0b01101001
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100
CMP = 0b10100111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.ram[self.SP] = 0xF4
        self.running = True
        self.FL = 0b000  # FL bits: 00000LGE
        self.dt = {
            # System Instructions
            LDI: self.handle_ldi,
            PRN: self.handle_prn,
            HLT: self.handle_hlt,
            PUSH: self.handle_push,
            POP: self.handle_pop,
            CALL: self.handle_call,
            RET: self.handle_ret,

            # Arith Instructions
            ADD: self.handle_add,
            SUB: self.handle_sub,
            MUL: self.handle_mul,
            DIV: self.handle_div,
            AND: self.handle_and,
            OR: self.handle_or,
            NOT: self.handle_not,
            XOR: self.handle_xor,
            MOD: self.handle_mod,
            SHL: self.handle_shl,
            SHR: self.handle_shr,
            CMP: self.handle_cmp,

            # Arith Logic
            'ADD': self.handle_ADD,
            'SUB': self.handle_SUB,
            'MUL': self.handle_MUL,
            'DIV': self.handle_DIV,
            'AND': self.handle_AND,
            'OR': self.handle_OR,
            'NOT': self.handle_NOT,
            'XOR': self.handle_XOR,
            'MOD': self.handle_MOD,
            'SHL': self.handle_SHL,
            'SHR': self.handle_SHR,
            'CMP': self.handle_CMP,
        }

    def handle_ldi(self, register, value):
        self.reg[register] = value
        self.pc += 3

    def handle_prn(self, register, some2):
        print(self.reg[register])
        self.pc += 2

    def handle_hlt(self, some1, some2):
        self.running = False
        sys.exit(-1)

    def handle_push(self, register, some2):
        self.SP -= 1
        self.ram[self.SP] = self.reg[register]
        self.pc += 2

    def handle_pop(self, register, some2):
        self.reg[register] = self.ram[self.SP]
        self.SP += 1
        self.pc += 2

    def handle_call(self, register, some2):
        """
        Handles a subroutine CALL.
        Push the address of the instruction directly after the CALL to the stack. This allows us to return to where we left off when the subroutine finiseses executing.
        """
        self.SP -= 1
        self.ram[self.SP] = self.pc + 2
        # The code below also works after
        # the SP has been decremented by 1
        # self.ram_write(self.SP, self.pc + 2)

        # Set the pc to the address stored in the given register
        self.pc = self.reg[register]

    def handle_ret(self, some1, some2):
        """
        Read from RAM, pop the value from the top (the current SP) of the stack and store in the program counter
        """
        self.pc = self.ram[self.SP]
        # The code below also works to read from ram
        # self.pc = self.ram_read(self.SP)
        self.SP += 1

    # Perform AND on ALU instructions to keep values between 0-255

    def handle_add(self, reg_a, reg_b):
        self.alu('ADD', reg_a, reg_b)

    def handle_sub(self, reg_a, reg_b):
        self.alu('SUB', reg_a, reg_b)

    def handle_mul(self, reg_a, reg_b):
        self.alu('MUL', reg_a, reg_b)

    def handle_div(self, reg_a, reg_b):
        self.alu('DIV', reg_a, reg_b)

    def handle_and(self, reg_a, reg_b):
        self.alu('AND', reg_a, reg_b)

    def handle_or(self, reg_a, reg_b):
        self.alu('OR', reg_a, reg_b)

    def handle_not(self, reg_a, reg_b):
        self.alu('NOT', reg_a, reg_b)

    def handle_xor(self, reg_a, reg_b):
        self.alu('XOR', reg_a, reg_b)

    def handle_mod(self, reg_a, reg_b):
        self.alu('MOD', reg_a, reg_b)

    def handle_shl(self, reg_a, reg_b):
        self.alu('SHL', reg_a, reg_b)

    def handle_shr(self, reg_a, reg_b):
        self.alu('SHR', reg_a, reg_b)

    def handle_cmp(self, reg_a, reg_b):
        self.alu('CMP', reg_a, reg_b)

    def handle_ADD(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] + self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_SUB(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] - self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_MUL(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_DIV(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] / self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_AND(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] & self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_OR(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] | self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_NOT(self, reg_a, reg_b):
        self.reg[reg_a] = ~self.reg[reg_a]
        self.pc += 2

    def handle_XOR(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] ^ self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_MOD(self, reg_a, reg_b):
        self.reg[reg_a] %= self.reg[reg_b]
        self.pc += 3

    def handle_SHL(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] << self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_SHR(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] >> self.reg[reg_b]) & 0xFF
        self.pc += 3

    def handle_CMP(self, reg_a, reg_b):
        """
        Compares values in the registers and sets the Flags accordingly.
        """
        if self.reg[reg_a] == self.reg[reg_b]:
            # set E to 1
            self.FL = 0b001
            # else set E to 0
            print('E', f"{self.FL:08b}")

        if self.reg[reg_a] > self.reg[reg_b]:
            # set G to 1
            self.FL = 0b010
            # else set G to 0
            print('G', f"{self.FL:08b}")

        if self.reg[reg_a] < self.reg[reg_b]:
            # set L to 1
            self.FL = 0b100
            # else set L to 0
            print('L', f"{self.FL:08b}")
        self.pc += 3

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        try:
            with open(filename) as file:
                for line in file:
                    # remove comments
                    no_comments = line.split('#')

                    # Grab the numbers and remove whitespaces
                    numbers = no_comments[0].strip()

                    # If we have an empty line
                    if numbers == '':
                        # continue iteration
                        continue

                    # Convert to integers to make it possible
                    # to save to register
                    values = int(numbers, 2)

                    # Using the address as index
                    # store the result gotten from reading the file
                    # and save to self.reg[address]
                    self.ram[address] = values

                    # Continue iteration
                    address += 1
        except FileNotFoundError:
            print("File not found!!!")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        try:
            handle_func = self.dt[op]
            handle_func(reg_a, reg_b)
        except:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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
            # op_size = ir >> 6
            # Anding ir with 0b00100000 will always return 0b00100000 and shifting right with 6 will always return 0... So bad choice
            # op_size1 = (ir & 0b00100000) >> 6
            # print('op_s1', f"{op_size1:08b}")
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            if ir in self.dt:
                # if op_size == 0:
                #     self.dt[ir]()
                # elif op_size == 1:
                #     self.dt[ir](op_a)
                # elif op_size == 2:
                self.dt[ir](op_a, op_b)
            else:
                print(f"Instruction: {ir:b} not found!")
                self.running = False


# 1010 1000 - AND
# 0010 0000 - 0b00100000
# ---------
# 0010 0000

# If the instruction is ALU it should always return 0b00100000
# if ir & 0b00100000 == 0b00100000:
# 1010 1000
# 1010 1000
# ----------
# 1010 1000 -


# Implement three instructions:

# LDI: load "immediate", store a value in a register, or "set this register to this value".
# PRN: a pseudo - instruction that prints the numeric value stored in a register.
# HLT: halt the CPU and exit the emulator.

# Not Implemented
# run()
# pc
# ram
# ram_read()
# ram_write()
# register (reg)

# cpu.py -> Implements the 8bit computer architecture
# Implemented

# ls8.py -> Run with each example file as second argument to run the program created in cpu.py
# LS8-spec ->
#

# Start by reading LS8-spec.md
