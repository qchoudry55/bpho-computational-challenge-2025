import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#interactive model of real, inverted image of object outside focal range of ideal lens
#coordinate transformations for thin lens:
    #X = -fx/(x-f)
    #Y = y/x * X
    #only valid when x>f
#thin lens equation:
    #1/u + 1/v = 1/f
#original object has Cartesian coordinates (x,y)
#new image has Cartesian coordinates (X,Y)
#lens is either to left or right of object to see new image clearly and show what actually happens with a thin lens

#thin lens function for coordinate transformations
def lens_transform(x, y, f):
    #new image coordinate X
    X = -f * x / (x - f)
    #new image coordinate Y
    Y = (y / x) * X
    return X, Y

#function to create new image with new coordinates from thin lens function
def create_lens_img(object_img_path, f=5, object_x=10, object_y=0, lens_side='right'):
    #load original object in RGB format
    object_img = Image.open(object_img_path).convert('RGB')
    #convert object to numpy
    obj_array = np.array(object_img)
    #find object dimensions
    obj_height, obj_width = obj_array.shape[:2]

    #calculate new image coordinates
    X, Y = lens_transform(object_x, object_y, f)

    #initial canvas dimensions
    buffer = 100
    separation = 200
    object_translation = 150

    #calculate required canvas dimensions with either lens on right or left (here, left is "else")
    if lens_side == 'right':
        visual_object_x = object_x + object_translation
        total_width = int(visual_object_x + abs(X) + 2 * obj_width + buffer + separation)
        lens_position = int(visual_object_x + obj_width + buffer // 2)
        image_position = lens_position + int(abs(X)) + separation

    else:
        visual_object_x = object_x
        total_width = int(visual_object_x + abs(X) + 2 * obj_width + buffer + separation)
        lens_position = int(total_width - visual_object_x - obj_width - buffer // 2)
        image_position = lens_position - int(abs(X)) - separation

    total_height = int(2 * max(obj_height, abs(Y)) + buffer)
    canvas = np.zeros((total_height, total_width, 3), dtype=np.uint8) + 255

    #place object onto canvas, depending on whether the lens is on the right or left
    center_y = total_height // 2
    if lens_side == 'right':
        obj_x_start = buffer // 2
    else:
        obj_x_start = lens_position + buffer // 2

    #ensure object does not exceed canvas dimensions for program to run
    obj_y_start = center_y - obj_height // 2
    canvas[obj_y_start:obj_y_start + obj_height, obj_x_start:obj_x_start + obj_width] = obj_array

    #place new image w/ inversions and scaled
    #magnification of thin lens
    mag = abs(X / object_x)  # Note: using original object_x for correct magnification
    img_width = int(obj_width * mag)
    img_height = int(obj_height * mag)

    #flip image
    img_array = np.flipud(obj_array)
    img_array = np.array(Image.fromarray(img_array).resize((img_width, img_height)))

    #place image
    img_x_start = image_position - img_width // 2
    img_y_start = center_y - img_height // 2

    #draw optical axis
    canvas[center_y - 1:center_y + 1, :] = [0, 0, 0]
    canvas[img_y_start:img_y_start + img_height, img_x_start:img_x_start + img_width] = img_array

    #draw lens
    lens_thickness = 10
    lens_left = max(0, lens_position - lens_thickness // 2)
    lens_right = min(total_width, lens_position + lens_thickness // 2)
    canvas[:, lens_left:lens_right] = [200, 200, 255]

    #mark focal points (where waves meet after refraction in lens to give the final coordinates of new image)
    f_pixels = int(f)
    for fp in [lens_position - f_pixels, lens_position + f_pixels]:
        fp_left = max(0, fp - 1)
        fp_right = min(total_width, fp + 1)
        canvas[center_y - 5:center_y + 5, fp_left:fp_right] = [255, 0, 0]

    return canvas

#make plot interactive
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.3)

#add slide buttons to choose where lens goes
ax_left = plt.axes([0.2, 0.25, 0.1, 0.04])
ax_right = plt.axes([0.7, 0.25, 0.1, 0.04])
left_button = plt.Button(ax_left, 'Lens Left')
right_button = plt.Button(ax_right, 'Lens Right')

#initial positions for sliders (adjustable on plot)
init_f = 5
init_x = 10
current_side = 'right'

#create initial plot for object and image via functions
canvas = create_lens_img("../challenge_pic4.jpg", f=init_f, object_x=init_x, lens_side=current_side)
img_display = ax.imshow(canvas)
ax.set_title(f"Thin Lens Simulation (f = {init_f}, u = {init_x}, Lens: {current_side}")
ax.axis('off')

#add matplotlib sliders
ax_f = plt.axes([0.2, 0.2, 0.6, 0.03])
ax_x = plt.axes([0.2, 0.15, 0.6, 0.03])

#name sliders and input slider boundaries/extremes to make it fully interactive with user
f_slider = Slider(ax_f, 'Focal Length (f)', 1, 10, valinit=init_f)
x_slider = Slider(ax_x, 'Object Distance (u)', 5.1, 15, valinit=init_x)

#fully execute all functions for sliders and input image to be used within new image function
def update(val=None):
    global current_side
    f = f_slider.val
    x = x_slider.val
    canvas = create_lens_img("../challenge_pic4.jpg", f=f, object_x=x, lens_side=current_side)
    img_display.set_data(canvas)
    ax.set_title(f"Thin Lens Simulation (f = {f:.1f}, u = {x:.1f}, Lens: {current_side}")
    fig.canvas.draw_idle()

#define what happens if one of the lens positioning buttons is clicked
def set_left(event):
    global current_side
    current_side = 'left'
    update()
def set_right(event):
    global current_side
    current_side = 'right'
    update()

#define what buttons do for lens positioning
left_button.on_clicked(set_left)
right_button.on_clicked(set_right)
f_slider.on_changed(update)
x_slider.on_changed(update)

#show plot via matplotlib
plt.show()

#when running code:
    #blue lines represent the thin lens therefore it is located in centre of the plot
    #horizontal bounds of both object and new image are shown as small red lines
    #sliders cannot go above or below (depends on which slider) certain values otherwise image exceeds canvas boundaries or lens