import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

# FUNCIÓN CRUCIAL: Localiza archivos dentro del .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DesktopPet:
    def __init__(self):
        self.window = tk.Tk()
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'black')

        self.base_width = 100
        self.base_height = 100
        self.current_height = 100
        self.growing = True

        # USAMOS resource_path para cargar la imagen
        image_path = resource_path("pet.png")
        self.original_img = Image.open(image_path).convert("RGBA")
        
        self.label = tk.Label(self.window, bg='black', bd=0, highlightthickness=0, anchor='s')
        self.label.pack(fill='both', expand=True)

        self.label.bind('<Button-1>', self.start_drag)  
        self.label.bind('<B1-Motion>', self.do_drag)    
        self.label.bind('<Button-3>', lambda e: self.window.destroy()) 

        self.window.geometry(f"{self.base_width}x{self.base_height + 10}+500+500")
        
        self.animate()
        self.window.mainloop()

    def animate(self):
        if self.growing:
            self.current_height += 1
            if self.current_height > 105: self.growing = False
        else:
            self.current_height -= 1
            if self.current_height < 95: self.growing = True

        resized_img = self.original_img.resize((self.base_width, self.current_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_img)
        self.label.config(image=self.photo)
        self.window.after(100, self.animate)

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event):
        x = self.window.winfo_x() + (event.x - self.offset_x)
        y = self.window.winfo_y() + (event.y - self.offset_y)
        self.window.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    DesktopPet()