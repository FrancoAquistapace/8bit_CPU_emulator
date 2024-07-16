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

    def update(self, canvas, color):
        # Update canvas object
        canvas.itemconfig(self.obj, fill=color)

    def toggle(self, canvas):
        if self.state == 0:
            self.state += 1
            color = self.on_c
        else:
            self.state -= 1
            color = self.off_c
        self.update(canvas, color)

    def turn_on(self):
        self.state = 1

    def turn_off(self):
        self.state = 0
        
    def set_state(self, new_state):
        self.state = new_state


class NumberLight(object):
    def __init__(self, x, y, on_c):
        self.x = x
        self.y = y
        self.state = 'o'
        self.off_c = 'black'
        self.on_c = on_c
        self.obj = None

    def build(self, canvas):
        if self.state == 'o':
            color = self.off_c
        else:
            color = self.on_c

        # Delete previous text
        if self.obj != None:
            canvas.delete(self.obj)
        
        self.obj = canvas.create_text(
                        self.x, self.y,
                        text=self.state, 
                        fill=color,
                        font=('Helvetica 90 bold'))

    def set_state(self, new_state):
        self.state = new_state

    def update(self, canvas):
        # Update color
        if self.state == 'o':
            color = self.off_c
        else:
            color = self.on_c
        # Update canvas object
        canvas.itemconfig(self.obj, fill=color, text=self.state)


# Define clock light
clock_on_c = CYAN_ON
clock_off_c = CYAN_OFF
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


# Define instruction register lights
inst_reg_on_c = [CYAN_ON for i in range(4)]
inst_reg_on_c.extend([YELLOW_ON for i in range(4)])
inst_reg_off_c = [CYAN_OFF for i in range(4)]
inst_reg_off_c.extend([YELLOW_OFF for i in range(4)])
inst_reg_x_arr = [450 + i*30 for i in range(8)]
inst_reg_meta = [Light(x=inst_reg_x_arr[i], y=400, r=LIGHT_R, 
                    off_c=inst_reg_off_c[i], 
                    on_c=inst_reg_on_c[i]) for i in range(8)]


# Add run and prog lights
run_on_c = GREEN_ON
run_off_c = GREEN_OFF
run_meta = Light(x=125, y=220, r=LIGHT_R,
                    off_c=run_off_c,
                    on_c=run_on_c)

prog_on_c = RED_ON
prog_off_c = RED_OFF
prog_meta = Light(x=180, y=220, r=LIGHT_R,
                    off_c=prog_off_c,
                    on_c=prog_on_c)


# Add T and extra lights
T_on_c = GREEN_ON
T_off_c = GREEN_OFF
T_x_arr = [160 + i*37 for i in range(5)]
T_meta = [Light(x=x, y=435, r=LIGHT_R, 
                off_c=T_off_c, 
                on_c=T_on_c) for x in T_x_arr]


# Add extra lights
extra_on_c = RED_ON
extra_off_c = RED_OFF
extra_x_arr = [40 + i*30 for i in range(3)]
extra_meta = [Light(x=x, y=435, r=LIGHT_R, 
                off_c=extra_off_c, 
                on_c=extra_on_c) for x in extra_x_arr]


# Get all lights into an overall array
all_lights = [clock_light_meta]
all_lights.extend(mem_address_meta)
all_lights.extend(cont_wrd_meta)
all_lights.extend(bus_meta)
all_lights.extend(ram_meta)
all_lights.extend(alu_meta)
all_lights.extend(areg_meta)
all_lights.extend(breg_meta)
all_lights.extend(prog_cnt_meta)
all_lights.extend(flags_meta)
all_lights.extend(inst_reg_meta)
all_lights.append(run_meta)
all_lights.append(prog_meta)
all_lights.extend(T_meta)
all_lights.extend(extra_meta)


# Define output register number lights
output_reg_meta = [NumberLight(1120 - i*100, 620, RED_OFF) for i in range(3)]
all_lights.extend(output_reg_meta)