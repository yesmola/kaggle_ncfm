from skimage.data import imread
from skimage.io import imshow, imsave
from skimage import img_as_float
import pandas as pd
import numpy as np
import cv2
from skimage.util import crop
from skimage.transform import rotate
from skimage.transform import resize
import matplotlib.pyplot as plt
import math
from math import atan2, degrees, pi


def deg_angle_between(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    rads = atan2(-dy, dx)
    rads %= 2 * pi
    degs = degrees(rads)
    return degs


def get_rotated_cropped_fish(img, x1, y1, x2, y2):
    (h, w) = img.shape[:2]
    # calculate center and angle
    center = ((x1 + x2) / 2, (y1 + y2) / 2)
    angle = np.floor(-deg_angle_between(x1, y1, x2, y2))
    # print('angle=' +str(angle) + ' ')
    # print('center=' +str(center))
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))

    fish_length = np.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    cropped = rotated[
              (int)(max((center[1] - (fish_length // 1.8)), 0)):(max((int)(center[1] + (fish_length // 1.8)), 0)),
              (max((int)(center[0] - (fish_length // 1.8)), 0)):(max((int)(center[0] + (fish_length // 1.8)), 0))]
    # imshow(img)
    # imshow(rotated)
    # imshow(cropped)
    resized = resize(cropped, (224, 224))
    return resized


label_files = ['/home/yuanye/PycharmProjects/kaggle_ncfm/labels/bet_labels.json',
               '/home/yuanye/PycharmProjects/kaggle_ncfm/labels/alb_labels.json',
               '/home/yuanye/PycharmProjects/kaggle_ncfm/labels/yft_labels.json',
               '/home/yuanye/PycharmProjects/kaggle_ncfm/labels/dol_labels.json',
               '/home/yuanye/PycharmProjects/kaggle_ncfm/labels/shark_labels.json',
               '/home/yuanye/PycharmProjects/kaggle_ncfm/labels/lag_labels.json',
               '/home/yuanye/PycharmProjects/kaggle_ncfm/labels/other_labels.json']

data_dirs = ['/home/yuanye/fish_data/train/BET/',
             '/home/yuanye/fish_data/train/ALB/',
             '/home/yuanye/fish_data/train/YFT/',
             '/home/yuanye/fish_data/train/DOL/',
             '/home/yuanye/fish_data/train/SHARK/',
             '/home/yuanye/fish_data/train/LAG/',
             '/home/yuanye/fish_data/train/OTHER/']


images = list()
labels_list = list()
for c in range(7):
    labels = pd.read_json(label_files[c])
    for i in range(len(labels)):
        img_filename = labels.iloc[i, 2]
        print(img_filename)
        l1 = pd.DataFrame((labels[labels.filename == img_filename].annotations).iloc[0])
        image = imread(data_dirs[c] + img_filename)
        # imshow(image)
        images.append(
            get_rotated_cropped_fish(image, np.floor(l1.iloc[0, 1]), np.floor(l1.iloc[0, 2]), np.floor(l1.iloc[1, 1]),
                                     np.floor(l1.iloc[1, 2])))
        print('success')
        labels_list.append(c)


# pd.DataFrame(labels_list).iloc[:, 0].value_counts()
pd.DataFrame(labels_list).iloc[:, 0].value_counts()

for i in range(len(images)):
    if labels_list[i] == 0:
        imsave('/home/yuanye/fish_data/preprocessed_train/BET/img' + str(i) + 'BET_0.jpg', images[i])
    elif labels_list[i] == 1:
        imsave('/home/yuanye/fish_data/preprocessed_train/ALB/img' + str(i) + 'ALB_0.jpg', images[i])
    elif labels_list[i] == 2:
        imsave('/home/yuanye/fish_data/preprocessed_train/YFT/img' + str(i) + 'YFT_0.jpg', images[i])
    elif labels_list[i] == 3:
        imsave('/home/yuanye/fish_data/preprocessed_train/DOL/img' + str(i) + 'DOL_0.jpg', images[i])
    elif labels_list[i] == 4:
        imsave('/home/yuanye/fish_data/preprocessed_train/SHARK/img' + str(i) + 'SHARK_0.jpg', images[i])
    elif labels_list[i] == 5:
        imsave('/home/yuanye/fish_data/preprocessed_train/LAG/img' + str(i) + 'LAG_0.jpg', images[i])
    elif labels_list[i] == 6:
        imsave('/home/yuanye/fish_data/preprocessed_train/OTHER/img' + str(i) + 'OTHER_0.jpg', images[i])

