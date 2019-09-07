from keras.models import load_model
import os
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

img_width = 299
img_height = 299
BATCH_SIZE = 32
nbr_test_samples = 5261

FishNames = ['ALB', 'BET', 'DOL', 'LAG', 'NoF', 'OTHER', 'SHARK', 'YFT']

root_path = '/home/yuanye/fish_data/'
weights_path = '/home/yuanye/fish_data/weights_crop.h5'
test_data_dir = '/home/yuanye/fish_data/test2'

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

print(test_image_list)

print('Loading model and weights from training process ...')
InceptionV3_model = load_model(weights_path)

print('Begin to predict for testing data ...')
predictions = InceptionV3_model.predict_generator(test_generator, nbr_test_samples)

print('Predict successfully')
np.savetxt(os.path.join(root_path, 'predictions1_cls.txt'), predictions)

print('Begin to write submission file ..')
f_submit = open(os.path.join(root_path, 'submit2_cls.csv'), 'w')
print('Open successfully')
f_submit.write('image,ALB,BET,DOL,LAG,NoF,OTHER,SHARK,YFT\n')
print('Write successfully')
for i, image_name in enumerate(test_image_list):
    pred = ['%.6f' % p for p in predictions[i, :]]
    if i % 100 == 0:
        print('{} / {}'.format(i, nbr_test_samples))
    f_submit.write('%s,%s\n' % (os.path.basename(image_name), ','.join(pred)))

f_submit.close()

print('Submission file successfully generated!')
