import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import cv2
import time
import threading

# Dummy user data (for demonstration purposes)
users = {"admin": "password123"}

# Function to disable USB ports
def disable_usb():
    try:
        os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 4 /f")
        messagebox.showinfo("Success", "USB access has been disabled.")
    except Exception as e:
        messagebox.showerror("Error", f"Error disabling USB: {e}")

# Function to enable USB ports
def enable_usb():
    try:
        os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 3 /f")
        messagebox.showinfo("Success", "USB access has been enabled.")
    except Exception as e:
        messagebox.showerror("Error", f"Error enabling USB: {e}")

# Function for login authentication
def authenticate(username, password, root, login_frame):
    if username in users and users[username] == password:
        messagebox.showinfo("Welcome", "Login Successful!")
        login_frame.destroy()
        main_screen(root)
        start_usb_monitoring()  # Start USB monitoring after successful login
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# Function for user registration
def register_user(username, password, confirm_password):
    if username in users:
        messagebox.showerror("Error", "User already exists!")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
    else:
        users[username] = password
        messagebox.showinfo("Success", "User registered successfully!")

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    if not is_fullscreen:
        root.geometry("800x600")  # Default window size for small screen
    return "break"

# Function to exit fullscreen
def exit_fullscreen(event=None):
    global is_fullscreen
    if is_fullscreen:
        toggle_fullscreen()

# Function to monitor USB device insertions
def start_usb_monitoring():
    threading.Thread(target=usb_insertion_monitor, daemon=True).start()

# USB device insertion monitor
def usb_insertion_monitor():
    previous_usb_count = get_usb_device_count()  # Get initial USB device count
    while True:
        time.sleep(5)  # Check every 5 seconds for device insertions
        current_usb_count = get_usb_device_count()  # Get current USB device count
        
        if current_usb_count > previous_usb_count:  # If a new USB device is inserted
            capture_photo()  # Capture a photo when a new USB device is inserted
            previous_usb_count = current_usb_count  # Update the USB count

# Function to capture a photo using the webcam
def capture_photo():
    try:
        camera = cv2.VideoCapture(0)  # Access the default webcam
        if not camera.isOpened():
            messagebox.showerror("Error", "Could not access the camera.")
            return
        
        ret, frame = camera.read()  # Capture an image
        if ret:
            filename = "usb_insertion.jpg"  # Save photo as usb_insertion.jpg
            cv2.imwrite(filename, frame)  # Save to disk
            messagebox.showinfo("Photo Captured", "A photo has been taken and saved as 'usb_insertion.jpg'")
        camera.release()  # Release the camera resources
    except Exception as e:
        messagebox.showerror("Error", f"Error capturing photo: {e}")

# Function to get the number of connected USB devices
def get_usb_device_count():
    try:
        output = subprocess.check_output('wmic path Win32_USBHub get DeviceID', shell=True)
        return len(output.decode().splitlines()) - 1  # Subtract 1 to avoid header counting
    except Exception as e:
        print(f"Error checking USB devices: {e}")
        return 0

# Login Screen
def login_screen(root):
    root.title("USB Security Manager - Login")
    root.configure(bg="#f5f5f5")
    root.bind("<F11>", toggle_fullscreen)  # Toggle fullscreen with F11 key
    root.bind("<Escape>", exit_fullscreen)  # Exit fullscreen with Escape key

    login_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(login_frame, text="Login", font=("Arial", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(login_frame, text="Username:", bg="#ffffff").grid(row=1, column=0, sticky="w")
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=1, column=1)

    tk.Label(login_frame, text="Password:", bg="#ffffff").grid(row=2, column=0, sticky="w")
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=2, column=1)

    login_button = tk.Button(
        login_frame, text="Login",
        command=lambda: authenticate(username_entry.get(), password_entry.get(), root, login_frame),
        bg="#007BFF", fg="#ffffff", padx=10, pady=5
    )
    login_button.grid(row=3, column=0, columnspan=2, pady=10)

    register_button = tk.Button(
        login_frame, text="Register",
        command=lambda: register_screen(root),
        bg="#6c757d", fg="#ffffff", padx=10, pady=5
    )
    register_button.grid(row=4, column=0, columnspan=2, pady=5)

# Register Screen
def register_screen(root):
    root.title("USB Security Manager - Register")
    root.configure(bg="#f5f5f5")

    register_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
    register_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(register_frame, text="Register", font=("Arial", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(register_frame, text="Username:", bg="#ffffff").grid(row=1, column=0, sticky="w")
    username_entry = tk.Entry(register_frame)
    username_entry.grid(row=1, column=1)

    tk.Label(register_frame, text="Password:", bg="#ffffff").grid(row=2, column=0, sticky="w")
    password_entry = tk.Entry(register_frame, show="*")
    password_entry.grid(row=2, column=1)

    tk.Label(register_frame, text="Confirm Password:", bg="#ffffff").grid(row=3, column=0, sticky="w")
    confirm_password_entry = tk.Entry(register_frame, show="*")
    confirm_password_entry.grid(row=3, column=1)

    register_button = tk.Button(
        register_frame, text="Register",
        command=lambda: register_user(username_entry.get(), password_entry.get(), confirm_password_entry.get()),
        bg="#28A745", fg="#ffffff", padx=10, pady=5
    )
    register_button.grid(row=4, column=0, columnspan=2, pady=10)

    back_button = tk.Button(
        register_frame, text="Back to Login",
        command=lambda: [register_frame.destroy(), login_screen(root)],
        bg="#6c757d", fg="#ffffff", padx=10, pady=5
    )
    back_button.grid(row=5, column=0, columnspan=2, pady=5)

# Main Screen
def main_screen(root):
    root.title("USB Security Manager")
    root.configure(bg="#212529")

    header_label = tk.Label(root, text="USB Security Manager", font=("Arial", 18, "bold"), bg="#212529", fg="#ffffff")
    header_label.pack(pady=10)

    disable_button = tk.Button(root, text="Disable USB Ports", command=disable_usb, bg="#DC3545", fg="#ffffff", padx=10, pady=5)
    disable_button.pack(pady=10)

    enable_button = tk.Button(root, text="Enable USB Ports", command=enable_usb, bg="#28A745", fg="#ffffff", padx=10, pady=5)
    enable_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="#6c757d", fg="#ffffff", padx=10, pady=5)
    exit_button.pack(pady=20)

# Run Application
if __name__ == "__main__":
    global root, is_fullscreen
    is_fullscreen = False
    root = tk.Tk()
    login_screen(root)
    root.mainloop()
