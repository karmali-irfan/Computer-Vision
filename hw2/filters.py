import numpy as np


def conv_nested(image, kernel):
    """A naive implementation of convolution filter.

    This is a naive implementation of convolution using 4 nested for-loops.
    This function computes convolution of an image with a kernel and outputs
    the result that has the same shape as the input image.

    Args:
        image: numpy array of shape (Hi, Wi).
        kernel: numpy array of shape (Hk, Wk).

    Returns:
        out: numpy array of shape (Hi, Wi).
    """
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))

    ### YOUR CODE HERE
    h, w = Hk // 2, Wk // 2
    #height of the image
    for i in range(Hi):
        #width of the image
        for j in range(Wi):
            sum = 0
            #height of the kernel
            for k in range(Hk):
                #width of the kernel 
                for l in range(Wk):
                    #accounting for the corners
                    if 0 <= i + h - k < Hi and 0 <= j + w - l < Wi:
                        sum = sum + kernel[k, l] * image[i + h - k, j + w - l]
            out[i, j] = sum 
    ### END YOUR CODE
    
   

    return out

def zero_pad(image, pad_height, pad_width):
    """ Zero-pad an image.

    Ex: a 1x1 image [[1]] with pad_height = 1, pad_width = 2 becomes:

        [[0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0]]         of shape (3, 5)

    Args:
        image: numpy array of shape (H, W).
        pad_width: width of the zero padding (left and right padding).
        pad_height: height of the zero padding (bottom and top padding).

    Returns:
        out: numpy array of shape (H+2*pad_height, W+2*pad_width).
    """

    H, W = image.shape
    out = None 

    ### YOUR CODE HERE
    h = H + 2*pad_height 
    w = W + 2*pad_width 
    #creating an array of zeros 
    array = np.array(  [[float(0)]*w]*h  )
    #padding the image
    array[pad_height:h-pad_height, pad_width:w-pad_width] = image[:,:]
    out = array    
    ### END YOUR CODE
    
    #array = np.zeros((H + 2 * pad_height, W + 2 * pad_width))
    #np.zeros creates an array of the size with floats. Using ints
    #would result in not all pixels being shown, hence line 61 uses 
    #float(0)
    return out


def conv_fast(image, kernel):
    """ An efficient implementation of convolution filter.

    This function uses element-wise multiplication and np.sum()
    to efficiently compute weighted sum of neighborhood at each
    pixel.

    Hints:
        - Use the zero_pad function you implemented above
        - There should be two nested for-loops
        - You may find np.flip() and np.sum() useful

    Args:
        image: numpy array of shape (Hi, Wi).
        kernel: numpy array of shape (Hk, Wk).

    Returns:
        out: numpy array of shape (Hi, Wi).
    """
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))

    ### YOUR CODE HERE
    padded_image = zero_pad(image, Hk//2, Wk//2)
    #flipping the kernel 
    kernel = np.flip(kernel, 0)
    kernel = np.flip(kernel, 1)
    for i in range (Hi): 
        for j in range (Wi): 
            #sum of the multiplications
            out[i][j] = np.sum(padded_image[i:i+Hk, j:j+Wk] * kernel)
    ### END YOUR CODE
    return out

def cross_correlation(f, g):
    """ Cross-correlation of f and g.

    Hint: use the conv_fast function defined above.

    Args:
        f: numpy array of shape (Hf, Wf).
        g: numpy array of shape (Hg, Wg).

    Returns:
        out: numpy array of shape (Hf, Wf).
    """

    out = None
    ### YOUR CODE HERE
    g = np.flip(g, (0,1))
    out = conv_fast(f, g) 
    ### END YOUR CODE

    return out

def zero_mean_cross_correlation(f, g):
    """ Zero-mean cross-correlation of f and g.

    Subtract the mean of g from g so that its mean becomes zero.

    Hint: you should look up useful numpy functions online for calculating the mean.

    Args:
        f: numpy array of shape (Hf, Wf).
        g: numpy array of shape (Hg, Wg).

    Returns:
        out: numpy array of shape (Hf, Wf).
    """

    out = None
    ### YOUR CODE HERE
    #substracting the mean from g 
    g = g - np.mean(g) 
    out = cross_correlation(f, g)
    ### END YOUR CODE

    return out

def normalized_cross_correlation(f, g):
    """ Normalized cross-correlation of f and g.

    Normalize the subimage of f and the template g at each step
    before computing the weighted sum of the two.

    Hint: you should look up useful numpy functions online for calculating 
          the mean and standard deviation.

    Args:
        f: numpy array of shape (Hf, Wf).
        g: numpy array of shape (Hg, Wg).

    Returns:
        out: numpy array of shape (Hf, Wf)
    """
    
    
    ### YOUR CODE HERE
    Hi, Wi = f.shape
    Hk, Wk = g.shape
    out = np.zeros((Hi, Wi))

    f_padded = zero_pad(f, Hk // 2, Wk // 2)
    normalised_g = (g - np.mean(g)) / np.std(g)
    
    for m in range(Hi):
        for n in range(Wi):
            img_patch = f_padded[m: m + Hk, n: n + Wk]
            normalised_patch = (img_patch -  np.mean(img_patch)) / np.std(img_patch) 
            out[m, n] = np.sum(np.multiply(normalised_patch, normalised_g))
    return out
    
    ### END YOUR CODE

    return out
