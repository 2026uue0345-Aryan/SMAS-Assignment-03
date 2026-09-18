import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import numpy as np


class ImageTransformationToolbox:

    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Image Transformation Toolbox")
        self.root.geometry("1000x750")

        # Store images
        self.original_image = None
        self.current_image = None
        self.display_image = None

        # Title
        title = tk.Label(
            root,
            text="Interactive Image Transformation Toolbox",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Upload Image",
            command=self.upload_image,
            width=15
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Rotate",
            command=self.rotate,
            width=12
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Resize",
            command=self.resize,
            width=12
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Flip",
            command=self.flip,
            width=12
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Shear",
            command=self.shear,
            width=12
        ).grid(row=0, column=4, padx=5)

        tk.Button(
            button_frame,
            text="Custom Matrix",
            command=self.custom_matrix,
            width=15
        ).grid(row=0, column=5, padx=5)

        tk.Button(
            button_frame,
            text="Reset",
            command=self.reset,
            width=12
        ).grid(row=0, column=6, padx=5)

        # Image display area
        self.image_label = tk.Label(
            root,
            text="Please upload an image",
            font=("Arial", 14),
            relief="sunken",
            width=80,
            height=30
        )

        self.image_label.pack(padx=20, pady=20)

        # Status
        self.status_label = tk.Label(
            root,
            text="No image loaded",
            font=("Arial", 11)
        )
        self.status_label.pack(pady=5)

    # --------------------------------------------------
    # Upload Image
    # --------------------------------------------------

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png"),
                ("JPG Files", "*.jpg"),
                ("PNG Files", "*.png")
            ]
        )

        if file_path:
            self.original_image = Image.open(file_path).convert("RGB")
            self.current_image = self.original_image.copy()

            self.show_image()

            self.status_label.config(
                text=f"Image loaded: {self.original_image.size}"
            )

    # --------------------------------------------------
    # Display Image
    # --------------------------------------------------

    def show_image(self):

        if self.current_image is None:
            return

        image = self.current_image.copy()

        # Resize only for display
        max_width = 800
        max_height = 500

        image.thumbnail((max_width, max_height))

        self.display_image = ImageTk.PhotoImage(image)

        self.image_label.config(
            image=self.display_image,
            text=""
        )

    # --------------------------------------------------
    # Check Image
    # --------------------------------------------------

    def check_image(self):

        if self.current_image is None:
            messagebox.showwarning(
                "No Image",
                "Please upload an image first."
            )
            return False

        return True

    # --------------------------------------------------
    # ROTATE
    # --------------------------------------------------

    def rotate(self):

        if not self.check_image():
            return

        angle = simpledialog.askfloat(
            "Rotate",
            "Enter rotation angle in degrees:\n"
            "(Positive = Counterclockwise)"
        )

        if angle is not None:

            self.current_image = self.current_image.rotate(
                angle,
                expand=True
            )

            self.show_image()

            self.status_label.config(
                text=f"Rotated by {angle} degrees"
            )

    # --------------------------------------------------
    # RESIZE
    # --------------------------------------------------

    def resize(self):

        if not self.check_image():
            return

        factor = simpledialog.askfloat(
            "Resize",
            "Enter resize factor:\n"
            "Example: 2 = double size\n"
            "0.5 = half size"
        )

        if factor is None:
            return

        if factor <= 0:
            messagebox.showerror(
                "Invalid Factor",
                "Resize factor must be greater than 0."
            )
            return

        width, height = self.current_image.size

        new_width = int(width * factor)
        new_height = int(height * factor)

        self.current_image = self.current_image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        self.show_image()

        self.status_label.config(
            text=f"Resized by factor {factor}"
        )

    # --------------------------------------------------
    # FLIP
    # --------------------------------------------------

    def flip(self):

        if not self.check_image():
            return

        choice = simpledialog.askstring(
            "Flip",
            "Enter flip direction:\n"
            "H = Horizontal\n"
            "V = Vertical"
        )

        if choice is None:
            return

        choice = choice.upper()

        if choice == "H":

            self.current_image = self.current_image.transpose(
                Image.Transpose.FLIP_LEFT_RIGHT
            )

            self.status_label.config(
                text="Image flipped horizontally"
            )

        elif choice == "V":

            self.current_image = self.current_image.transpose(
                Image.Transpose.FLIP_TOP_BOTTOM
            )

            self.status_label.config(
                text="Image flipped vertically"
            )

        else:

            messagebox.showerror(
                "Invalid Input",
                "Please enter H or V."
            )
            return

        self.show_image()

    # --------------------------------------------------
    # SHEAR
    # --------------------------------------------------

    def shear(self):

        if not self.check_image():
            return

        direction = simpledialog.askstring(
            "Shear",
            "Enter shear direction:\n"
            "X = Horizontal shear\n"
            "Y = Vertical shear"
        )

        if direction is None:
            return

        direction = direction.upper()

        shear_factor = simpledialog.askfloat(
            "Shear Factor",
            "Enter shear factor:\n"
            "Example: 0.5 or -0.5"
        )

        if shear_factor is None:
            return

        width, height = self.current_image.size

        if direction == "X":

            # x' = x + k*y
            matrix = (
                1,
                shear_factor,
                0,
                1,
                0,
                0
            )

            new_width = int(width + abs(shear_factor) * height)

            self.current_image = self.current_image.transform(
                (new_width, height),
                Image.Transform.AFFINE,
                matrix,
                resample=Image.Resampling.BICUBIC
            )

            self.status_label.config(
                text=f"Horizontal shear: k = {shear_factor}"
            )

        elif direction == "Y":

            # y' = y + k*x
            matrix = (
                1,
                0,
                0,
                shear_factor,
                1,
                0
            )

            new_height = int(height + abs(shear_factor) * width)

            self.current_image = self.current_image.transform(
                (width, new_height),
                Image.Transform.AFFINE,
                matrix,
                resample=Image.Resampling.BICUBIC
            )

            self.status_label.config(
                text=f"Vertical shear: k = {shear_factor}"
            )

        else:

            messagebox.showerror(
                "Invalid Direction",
                "Please enter X or Y."
            )
            return

        self.show_image()

    # --------------------------------------------------
    # CUSTOM MATRIX
    # --------------------------------------------------

    def custom_matrix(self):

        if not self.check_image():
            return

        messagebox.showinfo(
            "Custom Matrix",
            "Enter a 2 × 2 transformation matrix:\n\n"
            "[ a  b ]\n"
            "[ c  d ]"
        )

        a = simpledialog.askfloat("Matrix", "Enter a:")
        if a is None:
            return

        b = simpledialog.askfloat("Matrix", "Enter b:")
        if b is None:
            return

        c = simpledialog.askfloat("Matrix", "Enter c:")
        if c is None:
            return

        d = simpledialog.askfloat("Matrix", "Enter d:")
        if d is None:
            return

        matrix = np.array([
            [a, b],
            [c, d]
        ])

        # PIL requires inverse transformation
        try:
            inverse_matrix = np.linalg.inv(matrix)
        except np.linalg.LinAlgError:

            messagebox.showerror(
                "Invalid Matrix",
                "This matrix is singular and cannot be used."
            )
            return

        # PIL affine transformation parameters
        pil_matrix = (
            inverse_matrix[0, 0],
            inverse_matrix[0, 1],
            0,
            inverse_matrix[1, 0],
            inverse_matrix[1, 1],
            0
        )

        width, height = self.current_image.size

        self.current_image = self.current_image.transform(
            (width, height),
            Image.Transform.AFFINE,
            pil_matrix,
            resample=Image.Resampling.BICUBIC
        )

        self.show_image()

        self.status_label.config(
            text=f"Custom matrix applied: [[{a}, {b}], [{c}, {d}]]"
        )

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        if self.original_image is None:
            messagebox.showwarning(
                "No Image",
                "Please upload an image first."
            )
            return

        self.current_image = self.original_image.copy()

        self.show_image()

        self.status_label.config(
            text="Image reset to original"
        )


# ------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = ImageTransformationToolbox(root)

    root.mainloop()