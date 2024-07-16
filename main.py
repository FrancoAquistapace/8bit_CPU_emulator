# In this file we specify the main script for
# running the application

# Import modules
import tkinter as tk
import time
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Import layout
from layout import *
from components import *
from window import *

# Emulator parameters
EMULATOR_TIME_SCALE = 100
DEFAULT_PERIOD = 0.5
RUNNING = False
HLT, MI, RI, RO, IO, II, AI, AO = 0, 0, 0, 0, 0, 0, 0, 0
EO, SU, BI, OI, CE, CO, CI, FI = 0, 0, 0, 0, 0, 0, 0, 0
EEPROM_ADDRESS = 0
RAM_ADDRESS = 0
DATA_ADDRESS = 0

# Create the clock and counters
clock = Clock(out_lights=[clock_light_meta], period=DEFAULT_PERIOD)
counter_comp = Counter(out_lights=extra_meta)
tcounter_comp = TCounter(out_lights=T_meta)
pcounter_comp = ProgramCounter(out_lights=prog_cnt_meta)

# Create the EEPROMs and Multiplexer
eeproms = [EEPROM(out_lights=[cont_wrd_meta[i] for i in range(8)]), 
           EEPROM(out_lights=[cont_wrd_meta[i+8] for i in range(8)])]

mplex_comp = Multiplexer()

# Create instruction register
inst_reg_comp = Register(out_lights=inst_reg_meta)

# Create A and B registers
areg_comp = Register(out_lights=areg_meta)
breg_comp = Register(out_lights=breg_meta)

# Create ALU
alu_comp = ALU(out_lights=alu_meta)

# Create the RAM and set some default program
ram_comp = RAM(out_lights=ram_meta)
ram_comp.write(0, [0,0,0,1,0,1,0,0]) # LDA [4]
ram_comp.write(1, [0,0,1,0,0,1,0,1]) # ADD [5]
ram_comp.write(2, [1,1,1,0,0,0,0,0]) # OUT
ram_comp.write(3, [1,1,1,1,0,0,0,0]) # HLT
ram_comp.write(4, [0,0,0,0,1,1,1,0]) # [4] 14
ram_comp.write(5, [0,0,0,1,1,1,0,0]) # [5] 28

# Create the memory address
mem_address_comp = MemoryAddress(out_lights=mem_address_meta)

# Create the output register
output_reg_comp = OutputRegister(out_lights=output_reg_meta)

# Create the Bus
bus_comp = Bus()

# Write default configuration for each EEPROM
eeproms[0].write([[0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 1, 0, 0], 
                  [0, 1, 0, 0, 1, 0, 0, 0], 
                  [0, 0, 0, 1, 0, 0, 1, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0]])

eeproms[1].write([[0, 0, 0, 0, 0, 1, 0, 0], 
                  [0, 0, 0, 0, 1, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 1, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0]])

# Write default multiplexer configuration
mplex_comp.set_fetch_map({'000': 0, '001': 1})
mplex_comp.set_instr_map(
    {'0001010': 2, # LDA - State 010
     '0001011': 3, # LDA - State 011
     '0001100': 4, # LDA - State 100
     '0010010': 2, # ADD - State 010
     '0010011': 5, # ADD - State 011
     '0010100': 6, # ADD - State 100
     '1110010': 7, # OUT - State 010
     '1110011': 9, # OUT - State 011
     '1110100': 9, # OUT - State 100
     '1111010': 8, # HLT - State 010
     '1111011': 9, # HLT - State 011
     '1111100': 9, # HLT - State 100
    })

# Init. prev. counter pos variable
PREV_COUNTER_POS = 0

