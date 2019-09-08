from keras.models import load_model
import os
import sys
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
import tensorflow as tf


# weights = True: full image ;False: cropped image
def predict_imgs(weights, num):
    img_width = 299
    img_height = 299
    batch_size = 32
    nbr_test_samples = num

    root_path = '/home/yuanye/backend/'
    if weights:
        test_data_dir = '/home/yuanye/backend/cropped_imgs/full'
    else:
        test_data_dir = '/home/yuanye/backend/cropped_imgs/cls'

    test_data_gen = ImageDataGenerator(rescale=1. / 255)

    test_generator = test_data_gen.flow_from_directory(
        test_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        shuffle=False,  # Important !!!
        classes=None,
        class_mode=None)

    test_image_list = test_generator.filenames

    K.clear_session()

    if weights:
        inception_v3_model = load_model('/home/yuanye/fish_data/weights_wy.h5')
    else:
        inception_v3_model = load_model('/home/yuanye/fish_data/weights_crop.h5')

    predictions = inception_v3_model.predict_generator(test_generator, nbr_test_samples)
    f_submit = open(os.path.join(root_path, 'results.csv'), 'a')

    for i, image_name in enumerate(test_image_list):
        pred = ['%.6f' % p for p in predictions[i, :]]
        f_submit.write('%s,%s\n' % (os.path.basename(image_name), ','.join(pred)))

    f_submit.close()

    K.clear_session()
    tf.reset_default_graph()

    return pred
