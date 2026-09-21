import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Arc
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

#for concave mirror:
    #reflects off mirror with angle of incidence = angle of reflection
    #image has certain coordinates depending on angle of incidence/reflection and coordinates of object
#when object is very close to mirror, image is infinitely backwards and enlarged but not flipped
#when object is at focal point (-R/2), image flips and is smaller before enlarging as object moves further away

def calculate_image_coordinates(x_i, y_i, R):
    try:
        #calculate angle θ_i
        theta_i = np.arctan2(y_i, np.sqrt(R ** 2 - x_i ** 2))

        #calculate m_i
        m_i = np.tan(2 * theta_i)

        #avoid division by 0
        if (y_i / x_i + m_i) == 0:
            return float('inf'), float('inf')

        #calculate X_i and Y_i
        numerator_X = m_i * np.sqrt(R ** 2 - y_i ** 2) - y_i
        denominator = (y_i / x_i) + m_i
        X_i = -numerator_X / denominator
        Y_i = -(y_i / x_i) * (m_i * np.sqrt(R ** 2 - y_i ** 2) - y_i) / ((y_i / x_i) + m_i)

        return X_i, Y_i

    #in case of weird results, break code
    except:
        return float('inf'), float('inf')

#function for reflection ray off mirror to new image
def trace_reflection_ray(x_i, y_i, R, X_i, Y_i, ax):
    #draw ray from object to mirror to image where θ_1 = θ_r
    try:
        #parametrize possible points on mirror
        thetas = np.linspace(0, np.pi, 500)
        for theta in thetas:
            x_mirror = R * np.cos(theta)
            y_mirror = R * np.sin(theta)

            #calculate incident vector
            ix, iy = x_i - x_mirror, y_i - y_mirror
            incident_dir = np.array([ix, iy]) / np.hypot(ix, iy)

            #calculate normal vector at mirror point (pointing toward centre of curvature)
            nx, ny = -np.cos(theta), -np.sin(theta)
            normal_dir = np.array([nx, ny]) / np.hypot(nx, ny)

            #calculate reflected vector
            dot_product = np.dot(incident_dir, normal_dir)
            reflected_dir = incident_dir - 2 * dot_product * normal_dir

            #check if reflected ray passes close to image
            #solve for t where ray hits image line
            if abs(reflected_dir[0]) > 1e-6:
                t = (X_i - x_mirror) / reflected_dir[0]
                y_hit = y_mirror + t * reflected_dir[1]
                if abs(y_hit - Y_i) < 1e-2:  # close enough
                    #draw ray
                    ax.plot([x_i, x_mirror], [y_i, y_mirror], 'm-', linewidth=2)
                    ax.plot([x_mirror, X_i], [y_mirror, Y_i], 'm--', linewidth=2)
                    ax.plot([x_mirror, x_mirror + nx * 0.3],
                            [y_mirror, y_mirror + ny * 0.3], 'k:', linewidth=1)
                    return True
        return False

    #in case of failures
    except:
        return False

#function to draw straight line between mirror and object through image
def extend_line_to_mirror(x_1, y_1, x_2, y_2, R):
    #find intersection of line between (x1,y1) and (x2,y2) where R^2 = x^2 + y^2
    d_x = x_2 - x_1
    d_y = y_2 - y_1

    # Solve for intersection with circle x^2 + y^2 = R^2
    a = d_x**2 + d_y**2
    b = 2 * (x_1*d_x + y_1*d_y)
    c = x_1**2 + y_1**2 - R**2

    disc = b**2 - 4*a*c
    if disc < 0:
        #no intersection
        return None

    t_1 = (-b + np.sqrt(disc)) / (2*a)
    t_2 = (-b - np.sqrt(disc)) / (2*a)

    #use t that is between 0 and 1 or beyond
    for t in (t_1, t_2):
        x_hit = x_1 + t*d_x
        y_hit = y_1 + t*d_y
        if y_hit >= 0:  # upper half of mirror
            return x_hit, y_hit
    return None

#function to put images onto plot
def place_image(ax, x, y, image_path, zoom=0.1, flip_vertical=False):
    img = mpimg.imread(image_path)
    if flip_vertical:
        #flip image vertically
        img = np.flipud(img)
    im = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(im, (x, y), frameon=False)
    ax.add_artist(ab)

