import os
import mss
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

from region_selector import RegionSelector
from tracker import MotionDetector, ObjectTracker
from bbox_utils import BoundingBoxProcessor

UNKNOWN_FOLDER = "dataset/unknown_class"

if not os.path.exists(UNKNOWN_FOLDER):
    os.makedirs(UNKNOWN_FOLDER)

img_counter = 0
saved_ids = set()

capture_active = False
capture_region = None

detector = MotionDetector()
tracker = ObjectTracker()
bbox = BoundingBoxProcessor()


def select_region():
    global capture_region
    
    selector = RegionSelector()
    
    if selector.region["width"] > 10 and selector.region["height"] > 10:
        capture_region = selector.region
        print("Selected Region:", capture_region)
    else:
        print("Invalid region selected. Drag a larger area.")
    
def start_capture():
    global capture_active
    capture_active = True
    print("Capture Started")
    
def stop_capture():
    global capture_active
    capture_active = False
    print("Capture Stopped")
    
with mss.mss() as sct:
    
    root = tk.Tk()
    root.title("AI Capture Control")
    
    btn_select = tk.Button(root, text="Select Area", command=select_region)
    btn_select.pack()
    
    btn_start = tk.Button(root, text="Start Capture", command=start_capture)
    btn_start.pack()
    
    btn_stop = tk.Button(root, text="Stop Capture", command=stop_capture)
    btn_stop.pack()
    
    video_label = tk.Label(root)
    video_label.pack()
    
    def update_frame():
        
        global img_counter
        
        if capture_active and capture_region is not None:
            
            screenshot = sct.grab(capture_region)
            
            frame = np.array(screenshot)[:, :, :3]
            
            gray = np.mean(frame, axis=2).astype(np.uint8)
            
            boxes = detector.detect(gray)
            
            tracked = tracker.update(boxes)
            
            for obj_id, box in tracked.items():
                
                frame = bbox.draw_box(frame, box)
                
                if obj_id not in saved_ids:
                    
                    crop = bbox.crop_object(frame, box)
                        
                    if crop.size > 0:
                        
                        img = Image.fromarray(crop.astype(np.uint8))
                        
                        filename = os.path.join(
                            UNKNOWN_FOLDER,
                            f"object_{img_counter}.png"
                        )
                        
                        img.save(filename)
                        
                        saved_ids.add(obj_id)
                        
                        img_counter += 1
                            
        else:
            frame = np.zeros((400,700,3), dtype=np.uint8)
            
            if capture_region:
                frame = np.zeros(
                    (capture_region["height"], capture_region["width"],3),
                    dtype=np.uint8
                )
            
        img = Image.fromarray(frame)
        
        img = img.resize((800, 450))
        
        tk_img = ImageTk.PhotoImage(img)
        
        video_label.config(image=tk_img)
        video_label.image = tk_img
        
        root.after(10, update_frame)
        
    update_frame()
    
    root.mainloop()