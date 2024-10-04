import cv2
import numpy as np
from tkinter import Tk, filedialog, Button, Label, Canvas, PhotoImage
from PIL import Image, ImageTk

# Artistic Filters Implementation
def apply_filter(image, filter_type):
    if filter_type == "neon":
        # Neon Effect (Edge detection + Inverted colors)
        edges = cv2.Canny(image, 100, 200)
        edges_inverted = cv2.bitwise_not(edges)
        return edges_inverted

    elif filter_type == "sw":
        # Black & White Filter
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    elif filter_type == "sepia":
        # Sepia Filter
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(image, kernel)
        sepia = np.clip(sepia, 0, 255)
        return sepia

    elif filter_type == "inverted":
        # Inverted Colors
        return cv2.bitwise_not(image)

    elif filter_type == "comic":
        # Comic Effect
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif filter_type == "glow":
        # Glow Effect (Gaussian blur + blending)
        blurred = cv2.GaussianBlur(image, (15, 15), 0)
        glow = cv2.addWeighted(image, 0.5, blurred, 0.5, 0)
        return glow

    else:
        return image

# GUI for the Application
def load_image():
    global img, tk_img, canvas
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        tk_img = ImageTk.PhotoImage(img_pil)
        canvas.create_image(0, 0, anchor='nw', image=tk_img)


def apply_selected_filter(filter_type):
    global img, tk_img, canvas
    if img is not None:
        filtered_img = apply_filter(img, filter_type)
        filtered_img_rgb = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(filtered_img_rgb)
        tk_img = ImageTk.PhotoImage(img_pil)
        canvas.create_image(0, 0, anchor='nw', image=tk_img)

# Main GUI Window
root = Tk()
root.title("Artistic Photo Filter App")
root.geometry("800x600")

img = None
tk_img = None

# Load Image Button
load_btn = Button(root, text="Load Image", command=load_image)
load_btn.pack()

# Filter Buttons
filters = ["neon", "sw", "sepia", "inverted", "comic", "glow"]
for filter_type in filters:
    btn = Button(root, text=filter_type.capitalize(), command=lambda f=filter_type: apply_selected_filter(f))
    btn.pack()

# Image Canvas
canvas = Canvas(root, width=800, height=450, bg="gray")
canvas.pack()

# Run the application
root.mainloop()
