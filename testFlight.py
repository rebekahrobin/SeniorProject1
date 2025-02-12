import cv2 # type: ignore
import time
from djitellopy import Tello

# Initialize the Tello drone
tello = Tello()

# Connect to the Tello drone
print("Connecting to Tello...")
try:
    tello.connect()
    if tello.is_connected():
        print("Connected to Tello successfully!")
        print(f"Battery level: {tello.get_battery()}%")
except Exception as e:
    print(f"Failed to connect to Tello: {e}")
    exit()

# Start the video stream
try:
    tello.streamon()
    print("Video stream started.")
except Exception as e:
    print(f"Failed to start video stream: {e}")
    tello.end()
    exit()

# Function to display video stream
def display_video():
    print("Press 'q' to exit the video stream.")
    while True:
        frame_read = tello.get_frame_read()
        frame = frame_read.frame

        # Convert the frame from BGR to RGB to fix the color issue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the video feed
        cv2.imshow('Tello Video Stream', frame_rgb)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting video stream...")
            break

# Main flight and video logic
try:
    print("Taking off...")
    tello.takeoff()

    # Hover for 5 seconds while showing video stream
    print("Hovering and showing video...")
    time.sleep(2)  # Let the drone stabilize

    # Display video stream
    display_video()

    print("Landing...")
    tello.land()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Stop the video stream and cleanup
    tello.streamoff()
    cv2.destroyAllWindows()
    tello.end()
    print("Cleaned up resources.")