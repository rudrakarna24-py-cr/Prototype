import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

def convert_images(files, output_dir, target_format):
    converted = 0
    
    for file in files:
        try:
            with Image.open(file) as img:
                
                filename = os.path.splitext(os.path.basename(file))[0]
                
                if target_format.upper() == "JPG":
                    save_format = "JPEG"
                else:
                    save_format = target_format.upper()
                    
                output_file = os.path.join(
                    output_dir,
                    f"{filename}.{target_format.lower()}"
                )
                
                if save_format == "JPEG" and img.mode != "RGB":
                    img = img.convert("RGB")
                    
                img.save(output_file, save_format)
                
                converted += 1
                
        except Exception as e:
            print(f"Error converting {file}: {e}")
            
    messagebox.showinfo("Done", f"{converted} images converted successfully!")
    
def bulk_convert():
    folder = filedialog.askdirectory()
    files = [os.path.join(folder, f) for f in os.listdir(folder)
             if f.lower().endswith(('.png','.jpg','.jpeg','.webp','.bmp','.tiff'))]
    
    if not files:
        return
    
    output_dir = filedialog.askdirectory(title="Select Output Folder")
    
    if not output_dir:
        return
    
    format_window = tk.Toplevel(root)
    format_window.title("Select Format")
    format_window.geometry("300x150")
    
    tk.Label(format_window, text="Convert To Format:").pack(pady=10)
    
    format_var = tk.StringVar(value="JPEG")
    
    formats = ["JPG","JPEG", "PNG", "WEBP", "BMP", "TIFF"]
    
    dropdown = ttk.Combobox(format_window, textvariable=format_var, values=formats)
    dropdown.pack(pady=5)
    
    def start_convertion():
        target_format = format_var.get()
        convert_images(files, output_dir, target_format)
        format_window.destroy()
        
    tk.Button(format_window, text="Covert", command=start_convertion).pack(pady=10)
    
# Main window
root = tk.Tk()
root.title("Bulk Image Format Converter")
root.geometry("400x200")

tk.Label(root, text="Select Images and Converter", font=("Arial", 16)).pack(pady=20)

tk.Button(root, text="Select Images and Convert", command=bulk_convert).pack()

root.mainloop()