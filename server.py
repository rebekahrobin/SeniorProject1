import cv2
import asyncio
import base64
import websockets
import numpy as np
from flask import Flask, render_template

# 🔴 Change this to the camera index:
# 0 = Default Webcam (Integrated Camera)
# 1 or higher = External Camera (OBS Virtual Camera might be 1 or 2)
CAMERA_INDEX = 0  # Change to 1 or 2 if OBS Virtual Cam isn't detected

# Initialize Flask app
app = Flask(__name__)

# Open camera
cap = cv2.VideoCapture(CAMERA_INDEX)

# WebSocket clients list
clients = set()

# WebSocket server function
async def video_stream(websocket, path):
    global clients
    clients.add(websocket)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue  # Skip if frame not available

            frame = cv2.resize(frame, (640, 480))

            # Encode frame to base64
            _, buffer = cv2.imencode(".jpg", frame)
            frame_data = base64.b64encode(buffer).decode("utf-8")

            # Send frame to all connected clients
            await asyncio.gather(*[client.send(frame_data) for client in clients])

            await asyncio.sleep(0.03)  # Control frame rate

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        clients.remove(websocket)

# Start WebSocket server
async def start_websocket():
    async with websockets.serve(video_stream, "0.0.0.0", 8765):
        await asyncio.Future()  # Keep running

# Flask route to serve webpage
@app.route("/")
def index():
    return render_template("index.html")

# Run Flask and WebSocket in parallel
if __name__ == "__main__":
    import threading

    # Start WebSocket server in a separate thread
    threading.Thread(target=lambda: asyncio.run(start_websocket()), daemon=True).start()

    # Start Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
