# import time
# import os
# import cv2
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from log_manager import setup_logger, log_action

# logger = setup_logger()

# # Capture image when USB is inserted
# def capture_image(image_file="captured_image.jpg"):
#     camera = cv2.VideoCapture(0)
#     if not camera.isOpened():
#         log_action(logger, "Failed to open webcam.", level="error")
#         return

#     ret, frame = camera.read()
#     if ret:
#         cv2.imwrite(image_file, frame)
#         log_action(logger, f"Captured image saved to {image_file}.")
#         camera.release()
#     else:
#         log_action(logger, "Failed to capture image.", level="error")
#         camera.release()

# # USB event handler
# class USBEventHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         # Modify this to monitor USB device insertions dynamically
#         usb_drive_letter = "E:"  # Adjust this if USB is mounted elsewhere
#         if event.src_path.startswith(usb_drive_letter):
#             log_action(logger, "USB device inserted!")
#             capture_image()

# # Monitor USB devices dynamically (from a known path)
# def monitor_usb_events():
#     usb_drive_path = "F:\\"  # Modify this to match the drive letter
#     if not os.path.exists(usb_drive_path):
#         log_action(logger, f"Path {usb_drive_path} does not exist, monitoring won't work.")
#         return
    
#     event_handler = USBEventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, usb_drive_path, recursive=False)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

# def start_usb_monitoring():
#     monitor_usb_events()
