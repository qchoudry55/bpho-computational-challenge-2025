import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Arc
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

#opposite to concave mirror with curved part facing original image
#object starts outside of mirror, image seen inside mirror
#as object moves away from mirror (x or y increases), new image gets smaller and closer to centre of curvature

#calculate coordinates of new image and radius of convex mirror
def calculate_virtual_image(x, y, R):
    try:
        #calculate angle alpha
        alpha = 0.5 * np.arctan2(y, x)

        #calculate k
        k = x / np.cos(2 * alpha)

        #calculate Y coordinate
        denominator = (k / R) - np.cos(alpha) + (x / y) * np.sin(alpha)
        Y = (k * np.sin(alpha)) / denominator

        #calculate X coordinate
        X = x * (Y / y)

        return X, Y

    except:
        return float('inf'), float('inf')

#place image at respective coordinates
def place_image(ax, x, y, image_path, zoom=0.1, flip_horizontal = False):
    img = mpimg.imread(image_path)
    if flip_horizontal:
        #flip image horizontally for only the new image
        img = np.fliplr(img)
    im = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(im, (x, y), frameon=False)
    ax.add_artist(ab)
    return ab

#calculate magnification factor of new image which decreases with distance
def calculate_magnification(x, y, R):
    #base distance from mirror vertex
    distance = np.sqrt(x ** 2 + y ** 2)

    #focal length (negative for convex mirror)
    f = -R / 2

    #calculate image distance using mirror equation
    di = 1 / (1 / f - 1 / distance)

    #magnification formula for convex mirror (always positive and < 1)
    m = abs(di / distance)

    #ensure image gets smaller as object moves farther
    scaling_factor = 1 / (1 + distance / R)  # Decreases with distance

    return m * scaling_factor


#function to update plot when sliders are used
def update(val):
    #get current slider values
    R = radius_slider.val
    x = x_pos_slider.val
    y = y_pos_slider.val

    #clear previous plot
    ax.clear()

    #draw convex mirror
    mirror = Arc((0, 0), 2 * R, 2 * R, theta1=0, theta2=180,
                 color='blue', linewidth=2, fill=False)
    ax.add_patch(mirror)

    #draw principal axis
    ax.axhline(0, color='black', linestyle='--')

    #place object image
    object_img_path = "../challenge_pic4.jpg"  # Change this to your image path
    place_image(ax, x, y, object_img_path, zoom=0.15, flip_horizontal=False)

    #calculate virtual image coordinates
    X, Y = calculate_virtual_image(x, y, R)
    if not np.isinf(X) and not np.isinf(Y):
        #calculate magnification
        m = np.sqrt(X ** 2 + Y ** 2) / np.sqrt(x ** 2 + y ** 2)

        #place virtual image (smaller than object)
        virtual_img_path = "../challenge_pic4.jpg"
        place_image(ax, X, Y, virtual_img_path, zoom=0.15 * abs(m), flip_horizontal= True)

        #draw light rays
        #ray 1 = parallel to principal axis reflects as if from focal point
        f = R / 2  #focal length
        ax.plot([x, 0], [y, 1], 'r-')  #incident ray
        ax.plot([0, X], [1, Y], 'r--')  #virtual ray

        #ray 2 = towards center of curvature reflects back along itself
        ax.plot([x, 0], [y, 0], 'g-')  #incident ray
        ax.plot([0, X], [0, Y], 'g--')  #virtual ray

        #ray 3 = general ray using the given equations
        theta = np.arctan2(y, x)
        x_mirror = R * np.cos(theta)
        y_mirror = R * np.sin(theta)

        ax.plot([x, x_mirror], [y, y_mirror], 'b-')  #incident ray
        ax.plot([x_mirror, X], [y_mirror, Y], 'b--')  #virtual ray

        #draw normal at reflection point
        ax.plot([x_mirror, x_mirror - R * np.cos(theta)],
                [y_mirror, y_mirror - R * np.sin(theta)],
                'k:', linewidth=1)

        #add distance indicator
        ax.text(0.5 * (x + X), 0.5 * (y + Y), f"Mag: {m:.2f}x",
                bbox=dict(facecolor='white', alpha=0.7))

    #set plot limits and labels
    ax.set_xlim(-2 * R, 2 * R)
    ax.set_ylim(-0.5 * R, 1.5 * R)
    ax.set_aspect('equal')
    ax.set_title('Convex Mirror: Virtual Image Formation with Images')
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')
    ax.grid(True)

    plt.draw()


#create figure and axes
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

#initial parameters for sliders
R_initial = 2.0
x_initial = 2.5
y_initial = 1.5

#create sliders
ax_radius = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_x_pos = plt.axes([0.2, 0.10, 0.6, 0.03])
ax_y_pos = plt.axes([0.2, 0.05, 0.6, 0.03])

radius_slider = Slider(ax_radius, 'Mirror Radius (R)', 0.5, 5.0, valinit=R_initial)
x_pos_slider = Slider(ax_x_pos, 'Object X Position', 0, 5.0, valinit=x_initial)
y_pos_slider = Slider(ax_y_pos, 'Object Y Position', 0.1, 2.0, valinit=y_initial)

#use update function for sliders
radius_slider.on_changed(update)
x_pos_slider.on_changed(update)
y_pos_slider.on_changed(update)

#create initial plot
update(None)

plt.show()