import tkinter as tk

class RegionSelector:
    
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.region = None
        
        self.root = tk.Tk()
        
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.configure(bg="black")
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray")
        self.canvas.pack(fill="both", expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.root.mainloop()
        
    def on_press(self, event):
        
        self.start_x = self.root.winfo_pointerx()
        self.start_y = self.root.winfo_pointery()
        
        self.rect = self.canvas.create_rectangle(
            event.x, event.y,
            event.x, event.y,
            outline="red", 
            width=2
        )
        
    def on_drag(self, event):
        self.canvas.coords(
            self.rect,
            self.canvas.canvasx(event.x),
            self.canvas.canvasy(event.y),
            event.x,
            event.y
                           )
        
    def on_release(self, event):
        
        end_x = self.root.winfo_pointerx()
        end_y = self.root.winfo_pointery()
        
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        self.region = {
            "top": y1,
            "left": x1,
            "width": x2 - x1,
            "height": y2 - y1
        }
        
        self.root.destroy()
        