import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os
import sys
import random

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DesktopPet:
    def __init__(self):
        self.window = tk.Tk()
        self.window.iconbitmap(resource_path("pet.ico"))
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        self.trans_color = '#abcdef'
        self.window.wm_attributes('-transparentcolor', self.trans_color)
        self.window.config(bg=self.trans_color)

        self.base_w, self.base_h = 100, 100
        self.scale_factor = 1.0
        self.anim_offset = 0.0
        self.growing = True
        
        # Dirección: True para derecha, False para izquierda
        self.facing_right = True 
        
        self.auto_move = tk.BooleanVar(value=True)
        self.target_x, self.target_y = 500, 500
        self.screen_w = self.window.winfo_screenwidth()
        self.screen_h = self.window.winfo_screenheight()

        self.original_img = Image.open(resource_path("pet.png")).convert("RGBA")
        
        self.label = tk.Label(self.window, bg=self.trans_color, bd=0, highlightthickness=0)
        self.label.place(x=0, y=0, anchor='nw')

        self.label.bind('<Button-1>', self.start_drag)  
        self.label.bind('<B1-Motion>', self.do_drag)    
        self.label.bind('<Button-3>', self.show_menu) 

        self.animate()
        self.move_logic() 
        self.window.mainloop()

    def show_menu(self, event):
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Ajustar Tamaño", command=self.open_settings)
        menu.add_checkbutton(label="Movimiento Aleatorio", variable=self.auto_move)
        menu.add_separator()
        menu.add_command(label="Salir", command=self.window.destroy)
        menu.post(event.x_root, event.y_root)

    def open_settings(self):
        settings_win = tk.Toplevel(self.window)
        settings_win.title("Ajustes")
        settings_win.geometry("250x120")
        settings_win.attributes('-topmost', True)
        tk.Scale(settings_win, from_=0.5, to=3.0, resolution=0.1, orient='horizontal', 
                 label="Escala", command=lambda v: setattr(self, 'scale_factor', float(v))).pack(fill='x', padx=20)

    def move_logic(self):
        if self.auto_move.get():
            curr_x = self.window.winfo_x()
            curr_y = self.window.winfo_y()

            # Detectar nueva dirección antes de elegir nuevo destino
            if self.target_x > curr_x:
                self.facing_right = True
            elif self.target_x < curr_x:
                self.facing_right = False

            if abs(curr_x - self.target_x) < 5 and abs(curr_y - self.target_y) < 5:
                margin = int(100 * self.scale_factor)
                self.target_x = random.randint(0, self.screen_w - margin)
                self.target_y = random.randint(0, self.screen_h - margin)

            dx = 1 if self.target_x > curr_x else -1
            dy = 1 if self.target_y > curr_y else -1
            
            new_x = curr_x + (dx if abs(curr_x - self.target_x) > 0 else 0)
            new_y = curr_y + (dy if abs(curr_y - self.target_y) > 0 else 0)
            self.window.geometry(f"+{new_x}+{new_y}")

        self.window.after(60, self.move_logic)

    def animate(self):
        step = 0.5
        if self.growing:
            self.anim_offset += step
            if self.anim_offset > 5.0: self.growing = False
        else:
            self.anim_offset -= step
            if self.anim_offset < -5.0: self.growing = True

        final_w = int(self.base_w * self.scale_factor)
        final_h = int((self.base_h + self.anim_offset) * self.scale_factor)
        
        # PROCESAR IMAGEN: Redimensionar y luego voltear si es necesario
        img = self.original_img.resize((final_w, final_h), Image.Resampling.LANCZOS)
        
        if not self.facing_right:
            img = ImageOps.mirror(img) # Voltea la imagen horizontalmente
            
        self.photo = ImageTk.PhotoImage(img)
        self.window.geometry(f"{final_w}x{final_h}") 
        self.label.config(image=self.photo, width=final_w, height=final_h)
        self.window.after(80, self.animate)

    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y

    def do_drag(self, event):
        x = self.window.winfo_x() + (event.x - self.offset_x)
        y = self.window.winfo_y() + (event.y - self.offset_y)
        self.window.geometry(f"+{x}+{y}")
        self.target_x, self.target_y = x, y

if __name__ == "__main__":
    DesktopPet()