#function to update plot when sliders are used
def update(val):
    #get current slider values
    R = radius_slider.val
    x_i = x_pos_slider.val
    y_i = y_pos_slider.val

    #clear any previous points
    ax.clear()

    #draw only concave mirror without coding for a full circle
    mirror = Arc((0, 0), 2 * R, 2 * R, theta1=0, theta2=180,
                 color='blue', linewidth=2, fill=False)
    ax.add_patch(mirror)

    #plot center of curvature
    ax.plot(0, 0, 'ro', markersize=10)  # Center of curvature
    ax.plot(R, 0, 'go', markersize=10)  # Vertex of mirror

    #draw original object
    image_path1 = "../challenge_pic4.jpg"
    place_image(ax, x_i, y_i, image_path1, zoom=0.1, flip_vertical=False)

    #calculate coordinates of new image and draw
    X_i, Y_i = calculate_image_coordinates(x_i, y_i, R)

    #accommodate special circumstances of new image depending on y-value of object
    if not np.isinf(X_i) and not np.isinf(Y_i):
        focal_y = -R / 2
        base_zoom = 0.1

        if y_i > focal_y:
            #above focal point means no flip and enlarge as object gets closer to mirror vertex (x=R)
            dist_to_vertex = abs(x_i - R)
            zoom = base_zoom + 0.2 * max(0, 1 - dist_to_vertex / (3 * R))
            flip_vertical = False
        else:
            #at or below focal point means flip vertically and enlarge as y_i decreases
            zoom = base_zoom + 0.2 * max(0, min(1, (focal_y - y_i) / (3 * R)))
            #at exactly y_i == focal_y, zoom=base_zoom and no flip.
            flip_vertical = True if y_i < focal_y else False

        place_image(ax, X_i, Y_i, image_path1, zoom=zoom, flip_vertical=flip_vertical)

    #draw principal axis from mirror
    ax.axhline(0, color='black', linestyle='--')

    #plot focal point
    ax.plot(0, -R/2, 'bo', markersize=5)  # Center of curvature

    #draw light rays
    if not np.isinf(X_i) and not np.isinf(Y_i):
        #parallel ray to principal axis
        ax.plot([x_i, 0], [y_i, y_i], 'r--')
        ax.plot([0, X_i], [y_i, Y_i], 'r--')

        #extended ray to mirror through center of curvature
        hit_point = extend_line_to_mirror(x_i, y_i, X_i, Y_i, R)
        if hit_point is not None:
            h_x, h_y = hit_point
            #object to mirror ray
            ax.plot([x_i, h_x], [y_i, h_y], 'g--')
            #mirror to image ray
            ax.plot([h_x, X_i], [h_y, Y_i], 'g--')

        #new reflected ray
        trace_reflection_ray(x_i, y_i, R, X_i, Y_i, ax)

    #set plot limits and labels
    ax.set_xlim(-3 * R, 3 * R)
    ax.set_ylim(-5, 2*R)
    ax.set_aspect('equal')
    ax.set_title('Interactive Model of Real Image of an Object In a Concave Spherical Mirror')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    ax.grid(True)

    plt.draw()


#create figure and axes
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)

#initial parameters for sliders
R_initial = 2.0
x_i_initial = 0.05
y_i_initial = 0

#create sliders
ax_radius = plt.axes([0.2, 0.2, 0.6, 0.03])
ax_x_pos = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_y_pos = plt.axes([0.2, 0.1, 0.6, 0.03])

radius_slider = Slider(ax_radius, 'Mirror Radius', 0.5, 5, valinit=R_initial)
x_pos_slider = Slider(ax_x_pos, 'Object X Position', -1, 5.0, valinit=x_i_initial)
y_pos_slider = Slider(ax_y_pos, 'Object Y Position', -5, 2.5, valinit=y_i_initial)

#use update function for sliders
radius_slider.on_changed(update)
x_pos_slider.on_changed(update)
y_pos_slider.on_changed(update)

#create initial plot
update(None)

plt.show()