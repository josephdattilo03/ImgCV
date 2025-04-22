import AVFoundation as AVF
import cv2

def list_macos_cameras():
    devices = AVF.AVCaptureDevice.devices()
    return [(idx, d.localizedName()) for idx, d in enumerate(devices)]

def start_video_stream(device_index):
    # Set up the session correctly
    session = AVF.AVCaptureSession.alloc().init()

    # Get the device (camera)
    devices = AVF.AVCaptureDevice.devices()
    camera_device = devices[device_index]

    # Create input from the camera device
    device_input, error = AVF.AVCaptureDeviceInput.deviceInputWithDevice_error_(camera_device, None)
    if error:
        print("Error creating device input:", error)
        return

    # Add input to session
    session.addInput_(device_input)

    # Create output and add to session
    video_output = AVF.AVCaptureVideoDataOutput.alloc().init()
    session.addOutput_(video_output)

    # Set up a callback for the video data
    def video_data_output_callback(sample_buffer, connection):
        # Here we would process the sample buffer to get the frame data
        # Convert sample_buffer to OpenCV format
        # You can extract pixel data from the buffer and convert it to a numpy array for further processing
        pass

    # Start the session
    session.startRunning()

    print("Streaming... Press 'q' to quit.")
    while True:
        # Wait for frames
        print("hey")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    session.stopRunning()