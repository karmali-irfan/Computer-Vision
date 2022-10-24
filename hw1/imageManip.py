import math

import numpy as np
from PIL import Image
from skimage import color, io


def load(image_path):
    """Loads an image from a file path.

    HINT: Look up `skimage.io.imread()` function.

    Args:
        image_path: file path to the image.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    out = None

    ### YOUR CODE HERE
    #reading the path of the image
    out = io.imread(image_path)
    ### END YOUR CODE

    # Let's convert the image to be between the correct range.
    out = out.astype(np.float64) / 255
    return out


def dim_image(image):
    """Change the value of every pixel by following

                        x_n = 0.5*x_p^2

    where x_n is the new value and x_p is the original value.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None

    ### YOUR CODE HERE
    dim_image = image.copy() #copying the image
    #formula for dimming the image
    out = 0.5 * dim_image ** 2 
    ### END YOUR CODE

    return out


def convert_to_grey_scale(image):
    """Change image to gray scale.

    HINT: Look at `skimage.color` library to see if there is a function
    there you can use.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width).
    """
    out = None

    ### YOUR CODE HERE
    gray_image = image.copy() #copy of the image
    #function to convert to grayscale
    out = color.rgb2gray(gray_image) 
    ### END YOUR CODE

    return out


def rgb_exclusion(image, channel):
    """Return image **excluding** the rgb channel specified

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "R", "G" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None

    ### YOUR CODE HERE
    new_image = image.copy() #copy of the image
    
    if channel == 'R': #excluding R
        new_image[:,:,0] = 0
    
    if channel == 'G': #excluding G
        new_image[:,:,1] = 0
        
    if channel == 'B': #excluding B
        new_image[:,:,2] = 0
    
    out = new_image
    ### END YOUR CODE

    return out


def lab_decomposition(image, channel):
    """Decomposes the image into LAB and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "L", "A" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    lab = color.rgb2lab(image)
    out = None

    ### YOUR CODE HERE
    
    if channel == 'L':
        out = lab[  :, :, 0]
    if channel == 'A':
        out = lab[  :, :, 1]
    if channel == 'B':
        out = lab[  :, :, 2]

    ### END YOUR CODE

    return out


def hsv_decomposition(image, channel):
    """Decomposes the image into HSV and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "H", "S" or "V".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    hsv = color.rgb2hsv(image)
    out = None

    ### YOUR CODE HERE
    if channel == 'H': #returning only Hue 
        hsv = hsv[:,:,0]
    if channel == 'S': #returning only Saturation
        hsv = hsv[:,:,1]
    if channel == 'V': #Returning only Value
        hsv = hsv[:,:,2]
    
    out = hsv
    ### END YOUR CODE

    return out


def mix_images(image1, image2, channel1, channel2):
    """Combines image1 and image2 by taking the left half of image1
    and the right half of image2. The final combination also excludes
    channel1 from image1 and channel2 from image2 for each image.

    HINTS: Use `rgb_exclusion()` you implemented earlier as a helper
    function. Also look up `np.concatenate()` to help you combine images.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).
        image2: numpy array of shape(image_height, image_width, 3).
        channel1: str specifying channel used for image1.
        channel2: str specifying channel used for image2.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None
    ### YOUR CODE HERE
    #excluding channel1 from image1
    image1_copy = rgb_exclusion(image1, channel1)
    
    #exlcuding channel2 from image2
    image2_copy = rgb_exclusion(image2, channel2)
    
    #dimensions for image1 (righthalf)
    a = image1_copy[0:300 , 0:150]
    
    #dimensions for image2 (lefthalf)
    c = image2_copy[0:300, 150:300]
    
    #concatenating the two halfs 
    image_result = np.concatenate((a , c), axis = 1) 
    
    out = image_result 
    ### END YOUR CODE

    return out


def mix_quadrants(image):
    """THIS IS AN EXTRA CREDIT FUNCTION.

    This function takes an image, and performs a different operation
    to each of the 4 quadrants of the image. Then it combines the 4
    quadrants back together.

    Here are the 4 operations you should perform on the 4 quadrants:
        Top left quadrant: Remove the 'R' channel using `rgb_exclusion()`.
        Top right quadrant: Dim the quadrant using `dim_image()`.
        Bottom left quadrant: Brighthen the quadrant using the function:
            x_n = x_p^0.5
        Bottom right quadrant: Remove the 'R' channel using `rgb_exclusion()`.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    out = None

    ### YOUR CODE HERE
    q1 = image[0:150, 0:150] #upperleft quadrant 
    q2 = image[150:300, 0:150] #lowerleft quadrant 
    q3 = image[0:150 , 150:300] #upperright quadrant
    q4 = image[150:300, 150:300] #lowerright quadrant
    
    q1 = rgb_exclusion(q1, 'R') #excluding R from q1 
    q3 = dim_image(q3) #dimming q3
    q2 = q2 ** 0.5  #brightening q2
    q4 = rgb_exclusion(q4, 'R') # excluding R from q4
    
    #concatenating the quadrants to reform the image
    upperhalf = np.concatenate((q1, q2), axis = 0)
    lowerhalf = np.concatenate((q3, q4), axis = 0)
    image = np.concatenate((upperhalf, lowerhalf), axis = 1)
    out = image
    ### END YOUR CODE

    return  out 