# Main function
def run_cpu(root, canvas):
    global PREV_COUNTER_POS
    global EEPROM_ADDRESS
    global RAM_ADDRESS
    if RUNNING:
        # ----- Update state of the computer -------
        # Update clock
        clock_current = clock.update()
        # Update counter and Tcounter
        counter_pos = counter_comp.update(*clock_current)
        tcounter_comp.update(counter_pos)

        # Only operate once per counter pos
        if not counter_pos == PREV_COUNTER_POS:
            # Read line of instructions
            eeproms[0].update(EEPROM_ADDRESS)
            eeproms[0].output()
            HLT, MI, RI, RO, IO, II, AI, AO = eeproms[0].read()
            eeproms[1].update(EEPROM_ADDRESS)
            eeproms[1].output()
            EO, SU, BI, OI, CE, CO, CI, FI = eeproms[1].read()

            # Check for halt instruction
            if HLT:
                toggle_run(root, canvas)

            # CO -> (Output counter) Put prog. counter 
            # content on bus
            if CO:
                bus_content = [0 for i in range(4)]
                bus_content.extend(pcounter_comp.read())
                bus_comp.write(bus_content)

            # CE -> (Enable counter) Increase counter
            if CE: 
                pcounter_comp.update()
            pcounter_comp.output()

            # RO -> (RAM out) Read RAM into bus
            if RO:
                bus_comp.write(ram_comp.read(RAM_ADDRESS))

            # IO -> (Instr. register out) Put content on instr. 
            # register on bus
            if IO:
                bus_comp.write(bin_split(inst_reg_comp.read()))

            # AO -> (A register out) Read contents of reg.
            # A into the bus
            if AO:
                bus_comp.write(bin_split(areg_comp.read()))

            # EO -> (ALU out) Read the contents of the ALU to
            # the bus
            if EO:
                bus_comp.write(bin_split(alu_comp.read()))

            # OI -> (Output register in) Write to the output
            # register from bus
            if OI:
                output_reg_comp.write(bus_comp.read())
            output_reg_comp.output()

            # MI -> (Mem. address in) Write to memory address
            # from bus
            if MI:
                mem_address_comp.write(bus_comp.read()[4:])
                # Update our variable RAM address
                RAM_ADDRESS = to_int(mem_address_comp.read())
                ram_out = ram_comp.read(RAM_ADDRESS)
            mem_address_comp.output()

            # RI -> (RAM in) Write bus content into RAM at 
            # current address
            if RI:
                ram_comp.write(RAM_ADDRESS, bus_comp.read())

            # II -> (Instr. register in) Write content onto the
            # instr. register from the bus
            if II:
                inst_reg_comp.write(bus_comp.read())
            inst_reg_comp.output()

            # We update the EEPROM address by mapping the
            # instruction and the counter state
            ram_pcount = max(to_int(list_to_bin(pcounter_comp.read()))-1, 0)
            new_eeprom_instr = ram_comp.internal_state[ram_pcount][:4]
            new_eeprom_state = bin_split(counter_comp.read())
            EEPROM_ADDRESS = mplex_comp.apply(new_eeprom_instr, 
                                            new_eeprom_state)

            # AI -> (A register in) Write contents of bus
            # into register A
            if AI:
                areg_comp.write(bus_comp.read())

            # BI -> (B register in) Write contents of bus
            # into register B
            if BI:
                breg_comp.write(bus_comp.read())

            # Always update the ALU immediately after operating
            # on the A and B registers
            alu_comp.update(areg_comp.read(), breg_comp.read())
            alu_comp.output()
            areg_comp.output()
            breg_comp.output()

            # ------------------------------------------

            # Keep track of previous counter pos.
            PREV_COUNTER_POS = counter_pos


        # ------ Render computer lights ------------
        # Build all lights
        for l in all_lights:
            l.build(canvas)
        # ------------------------------------------

        root.after(EMULATOR_TIME_SCALE, run_cpu, root, canvas)


def toggle_run(root, canvas):
    global RUNNING

    if RUNNING:
        RUNNING = False
        run_meta.turn_off()
        run_meta.update(canvas, run_meta.off_c)
        prog_meta.turn_on()
        prog_meta.update(canvas, prog_meta.on_c)
        return
    else:
        RUNNING = True
        run_meta.turn_on()
        prog_meta.turn_off()
        run_cpu(root, canvas)
        return


def main():
    # ----- Window rendering ----------
    # Init window
    root = tk.Tk()
    root.title("Ben Eater's 8-bit CPU")
    root.geometry("1244x700")

    # Load the image file using Pillow
    image_pil = Image.open("background_img.png")
    image = ImageTk.PhotoImage(image_pil)

    # Create a canvas
    canvas_bg = tk.Canvas(root, width=1244, height=700)
    canvas_bg.pack()
    # Place the background image on the canvas
    canvas_bg.create_image(0, 0, anchor=tk.NW, image=image)
    # Create black background for output register lights
    output_width = 300
    output_height = int(output_width / 3)
    output_x = 860
    output_y = 570
    canvas_bg.create_rectangle(output_x, output_y, 
                               output_x + output_width,
                               output_y + output_height,
                               fill='black')
    # Check if we are running or not by default
    if RUNNING:
        run_meta.turn_on()
        prog_meta.turn_off()
    else:
        run_meta.turn_off()
        prog_meta.turn_on()
    # Build all lights
    for l in all_lights:
        l.build(canvas_bg)
    # Build number lights
    for l in output_reg_meta:
        l.build(canvas_bg)
    # -----------------------------------

    # ------ Check for user input --------------
    # Test button
    button = Button(root, "Run/Prog", 
                    command=lambda: toggle_run(root, canvas_bg),
                    pos=[300, 220])
    button.render(canvas_bg)

    # Pop up eeprom window and button
    eeprom_window = EEPROMWindow(root, eeproms[0], eeproms[1])
    eeprom_button = Button(root, "EEPROM", 
                    command=lambda: eeprom_window.open(),
                    pos=[500, 360])
    eeprom_button.render(canvas_bg)

    # Pop up RAM window and button
    ram_window = RAMWindow(root, ram_comp)
    ram_button = Button(root, "RAM", 
                    command=lambda: ram_window.open(),
                    pos=[500, 160])
    ram_button.render(canvas_bg)
    # ------------------------------------------

    # Run cpu
    run_cpu(root, canvas_bg)

    root.mainloop()

if __name__ == "__main__":
    main()