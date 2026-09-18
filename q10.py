import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ---------------------------------------------------
# 1. READ IMAGE
# ---------------------------------------------------

img = Image.open("Nature.jpeg").convert("RGB")
img = np.array(img)

print("Original image shape:", img.shape)


# ---------------------------------------------------
# 2. DEFINE BASIS VECTORS
# ---------------------------------------------------

e1 = np.array([1, 0])
e2 = np.array([0, 1])


# ---------------------------------------------------
# 3. DEFINE MATRICES
# ---------------------------------------------------

A1 = np.array([
    [2, 0],
    [0, 0.5]
])

A2 = np.array([
    [0, -1],
    [1,  0]
])

A3 = np.array([
    [1, 1],
    [0, 1]
])

A4 = np.array([
    [-1, 0],
    [0,  1]
])

A5 = np.array([
    [1, 0],
    [0, 0]
])


matrices = {
    "A1 - Scaling": A1,
    "A2 - 90 degree Rotation": A2,
    "A3 - Horizontal Shear": A3,
    "A4 - Reflection in y-axis": A4,
    "A5 - Projection onto x-axis": A5
}


# ---------------------------------------------------
# 4. PRINT ASSIGNMENT INFORMATION
# ---------------------------------------------------

print("\n\n===== TRANSFORMATION INFORMATION =====")

for name, A in matrices.items():

    Te1 = A @ e1
    Te2 = A @ e2
    rank = np.linalg.matrix_rank(A)

    print("\n", name)
    print("Matrix:")
    print(A)

    print("T(e1) =", Te1)
    print("T(e2) =", Te2)

    print("Rank =", rank)

    if rank < 2:
        print("Information loss: YES")
    else:
        print("Information loss: NO")


# ---------------------------------------------------
# 5. FUNCTION TO TRANSFORM IMAGE
# ---------------------------------------------------

def transform_image(image, A):

    height, width, channels = image.shape

    # Image centre
    cx = (width - 1) / 2
    cy = (height - 1) / 2

    # Create coordinates for every pixel
    y, x = np.indices((height, width))

    # Move origin to image centre
    X = x - cx
    Y = cy - y

    # Convert coordinates into vectors
    coordinates = np.vstack((
        X.flatten(),
        Y.flatten()
    ))

    # Apply transformation
    transformed_coordinates = A @ coordinates

    X_new = transformed_coordinates[0]
    Y_new = transformed_coordinates[1]

    # Find new boundaries
    min_x = np.floor(X_new.min())
    max_x = np.ceil(X_new.max())

    min_y = np.floor(Y_new.min())
    max_y = np.ceil(Y_new.max())

    new_width = int(max_x - min_x + 1)
    new_height = int(max_y - min_y + 1)

    # Create white output image
    new_image = np.ones(
        (new_height, new_width, channels),
        dtype=np.uint8
    ) * 255

    # Convert mathematical coordinates back to image coordinates
    new_x = np.round(X_new - min_x).astype(int)
    new_y = np.round(max_y - Y_new).astype(int)

    # Check valid pixels
    valid = (
        (new_x >= 0) &
        (new_x < new_width) &
        (new_y >= 0) &
        (new_y < new_height)
    )

    # Copy pixels
    original_pixels = image.reshape(-1, channels)

    new_image[
        new_y[valid],
        new_x[valid]
    ] = original_pixels[valid]

    return new_image


# ---------------------------------------------------
# 6. DISPLAY ORIGINAL IMAGE
# ---------------------------------------------------

plt.figure(figsize=(6, 5))
plt.imshow(img)
plt.title("Original Image")
plt.axis("off")
plt.show()


# ---------------------------------------------------
# 7. APPLY ALL TRANSFORMATIONS
# ---------------------------------------------------

for name, A in matrices.items():

    # A5 is mathematically a projection onto x-axis.
    # For visualization only, use a tiny y-scale.
    if name.startswith("A5"):

        A_visual = np.array([
            [1, 0],
            [0, 0.02]
        ])

        result = transform_image(img, A_visual)

        title = (
            "A5 - Projection onto x-axis\n"
            "0.02 used only for visualization"
        )

    else:

        result = transform_image(img, A)
        title = name

    # Display result
    plt.figure(figsize=(7, 5))
    plt.imshow(result)
    plt.title(title)
    plt.axis("off")
    plt.show()