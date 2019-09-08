from keras.models import load_model
import os
import sys
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

import numpy as np

img_width = 299
img_height = 299
BATCH_SIZE = 1
nbr_test_samples = int(sys.argv[2])

FishNames = ['ALB', 'BET', 'DOL', 'LAG', 'NoF', 'OTHER', 'SHARK', 'YFT']

root_path = '/home/yuanye/fish_data/'
test_data_dir = sys.argv[1]
weights_cls_path = '/home/yuanye/fish_data/weights_crop.h5'


# test data generator for prediction
test_data_gen = ImageDataGenerator(rescale=1. / 255)

test_generator = test_data_gen.flow_from_directory(
    test_data_dir,
    target_size=(img_width, img_height),
    batch_size=BATCH_SIZE,
    shuffle=False,  # Important !!!
    classes=None,
    class_mode=None)

test_image_list = test_generator.filenames

InceptionV3_model = load_model(weights_cls_path)
predictions = InceptionV3_model.predict_generator(test_generator, nbr_test_samples)

for i, image_name in enumerate(test_image_list):
    pred = ['%.6f' % p for p in predictions[i, :]]
    print('%s,%s\n' % (os.path.basename(image_name), ','.join(pred)))

