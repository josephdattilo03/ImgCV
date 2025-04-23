import cv2
import random

def list_cameras():
    """List available cameras by testing indices"""
    index = 0
    cameras = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            cameras.append(index)
        cap.release()
        index += 1
    return cameras

def condense_frame(frame, block_size=8):
    # Get dimensions and ensure they're divisible by block_size
    h, w = frame.shape[:2]
    h_new = h // block_size
    w_new = w // block_size
    
    # Trim frame if not divisible
    frame = frame[:h_new * block_size, :w_new * block_size]
    
    # Reshape into blocks and take mean
    if len(frame.shape) == 3:  
        condensed = frame.reshape(h_new, block_size, w_new, block_size, -1).mean(axis=(1, 3))
    else:  
        condensed = frame.reshape(h_new, block_size, w_new, block_size).mean(axis=(1, 3))
    
    return condensed.astype(frame.dtype)

def start_video_stream(camera_idx):
    """Capture video and print 2D grayscale arrays"""
    cap = cv2.VideoCapture(camera_idx)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        compressed = condense_frame(frame)
        h, w, _ = compressed.shape  # h = rows (height), w = columns (width)
        
        # Get random row and column indices
        random_row_idx = random.randint(0, h-1)
        random_col_idx = random.randint(0, w-1)
        
        # Access the random pixel correctly
        random_pixel = compressed[random_row_idx, random_col_idx]
        print(random_pixel)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def main(video_capture_idx):
    start_video_stream(video_capture_idx)

if __name__ == "__main__":
    cameras = list_cameras()
    for idx, cam in enumerate(cameras):
        print(f"{idx}: Camera index {cam}")
    
    if not cameras:
        print("No cameras found!")
        exit()
    
    chosen_device = int(input("Select a device from the list above: "))
    main(chosen_device)