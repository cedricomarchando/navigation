# %%
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav

# %%
#function using np.dot()
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])


img = plt.imread("../map/lorient_base.jpg")
plt.imshow(img)
plt.show()


img_gray = rgb2gray(img)

# put image upside down
img_gray_inv = img_gray.copy()
for i in range(len(img_gray)):
    img_gray_inv[i]= img_gray[len(img_gray)-i -1]

plt.imshow(img_gray_inv, cmap=plt.get_cmap('gray'))
plt.ylim(0,len(img_gray))

amer1 = nav.Amer(200,200)
boat = nav.Boat(300,310)
amer1.plot_position()
boat.plot_position()

plt.axis('off')
plt.show()

# %%
