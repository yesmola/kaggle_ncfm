from keras.applications.inception_v3 import InceptionV3
import os
from keras.layers import Flatten, Dense, AveragePooling2D
from keras.models import Model
from keras.optimizers import RMSprop, SGD
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image

LR = 0.0001
EPOCHS = 25
BATCH_SIZE = 32

img_width = 299
img_height = 299
nbr_train_samples = 9882
nbr_validation_samples = 2473

train_data_dir = '/home/yuanye/fish_data/train_split'
val_data_dir = '/home/yuanye/fish_data/val_split'

CLASSES = ['ALB', 'BET', 'DOL', 'LAG', 'NoF', 'OTHER', 'SHARK', 'YFT']

print('Loading InceptionV3 Weights ...')
InceptionV3_notop = InceptionV3(include_top=False, weights='imagenet',
                                input_tensor=None, input_shape=(299, 299, 3))

print('Adding Average Pooling Layer and Softmax Output Layer ...')
output = InceptionV3_notop.get_layer(index=-1).output  # Shape:(8, 8, 2048)
output = AveragePooling2D((8, 8), strides=(8, 8), name='avg_pool')(output)
output = Flatten(name='flatten')(output)
output = Dense(8, activation='softmax', name='predictions')(output)

InceptionV3_model = Model(InceptionV3_notop.input, output)
# InceptionV3_model.summary()

optimizer = SGD(lr=LR, momentum=0.9, decay=0.0, nesterov=True)
InceptionV3_model.compile(loss='categorical_crossentropy', optimizer=optimizer,
                          metrics=['accuracy'])

# autosave best model
best_model_file = '/home/yuanye/fish_data/weights_crop_aug_25.h5'
best_model = ModelCheckpoint(best_model_file, monitor='val_acc', verbose=1, save_best_only=True)

train_data_gen = ImageDataGenerator(rescale=1. / 255,
                                    shear_range=0.1,
                                    zoom_range=0.1,
                                    rotation_range=10.,
                                    width_shift_range=0.1,
                                    height_shift_range=0.1,
                                    horizontal_flip=True)

# this is the augmentation configuration we will use for validation:
# only rescaling
val_data_gen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_data_gen.flow_from_directory(train_data_dir,
                                                     target_size=(img_width, img_height),
                                                     batch_size=BATCH_SIZE,
                                                     shuffle=True,
                                                     classes=CLASSES,
                                                     class_mode='categorical')

validation_generator = val_data_gen.flow_from_directory(val_data_dir,
                                                        target_size=(img_width, img_height),
                                                        batch_size=BATCH_SIZE,
                                                        shuffle=True,
                                                        classes=CLASSES,
                                                        class_mode='categorical')

InceptionV3_model.fit_generator(train_generator,
                                samples_per_epoch=nbr_train_samples,
                                nb_epoch=EPOCHS,
                                validation_data=validation_generator,
                                nb_val_samples=nbr_validation_samples,
                                callbacks=[best_model])
