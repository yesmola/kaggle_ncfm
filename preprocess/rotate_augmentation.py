import os
from skimage.data import imread
from skimage.io import imshow, imsave
import matplotlib.pyplot as plt
import cv2

data_dirs = ['/home/yuanye/fish_data/preprocessed_train/BET/',
             '/home/yuanye/fish_data/preprocessed_train/ALB/',
             '/home/yuanye/fish_data/preprocessed_train/YFT/',
             '/home/yuanye/fish_data/preprocessed_train/DOL/',
             '/home/yuanye/fish_data/preprocessed_train/SHARK/',
             '/home/yuanye/fish_data/preprocessed_train/LAG/',
             '/home/yuanye/fish_data/preprocessed_train/OTHER/']

ALB_dir = '/home/yuanye/fish_data/preprocessed_train/ALB/'

ALB_images = os.listdir(ALB_dir)
ALB_images_update = list()


def get_rotate_images(img, angle):
    (h, w) = img.shape[:2]
    center = (h/2, w/2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


for i in range(len(ALB_images)):
    img_name = ALB_images[i]
    print(img_name)
    image = imread(ALB_dir + img_name)
    for j in range(1):
        ALB_images_update.append(get_rotate_images(image, 180*(j+1)))
    print('success')

for i in range(len(ALB_images_update)):
    imsave('/home/yuanye/fish_data/preprocessed_train/ALB/img' + str(i) + 'ALB_1.jpg', ALB_images_update[i])


