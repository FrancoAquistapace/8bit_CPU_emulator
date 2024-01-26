# In this file we specify some layout elements 
# for the main emulator window

# Import modules
import tkinter as tk

# Global params
LIGHT_R = 10

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
clock_on_c = '#eff5f9'
clock_off_c = '#b0cfe4'
clock_light_meta = Light(x=355, y=70, r=LIGHT_R, 
                        off_c=clock_off_c, on_c=clock_on_c)

# Define memory address lights
mem_address_on_c = '#f8f0bd'
mem_address_off_c = '#eeda5b'
mem_address_x_arr = [595 + i*30 for i in range(4)]
mem_address_meta = [Light(x=x, y=85, r=LIGHT_R,
                          off_c=mem_address_off_c, 
                          on_c=mem_address_on_c) for x in mem_address_x_arr]


# Define control word lights
cont_wrd_on_c = '#eff5f9'
cont_wrd_off_c = '#b0cfe4'
cont_wrd_x_arr = [56 + i*37.33 for i in range(16)]
cont_wrd_meta = [Light(x=x, y=550, r=LIGHT_R,
                          off_c=cont_wrd_off_c, 
                          on_c=cont_wrd_on_c) for x in cont_wrd_x_arr]


# Define bus lights
bus_on_c = '#da9999'
bus_off_c = '#a30000'
bus_x_arr = [800 + i*30 for i in range(8)]
bus_meta = [Light(x=x, y=35, r=LIGHT_R, 
                    off_c=bus_off_c, 
                    on_c=bus_on_c) for x in bus_x_arr]