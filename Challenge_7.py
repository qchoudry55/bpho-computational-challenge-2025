import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#interactive model of virtual, enlarged image inside focal range of lens
#coordinate transformations for thin lens:
    #X = -fx/(x-f)
    #Y = y/x * X
    #only valid when 0<x<f
#thin lens equation:
    #1/u + 1/v = 1/f
#original object has Cartesian coordinates (x,y)
#new image has Cartesian coordinates (X,Y)
#lens is now fixed to the left of the original object and new image

#magnifying lens function
def calculate_image_properties(u, f):
    #image distance on same side of lens
    v = f * u / (f - u)
    #magnification
    m = v / u
    return v, m

def create_scene(object_img_path, f=5, u=3):
    try:
        #load original object in RGB format
        obj_img = Image.open(object_img_path).convert('RGB')
        #convert object to numpy
        obj_array = np.array(obj_img)
        # find object dimensions
        obj_height, obj_width = obj_array.shape[:2]
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found at: {object_img_path}")

    #calculate image properties
    v, m = calculate_image_properties(u, f)
    img_w = int(obj_width * abs(m))
    img_h = int(obj_height * abs(m))

    #resize image but not flipped like last challenge
    img_array = np.array(Image.fromarray(obj_array).resize((img_w, img_h)))

    #calculate lens properties and fixed position
    lens_thickness = 10
    lens_pos = 150

    #object position to right of lens
    obj_x = lens_pos + lens_thickness + 50

    #new image position
    separation = 150  # Space between object and virtual image
    img_x = obj_x + obj_width + separation

    #calculate required canvas dimensions
    buffer = 100
    canvas_w = int(img_x + img_w + buffer)
    canvas_h = max(obj_height, img_h) + 2 * buffer

    #create canvas
    canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255
    center_y = canvas_h // 2

    #place object onto canvas
    obj_y = center_y - obj_height // 2
    canvas[obj_y:obj_y + obj_height, obj_x:obj_x + obj_width] = obj_array

    #place new image onto canvas
    img_y = center_y - img_h // 2
    if img_x + img_w <= canvas_w:
        canvas[img_y:img_y + img_h, img_x:img_x + img_w] = img_array

    #draw optical axis
    canvas[center_y - 1:center_y + 1, :] = [0, 0, 0]

    #draw lens
    lens_left = lens_pos - lens_thickness // 2
    lens_right = lens_pos + lens_thickness // 2
    canvas[:, lens_left:lens_right] = [200, 230, 255]  # Light blue

    #mark focal points (where waves meet after refraction in lens to give the final coordinates of new image)
    f_pixels = int(f)
    for fp in [lens_pos - f_pixels, lens_pos + f_pixels]:
        if 0 <= fp < canvas_w:
            canvas[center_y - 5:center_y + 5, fp - 1:fp + 1] = [255, 0, 0]

    return canvas


#make plot interactive
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

#initial positions for sliders (adjustable on plot)
init_f = 5
init_u = 2

#set image path variable to chosen picture
image_path = "../challenge_pic4.jpg"

#create initial plot for object and image via functions
try:
    canvas = create_scene(image_path, f=init_f, u=init_u)
    img_display = ax.imshow(canvas)
    ax.set_title(f"Virtual Image: f = {init_f}, u = {init_u}")
    ax.axis('off')
except FileNotFoundError as e:
    print(e)
    plt.close()
    exit()

#add matplotlib sliders
ax_f = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_u = plt.axes([0.2, 0.1, 0.6, 0.03])

#name sliders and input slider boundaries/extremes to make it fully interactive with user
f_slider = Slider(ax_f, 'Focal Length (f)', 2, 10, valinit=init_f)
u_slider = Slider(ax_u, 'Object Distance (u)', 0.5, init_f - 0.1, valinit=init_u)

#fully execute all functions for sliders and input image to be used within new image function
def update(val):
    f = f_slider.val
    u = min(u_slider.val, f * 0.99)
    u_slider.valmax = f * 0.99

    #put in option if code fails
    try:
        canvas = create_scene(image_path, f=f, u=u)
        img_display.set_data(canvas)
        ax.set_title(f"Virtual Image: f = {f:.1f}, u = {u:.1f}")
        fig.canvas.draw_idle()
    except FileNotFoundError as e:
        print(e)

#define what buttons do for lens positioning
f_slider.on_changed(update)
u_slider.on_changed(update)

#show plot via matplotlib
plt.show()