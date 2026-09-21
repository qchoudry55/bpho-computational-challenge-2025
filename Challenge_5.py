import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#virtual reflection of image in plane mirror
#image_path = path to input image file
#mirror_position = x-coordinate where mirror is placed w/ default at x=0

#reflection requirements:
        #image is equidistant from mirror on both sides
        #create new array to hold both the original image and its new reflection
        #mirror is at the x=mirror_position where mirror_position is int()

def create_mirror_reflection(img_path, mirror_position=0):
    #load object in RGB format
    original_image = Image.open(img_path).convert('RGB')
    #convert image to numpy
    img_array = np.array(original_image)

    #find image dimensions
    height, width, channels = img_array.shape

    #obtain canvas dimensions
    left_extent = min(0, 2 * mirror_position - width)
    right_extent = max(width, 2 * mirror_position)
    canvas_width = right_extent - left_extent

    #create white background canvas w/ correct number of channels and big enough to hold both images
    canvas = np.zeros((height, canvas_width, channels), dtype=np.uint8)

    #input original image into canvas
    original_position = -left_extent
    canvas[:, original_position:original_position + width] = img_array

    #create new reflected image
    #flipped horizontally since mirror is some value of x
    reflected_img = np.fliplr(img_array)
    reflection_position = 2 * mirror_position - width - left_extent
    canvas[:, reflection_position:reflection_position + width] = reflected_img

    #display both images w/ canvas on plot
    plt.figure(figsize=(10, 5))

    #plot original image w/ axes
    plt.subplot(1, 2, 1)
    plt.imshow(original_image)
    plt.title('Original Object')
    plt.xlabel('X coordinate (pixels)')
    plt.ylabel('Y coordinate (pixels)')
    plt.grid(True)
    plt.axis('on')

    #plot combined image w/ reflection and axes
    plt.subplot(1, 2, 2)
    plt.imshow(canvas)
    plt.title('Object with Virtual Reflection')
    plt.axvline(x=mirror_position - left_extent, color='r', linestyle='--', label='Mirror')
    plt.legend()
    plt.xlabel('X coordinate (pixels)')
    plt.ylabel('Y coordinate (pixels)')
    plt.grid(True)
    plt.axis('on')

    #show plot in matplotlib
    plt.tight_layout()
    plt.show()

create_mirror_reflection("../challenge_pic4.jpg", mirror_position=5)
