import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def main():
    root = tk.Tk()
    root.title("Tkinter Background Image Example")

    root.geometry("1244x700")

    # Load the image file using Pillow
    image_pil = Image.open("background_img.png")
    image = ImageTk.PhotoImage(image_pil)

    # Create a label with the image as the background
    background_label = tk.Label(root, image=image)
    background_label.place(relwidth=1, relheight=1)

    # Add other widgets on top of the background
    label = tk.Label(root, text="Hello, Tkinter!", font=("Helvetica", 16))
    label.pack(pady=20)

    button = tk.Button(root, text="Click Me", command=lambda: print("Button Clicked"))
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()