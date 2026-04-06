import numpy as np

class MotionDetector:
    
    def __init__(self, threshold=30, min_pixels=500):
        
        self.prev_frame = None
        self.threshold = threshold
        self.min_pixels = min_pixels
        
    def detect(self, frame):
        
        if self.prev_frame is None:
            self.prev_frame = frame
            return []
        
        diff = np.abs(frame.astype(np.int32) - self.prev_frame.astype(np.int32))
        
        motion_mask = diff > self.threshold
        
        objects = self.find_objects(motion_mask)
        
        self.prev_frame = frame
        
        return objects
    
    def find_objects(self, mask):
        
        visited = np.zeros(mask.shape, dtype=bool)
        objects = []
        
        h, w = mask.shape
        
        for y in range(h):
            for x in range(w):
                
                if mask[y, x] and not visited[y, x]:
                    
                    stack = [(y, x)]
                    pixels = []
                    visited[y, x] = True
                    
                    while stack:
                        
                        cy, cx = stack.pop()
                        pixels.append((cy, cx))
                        
                        for ny in range(cy - 1, cy + 2):
                            for nx in range(cx - 1, cx + 2):
                                
                                if 0 <= ny < h and 0 <= nx < w:
                                    
                                    if mask[ny, nx] and not visited[ny, nx]:
                                        
                                        visited[ny, nx] = True
                                        stack.append((ny, nx))
                                        
                    if len(pixels) > self.min_pixels:
                        
                        ys = [p[0] for p in pixels]
                        xs = [p[1] for p in pixels]
                        
                        box = (
                            min(xs),
                            min(ys),
                            max(xs),
                            max(ys)
                        )
                        
                        objects.append(box)
                            
        return objects
                
class ObjectTracker:
    
    def __init__(self, max_distance=50):
        
        self.objects = {}
        self.next_id = 0
        self.max_distance = max_distance
        
    def update(self, boxes):
        
        updated = {}
        
        for box in boxes:
            
            cx = (box[0] + box[2]) // 2
            cy = (box[1] + box[3]) // 2
            
            matched = None
            
            for obj_id, (px, py) in self.objects.items():
                
                dist = np.sqrt((cx - px)**2 + (cy - py)**2)
                
                if dist < self.max_distance:
                    matched = obj_id
                    break
                
            if matched is None:
                
                matched = self.next_id
                self.next_id += 1
                
            updated[matched] = (cx, cy)
            
        self.objects = updated
        
        return updated
    
    
            