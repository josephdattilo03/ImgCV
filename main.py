import cv2
import random
import mido
import time
import numpy as np

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
    """Capture video and control MIDI note and speed based on brightness, motion, and texture."""
    cap = cv2.VideoCapture(camera_idx)
    outport = mido.open_output(mido.get_output_names()[0])
    grounding_node_on = mido.Message("note_on", note=55, velocity=64)
    grounding_node_off = mido.Message("note_off", note=55, velocity=64)

    prev_gray = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Brightness via HSV
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        brightness = hsv_image[:, :, 2].mean()
        
        # Convert to grayscale for motion and texture
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- Texture detection via Laplacian ---
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        laplacian_var = laplacian.var()  # Variance of the Laplacian

        # Map Laplacian variance to MIDI velocity (1–127)
        # You might want to tune the divisor 100.0 depending on your camera and lighting
        velocity = int(np.clip((laplacian_var / 100.0) * 127, 1, 127))

        if prev_gray is None:
            prev_gray = gray_image
            continue

        # Frame difference
        frame_diff = cv2.absdiff(gray_image, prev_gray)
        motion_level = frame_diff.mean()

        prev_gray = gray_image.copy()

        # Map brightness to MIDI note
        midi_note = int((brightness / 255) * (115 - 55) + 55)

        # Sleep time based on motion
        min_sleep = 0.1
        max_sleep = 3.0
        normalized_motion = np.clip(motion_level / 50, 0, 1)
        sleep_time = max_sleep * (1 - normalized_motion) ** 3
        sleep_time = np.clip(sleep_time, min_sleep, max_sleep)

        print(f"midi_note: {midi_note}, velocity: {velocity}")
        print(f"brightness: {brightness:.2f}, motion_level: {motion_level:.2f}, laplacian_var: {laplacian_var:.2f}, sleep_time: {sleep_time:.2f}s")

        # Send MIDI messages
        note_on = mido.Message('note_on', note=int(midi_note), velocity=velocity)
        note_off = mido.Message('note_off', note=int(midi_note), velocity=velocity)
        
        outport.send(grounding_node_on)
        outport.send(grounding_node_off)
        outport.send(note_on)
        time.sleep(sleep_time)
        outport.send(note_off)

        # Show frame and Laplacian edges side by side
        # For visualization, scale Laplacian for display
        laplacian_display = cv2.convertScaleAbs(laplacian)
        combined = np.hstack((frame, cv2.cvtColor(laplacian_display, cv2.COLOR_GRAY2BGR)))
        cv2.imshow('Frame | Laplacian', combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




def main(video_capture_idx):
    start_video_stream(video_capture_idx)

def alternate_main():
    # Test function that plays fixed notes

    
    outport = mido.open_output(mido.get_output_names()[0])    
    while True:
        rand_note = random.randint(55, 115)
        random_note_on = mido.Message('note_on', note=55, velocity=rand_note)
        random_note_off = mido.Message('note_off', note=55, velocity=rand_note)
        outport.send(random_note_on)
        time.sleep(.3)
        outport.send(random_note_off)


    

if __name__ == "__main__":
    cameras = list_cameras()
    for idx, cam in enumerate(cameras):
        print(f"{idx}: Camera index {cam}")
    
    if not cameras:
        print("No cameras found!")
        exit()
    
    chosen_device = int(input("Select a device from the list above: "))
    # alternate_main()
    main(chosen_device)