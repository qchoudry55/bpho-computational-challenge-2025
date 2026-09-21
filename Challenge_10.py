import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def rotate_90cw(x, y, cx, cy):
    x_shift = x - cx
    y_shift = y - cy
    x_new = y_shift + cx
    y_new = -x_shift + cy
    return x_new, y_new


def anamorphic_mapping(img, Rf=3.0, arc_deg=160, resolution=500):
    half_side = np.sqrt(2) / 2
    cx, cy = 0, -half_side  # rotation center

    img = img.resize((resolution, resolution))
    src = np.array(img) / 255.0

    y, x = np.indices((resolution, resolution))
    x = (x - resolution / 2) / (resolution / 2)
    y = (y - resolution / 2) / (resolution / 2)

    mask = x**2 + y**2 <= 1

    theta = np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2)
    r_mapped = Rf * r

    # Original coordinates
    X_orig = r_mapped * np.cos(theta)
    Y_orig = r_mapped * np.sin(theta)

    # Rotate 90° CW about (0, -√2/2) to place sector below circle
    X_rot, Y_rot = rotate_90cw(X_orig, Y_orig, cx, cy)

    # Rotate 90° CW again to push it fully below the circle
    X_arc, Y_arc = rotate_90cw(X_rot, Y_rot, cx, cy)

    # Arc mask to shape the sector
    dx = X_arc - cx
    dy = Y_arc - cy
    theta_sector = np.arctan2(dy, dx)
    arc_rad = np.deg2rad(arc_deg) / 2
    arc_mask = np.abs(theta_sector) <= arc_rad

    final_mask = mask & arc_mask

    return X_arc[final_mask], Y_arc[final_mask], src[final_mask]

def plot_interactive_anamorphosis(img_path):
    img = Image.open(img_path).convert("RGB")
    res = 500
    half_side = np.sqrt(2) / 2

    img_square = img.resize((res, res))
    img_arr = np.ones((res, res, 3))

    xv, yv = np.meshgrid(np.linspace(-half_side, half_side, res), np.linspace(-half_side, half_side, res))
    mask_circle = xv ** 2 + yv ** 2 <= 1

    img_square_arr = np.array(img_square) / 255.0
    img_arr[mask_circle] = img_square_arr[mask_circle]

    # Initial parameters
    init_Rf = 3.0
    init_arc_deg = 160

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(left=0.1, bottom=0.25)

    # Plot elements initialized empty; updated in update()
    scatter = None
    sector_center = np.array([0, -half_side])

    # Rotation center
    cx, cy = 0, -half_side

    def update(val):
        ax.clear()

        Rf = slider_Rf.val
        arc_deg = slider_arc.val

        # Background circle
        ax.imshow(img_arr, extent=(-half_side, half_side, -half_side, half_side))
        circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=1.5)
        ax.add_patch(circle)

        # Rotation center
        cx, cy = 0, -half_side

        # --- Scatter points for the sector ---
        X_arc, Y_arc, colors = anamorphic_mapping(img, Rf=Rf, arc_deg=arc_deg, resolution=res)
        X_rot, Y_rot = rotate_90cw(X_arc, Y_arc, cx, cy)
        if X_rot.size > 0:
            ax.scatter(X_rot, Y_rot, c=colors, s=1)

        # --- Geometric sector radii (guaranteed equal) ---
        arc_rad = np.deg2rad(arc_deg) / 2

        # Define vectors relative to rotation center
        left_vec = np.array([Rf * np.cos(-arc_rad), Rf * np.sin(-arc_rad)])
        right_vec = np.array([Rf * np.cos(arc_rad), Rf * np.sin(arc_rad)])

        # Rotate vectors 90° CW around origin
        def rotate_vec_90cw(vec):
            x, y = vec
            return np.array([y, -x])

        left_rot = rotate_vec_90cw(left_vec) + np.array([cx, cy])
        right_rot = rotate_vec_90cw(right_vec) + np.array([cx, cy])

        # Draw radii
        ax.plot([cx, left_rot[0]], [cy, left_rot[1]], 'k--', linewidth=1)
        ax.plot([cx, right_rot[0]], [cy, right_rot[1]], 'k--', linewidth=1)

        # Mark rotation center
        ax.plot(cx, cy, 'ro')

        # Axes settings
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-Rf - 5, Rf + 5)
        ax.set_ylim(cy - Rf - 3, 5)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title(f"Anamorphic Sector Rotated 90° CW About (0, -√2/2) - Arc={arc_deg:.1f}°, Rf={Rf:.2f}")

        fig.canvas.draw_idle()

    # Sliders axes
    ax_Rf = plt.axes([0.1, 0.15, 0.8, 0.03])
    ax_arc = plt.axes([0.1, 0.1, 0.8, 0.03])

    slider_Rf = Slider(ax_Rf, 'Rf', 0.1, 10.0, valinit=init_Rf, valstep=0.1)
    slider_arc = Slider(ax_arc, 'Arc Angle', 10, 360, valinit=init_arc_deg, valstep=1)

    slider_Rf.on_changed(update)
    slider_arc.on_changed(update)

    update(None)
    plt.show()

plot_interactive_anamorphosis("../challenge_pic4.jpg")