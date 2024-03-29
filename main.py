# In this file we specify the main script for
# running the application

# Import modules
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Import layout
from layout import *


def main():
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

    # Draw clock light
    clock_light_meta.build(canvas_bg)

    # Draw mem address lights
    for l in mem_address_meta:
        l.build(canvas_bg)

    # Draw control word lights
    for l in cont_wrd_meta:
        l.build(canvas_bg)

    # Draw bus lights
    for l in bus_meta:
        l.build(canvas_bg)

    # Draw RAM lights
    for l in ram_meta:
        l.build(canvas_bg)

    # Draw ALU lights
    for l in alu_meta:
        l.build(canvas_bg)

    # Draw A register lights
    for l in areg_meta:
        l.build(canvas_bg)

    # Draw B register lights
    for l in breg_meta:
        l.build(canvas_bg)

    # Draw program counter lights
    for l in prog_cnt_meta:
        l.build(canvas_bg)

    # Draw flags lights
    for l in flags_meta:
        l.build(canvas_bg)

    # Draw instruction register lights
    for l in inst_reg_meta:
        l.build(canvas_bg)

    # Draw run and prog lights
    run_meta.build(canvas_bg)
    prog_meta.build(canvas_bg)

    # Draw T lights
    for l in T_meta:
        l.build(canvas_bg)

    # Draw extra lights
    for l in extra_meta:
        l.build(canvas_bg)

    # Create a button and add it on top of the background image
    button = tk.Button(root, text="Click Me", 
                       command=lambda: clock_light_meta.toggle(canvas_bg))
    button_window = canvas_bg.create_window(300, 220, anchor="center", window=button)

    root.mainloop()

if __name__ == "__main__":
    main()