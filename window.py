# Here we define the window elements, such as buttons

# Import modules
import tkinter as tk

# Button class with tk functionality
class Button():
    def __init__(self, root, text, command, pos):
        self.button = tk.Button(root, text=text, 
                       command=command)
        self.pos = pos

    def render(self, canvas):
        canvas.create_window(self.pos[0], self.pos[1], 
                             anchor="center", window=self.button)


# Specific button for the EEPROMS
class EEPROMButton(Button):
    def __init__(self, root, text, command, pos):
        super().__init__(root, text, command, pos)



# Popup window class to allow for access to the components
class PopupWindow():
    def __init__(self, root, geometry, title, label, label_pos):
        self.root = root
        self.geometry = geometry
        self.title = title
        self.label = label
        self.label_pos = label_pos

    def open(self):
        top = tk.Toplevel(self.root)
        top.geometry(self.geometry)
        top.title(self.title)
        self.label.place(x=self.label_pos[0],y=self.label_pos[1])


# Specific window for writting the EEPROMS
class EEPROMWindow(PopupWindow):
    def __init__(self, root, eeprom1, eeprom2, geometry="720x450", title="EEPROM Setup"):
        super().__init__(root, geometry, title, label=None, label_pos=None)
        self.eeprom1 = eeprom1
        self.eeprom2 = eeprom2
    
    def submit(self, content):
        internal_state_1 = []
        internal_state_2 = []
        for line in content:
            line_1 = []
            line_2 = []
            for i, entry in enumerate(line):
                if i < 8:
                    line_1.append(int(entry.get()))
                else:
                    line_2.append(int(entry.get()))
            internal_state_1.append(line_1)
            internal_state_2.append(line_2)

        # Write new contents to the EEPROMs
        self.eeprom1.write(internal_state_1)
        self.eeprom2.write(internal_state_2)   


    def open(self):
        top = tk.Toplevel(self.root)
        top.geometry(self.geometry)
        top.title(self.title)

        # Create a canvas
        canvas_top = tk.Canvas(top, width=720, height=450)
        #canvas_top.pack()

        # Create labels
        func_labels = ['HLT', 'MI', 'RI', 'RO', 'IO', 
                        'II', 'AI', 'AO', 'EO', 'SU',
                        'BI', 'OI', 'CE', 'CO', 'CI', 
                        'FI']
        top_labels = []
        for lab in func_labels:
            top_labels.append(tk.Label(top, text=lab))

        for i, new_label in enumerate(top_labels):
            new_label.grid(row=0, column=i, pady=2)

        # Data entries
        func_entries = []
        for j in range(11):
            entry_list = []
            for i, lab in enumerate(func_labels):
                new_entry = tk.Entry(top, width=3)
                new_entry.grid(row=j+1, column=i, pady=2)
                if i < 8:
                    val = self.eeprom1.internal_state[j][i]
                else:
                    val = self.eeprom2.internal_state[j][i-8]
                new_entry.insert(0, val) # Default value is 0
                entry_list.append(new_entry)
            func_entries.append(entry_list)

        # Submit button
        submit_button = Button(top, 'Apply', 
                                command=lambda: self.submit(func_entries),
                                pos=[20, 20])
        submit_button.button.grid(row=12, column=len(func_labels), pady=2)

# -----------------------------------------
# Specific window for writting the RAM
class RAMWindow(PopupWindow):
    def __init__(self, root, ram_comp, geometry="580x580", title="RAM Setup"):
        super().__init__(root, geometry, title, label=None, label_pos=None)
        self.ram_comp = ram_comp
    
    def submit(self, content):
        internal_state = []
        for line in content:
            line_ram = []
            for i, entry in enumerate(line):
                line_ram.append(int(entry.get()))
                
            internal_state.append(line_ram)

        # Write new contents to the RAM
        self.ram_comp.program(internal_state)

    def open(self):
        top = tk.Toplevel(self.root)
        top.geometry(self.geometry)
        top.title(self.title)

        # Create a canvas
        canvas_top = tk.Canvas(top, width=720, height=450)

        # Create labels
        func_labels = [str(i) for i in range(8)]
        top_labels = []
        for lab in func_labels:
            top_labels.append(tk.Label(top, text=lab))

        for i, new_label in enumerate(top_labels):
            new_label.grid(row=0, column=i, pady=2)

        # Data entries
        func_entries = []
        for j in range(16):
            entry_list = []
            for i, lab in enumerate(func_labels):
                new_entry = tk.Entry(top, width=3)
                new_entry.grid(row=j+1, column=i, pady=1)
                val = self.ram_comp.internal_state[j][i]
                new_entry.insert(0, val) # Default value is 0
                entry_list.append(new_entry)
            func_entries.append(entry_list)

        # Submit button
        submit_button = Button(top, 'Apply', 
                                command=lambda: self.submit(func_entries),
                                pos=[20, 20])
        submit_button.button.grid(row=12, column=len(func_labels), pady=2)

# -----------------------------------------
# Reference function to open a popup window
def open_popup(window, geometry="750x250", title="Child Window"):
   top= tk.Toplevel(window)
   top.geometry(geometry)
   top.title(title)
   tk.Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)