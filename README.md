# SMAS-Assignment-03 

Q 10.
| Transformation | T(e1)  | T(e2)   | Rank | Information loss |
| A1 Scaling     | (2,0)  | (0,0.5) |   2  |        No        |
| A2 Rotation    | (0,1)  | (-1,0)  |   2  |        No        |
| A3 Shear       | (1,0)  | (1,1)   |   2  |        No        |
| A4 Reflection  | (-1,0) | (0,1)   |   2  |        No        |
| A5 Projection  | (1,0)  | (0,0)   |   1  |        Yes       |

One-sentence explanations

A₁ — Scaling

The columns (2,0) and (0,0.5) show that the x-direction is stretched by 2 while the y-direction is compressed by half.

A₂ — 90° Rotation

The columns (0,1) and (-1,0) show that the basis directions are rotated 90° counterclockwise without changing their lengths.

A₃ — Horizontal Shear

The columns (1,0) and (1,1) show that the x-direction remains unchanged while the y-direction is shifted horizontally.

A₄ — Reflection

The columns (-1,0) and (0,1) show that the x-direction reverses while the y-direction remains unchanged, producing reflection in the y-axis.

A₅ — Projection

The columns (1,0) and (0,0 )show that the x-direction is preserved but the entire y-direction is collapsed to zero, causing information loss.




Q 11.
Aim - 
To develop an interactive Image Transformation Toolbox in Python that allows users to upload an image and apply common geometric transformations such as rotation, resizing, flipping, shearing, and custom matrix transformations.

Technologies used
Python
Tkinter
Pillow (PIL)
NumPy
VS Code

Transformations implemented
   Operation         Parameter             Mathematical idea            
|  Rotate        |   Angle             |  Rotation matrix             |
|  Resize        |  Scale factor       |  Scaling matrix              |
|  Flip          |  H/V                |  Reflection matrix           |
|  Shear         |  Direction + factor |  Shear matrix                |
|  Custom Matrix |  a, b, c, d         |  General 2 x 2 matrix        |
|  Reset         |  None               |  Restore original image      |

Conclusion - 
The developed toolbox provides an interactive way to understand geometric transformations using images. Each transformation can be related to a matrix operation on two-dimensional coordinates. The custom matrix option allows arbitrary 2 x 2 linear transformations to be applied to the uploaded image.


