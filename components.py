# In this file we specify the different 
# components of the 8-bit CPU

# Import modules
import tkinter as tk
import time
from logic import *

class Component():
    def __init__(self, out_lights):
        self.out_lights = out_lights
        self.internal_state = []
        self.out_state = []

    # Show the output of the component
    def output(self):
        for i,s in enumerate(self.out_state):
            self.out_lights[i].set_state(s)



class Clock(Component):
    def __init__(self, out_lights, period):
        super().__init__(out_lights)
        self.period = period
        self.timer = time.time()
        self.internal_state = [0]
        self.previous_state = 0
        # State of transition: 0 for no transition, 
        # 1 for rising and -1 for decreasing
        self.transition_state = 0 

    def update(self):
        # Store current state as previous
        self.previous_state = self.internal_state[0]

        # Get new state, changes only after period
        if (time.time() - self.timer) >= self.period:
            self.timer = time.time()
            if self.previous_state == 0:
                self.internal_state[0] = 1
            else:
                self.internal_state[0] = 0

        # Check for transition state
        if self.previous_state == self.internal_state[0]:
            self.transition_state = 0
        else:
            if self.internal_state[0] == 1:
                self.transition_state = 1
            elif self.internal_state[0] == 0:
                self.transition_state = -1

        # Update light
        self.out_state = self.internal_state
        self.output()
        
        return self.internal_state[0], self.transition_state


class Counter(Component):
    def __init__(self, out_lights):
        super().__init__(out_lights)
        self.internal_state = ['0b000']
        self.out_state = [0,0,0]

    def read(self):
        return self.internal_state[0]

    def update(self, clock_state, clock_transition):
        if clock_state == 0 and clock_transition == -1:
            self.internal_state[0] = bin_sum(self.internal_state[0], '0b001')
            if self.internal_state[0] == '0b101':
                self.internal_state[0] = '0b000'
            self.out_state = bin_split(self.internal_state[0])
            self.out_state.reverse()

        self.output()
        return self.internal_state[0]


class TCounter(Component):
    def __init__(self, out_lights):
        super().__init__(out_lights)
        self.internal_state = [1,0,0,0,0]

    def update(self, counter_state):
        pos = to_int(counter_state)
        for i in range(len(self.internal_state)):
            if i == pos:
                self.internal_state[i] = 1
            else:
                self.internal_state[i] = 0
        self.out_state = self.internal_state
        self.output()

class Multiplexer(Component):
    def __init__(self):
        super().__init__(out_lights=[])
        self.instr_map = dict()
        self.fetch_map = dict()

    def set_instr_map(self, new_map):
        self.instr_map = new_map.copy()

    def set_fetch_map(self, new_map):
        self.fetch_map = new_map.copy()
    
    # Function to return the correct EEPROM
    # address for a given instruction and
    # timer state
    def apply(self, instr, state):
        # Build instruction key
        instr_key = [str(i) for i in instr]
        instr_key = ''.join(instr_key)
        # Build state key
        state_key = [str(i) for i in state]
        state_key = ''.join(state_key)
        # Build total key
        tot_key = instr_key + state_key

        # Check for fetch state
        if state_key in ['000','001']:
            return self.fetch_map[state_key]

        # Else process current instruction
        else:
            return self.instr_map[tot_key]



class EEPROM(Component):
    def __init__(self, out_lights=[]):
        super().__init__(out_lights=out_lights)
        self.internal_state = [[0 for i in range(8)] for j in range(11)]
        self.word_dict = {}

    def write(self, new_internal_state):
        self.internal_state = new_internal_state.copy()

    def read(self):
        return self.out_state

    def update(self, address):
        self.out_state = self.internal_state[address].copy()

    def get_instr_word(self, key_val):
        if not key_val in self.word_dict:
            raise Exception("Invalid key for EEPROM.")
        else:
            # Make sure to update the output state
            self.update(self.word_dict[key_val])
            instr_word = self.read()
            return instr_word


class RAM(Component):
    def __init__(self, out_lights=[]):
        super().__init__(out_lights=out_lights)
        self.internal_state = [[0 for i in range(8)] for i in range(16)]

    def set_out_state(self, address):
        self.out_state = self.internal_state[address]

    def read(self, address):
        self.set_out_state(address)
        self.output()
        return self.out_state

    def program(self, content):
        self.internal_state = content.copy()

    def write(self, address, new_internal_state):
        self.internal_state[address] = new_internal_state


class Bus(Component):
    def __init__(self):
        super().__init__(out_lights=[])
        self.internal_state = [0 for i in range(8)]

    def read(self):
        return self.internal_state

    def write(self, new_internal_state):
        self.internal_state = new_internal_state


class ProgramCounter(Component):
    def __init__(self, out_lights=[]):
        super().__init__(out_lights=out_lights)
        self.internal_state = '0b0000'
        self.out_state = [0, 0, 0, 0]

    def read(self):
        return self.out_state

    def update(self):
        self.increase()
        self.out_state = bin_split(self.internal_state)
    
    def increase(self):
        old_state = self.internal_state
        if old_state == '0b1111':
            self.internal_state = '0b0000'
        else:
            self.internal_state = bin_sum(old_state, '0b0001')


class MemoryAddress(Component):
    def __init__(self, out_lights=[]):
        super().__init__(out_lights=out_lights)
        self.internal_state = '0b0000'
        self.out_state = [0, 0, 0, 0]

    def read(self):
        return self.internal_state

    def write(self, new_state):
        self.internal_state = list_to_bin(new_state)
        self.out_state = new_state


class Register(Component):
    def __init__(self, out_lights=[]):
        super().__init__(out_lights=out_lights)
        self.internal_state = '0b00000000'
        self.out_state = [0, 0, 0, 0, 0, 0, 0, 0]

    def read(self):
        return self.internal_state

    def write(self, new_state):
        self.internal_state = list_to_bin(new_state)
        self.out_state = new_state


class ALU(Component):
    def __init__(self, out_lights=[]):
        super().__init__(out_lights=out_lights)
        self.internal_state = '0b00000000'
        self.out_state = [0, 0, 0, 0, 0, 0, 0, 0]

    def read(self):
        return self.internal_state

    def update(self, a, b):
        new_state = bin_sum(a, b, bits=8)
        self.internal_state = new_state
        self.out_state = bin_split(new_state)


class OutputRegister(Component):
    def __init__(self, out_lights=[]):
        super().__init__(out_lights=out_lights)
        self.internal_state = '0b00000000'
        self.out_state = [0, 0, 0, 0, 0, 0, 0, 0]

    def write(self, new_state):
        self.internal_state = list_to_bin(new_state)
        self.out_state = new_state

    def output(self):
        # Turn binary state into integer str
        int_state = str(to_int(self.internal_state))
        str_state = int_state.zfill(3)
        print(int_state, str_state)
        for i in range(3):
            s = str_state[i]
            self.out_lights[2-i].set_state(s)
