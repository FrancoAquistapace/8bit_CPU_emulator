# In this file we specify some layout elements 
# for the main emulator window

# Import modules
import tkinter as tk

# Global params
LIGHT_R = 10
YELLOW_ON = '#f8f0bd'
YELLOW_OFF = '#eeda5b'
CYAN_ON = '#eff5f9'
CYAN_OFF = '#b0cfe4'
RED_ON = '#efa9ad'
RED_OFF = '#d82932'
GREEN_ON = '#99e9d5'
GREEN_OFF = '#00c897'

# Define light class
class Light(object):
    def __init__(self, x, y, r, on_c, off_c):
        self.x = x
        self.y = y
        self.r = r
        self.state = 0
        self.off_c = off_c
        self.on_c = on_c

    def build(self, canvas):
        if self.state == 0:
            color = self.off_c
        else:
            color = self.on_c
        self.obj = canvas.create_oval(
                                self.x - self.r, 
                                self.y - self.r, 
                                self.x + self.r, 
                                self.y + self.r, 
                                fill=color)

    def toggle(self, canvas):
        if self.state == 0:
            self.state += 1
            color = self.on_c
        else:
            self.state -= 1
            color = self.off_c
        # Update canvas object
        canvas.itemconfig(self.obj, fill=color)


# Define clock light
clock_on_c = YELLOW_ON
clock_off_c = YELLOW_OFF
clock_light_meta = Light(x=355, y=70, r=LIGHT_R, 
                        off_c=clock_off_c, on_c=clock_on_c)

# Define memory address lights
mem_address_on_c = YELLOW_ON
mem_address_off_c = YELLOW_OFF
mem_address_x_arr = [595 + i*30 for i in range(4)]
mem_address_meta = [Light(x=x, y=85, r=LIGHT_R,
                          off_c=mem_address_off_c, 
                          on_c=mem_address_on_c) for x in mem_address_x_arr]


# Define control word lights
cont_wrd_on_c = CYAN_ON
cont_wrd_off_c = CYAN_OFF
cont_wrd_x_arr = [56 + i*37.33 for i in range(16)]
cont_wrd_meta = [Light(x=x, y=550, r=LIGHT_R,
                          off_c=cont_wrd_off_c, 
                          on_c=cont_wrd_on_c) for x in cont_wrd_x_arr]


# Define bus lights
bus_on_c = RED_ON
bus_off_c = RED_OFF
bus_x_arr = [800 + i*30 for i in range(8)]
bus_meta = [Light(x=x, y=35, r=LIGHT_R, 
                    off_c=bus_off_c, 
                    on_c=bus_on_c) for x in bus_x_arr]


# Define RAM lights
ram_on_c = RED_ON
ram_off_c = RED_OFF
ram_x_arr = [440 + i*30 for i in range(8)]
ram_meta = [Light(x=x, y=212, r=LIGHT_R, 
                    off_c=ram_off_c, 
                    on_c=ram_on_c) for x in ram_x_arr]


# Define ALU lights
alu_on_c = RED_ON
alu_off_c = RED_OFF
alu_x_arr = [840 + i*30 for i in range(8)]
alu_meta = [Light(x=x, y=350, r=LIGHT_R, 
                    off_c=alu_off_c, 
                    on_c=alu_on_c) for x in alu_x_arr]


# Define A and B register lights
reg_on_c = RED_ON
reg_off_c = RED_OFF
reg_x_arr = [885 + i*30 for i in range(8)]
areg_meta = [Light(x=x, y=218, r=LIGHT_R, 
                    off_c=reg_off_c, 
                    on_c=reg_on_c) for x in reg_x_arr]
breg_meta = [Light(x=x, y=480, r=LIGHT_R, 
                    off_c=reg_off_c, 
                    on_c=reg_on_c) for x in reg_x_arr]


# Define program counter lights
prog_cnt_on_c = GREEN_ON
prog_cnt_off_c = GREEN_OFF
prog_cnt_x_arr = [1095 + i*30 for i in range(4)]
prog_cnt_meta = [Light(x=x, y=115, r=LIGHT_R, 
                    off_c=prog_cnt_off_c, 
                    on_c=prog_cnt_on_c) for x in prog_cnt_x_arr]


# Define flags lights
flags_on_c = GREEN_ON
flags_off_c = GREEN_OFF
flags_y_arr = [335 + i*30 for i in range(2)]
flags_meta = [Light(x=1180, y=y, r=LIGHT_R, 
                    off_c=flags_off_c, 
                    on_c=flags_on_c) for y in flags_y_arr]