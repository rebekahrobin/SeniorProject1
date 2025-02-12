from djitellopy import Tello
import time

# Initialize and connect to Tello drone
print("Create Tello object")
tello = Tello()

print("Connect to Tello Drone")
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

print("Takeoff!")
tello.takeoff()
time.sleep(1)

# Travel distance parameters (adjust as needed)
vertical_distance = 100  # Vertical leg of the "L" in cm
horizontal_distance = 100  # Horizontal leg of the "L" in cm
speed = 20                # Drone speed in cm/s

"""
Flight Pattern (L):
   1
   |
   |
   |
   2------3
"""

# Step 1: Ascend vertically (the upright leg of the "L")
print("Move to position 2")
tello.go_xyz_speed(0, 0, vertical_distance, speed)
time.sleep(1)

# Step 2: Move horizontally to the right (the base of the "L")
print("Move to position 3")
tello.go_xyz_speed(0, horizontal_distance, 0, speed)
time.sleep(.5)

# Return to initial position (optional)
print("Returning to initial position")
tello.go_xyz_speed(0, -horizontal_distance, -vertical_distance, speed)
time.sleep(.5)

# Land the drone
print("Landing...")
tello.land()
print("Touchdown. Goodbye!")
