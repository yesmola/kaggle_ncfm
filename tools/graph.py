import matplotlib.pyplot as plt
import numpy as np

epoch = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                  13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
loss_train = [1.6786, 1.4821, 1.3871, 1.3160, 1.2187, 1.1571, 1.0910, 1.0444, 0.9725, 0.9512, 0.8606, 0.8331,
              0.7850, 0.7314, 0.7024, 0.6395, 0.6214, 0.5798, 0.5585, 0.5148, 0.4893, 0.4774, 0.4258, 0.4333, 0.4023]
acc_train = [0.4126, 0.4875, 0.5261, 0.5528, 0.5766, 0.5932, 0.6158, 0.6275, 0.6591, 0.6678, 0.7015, 0.7253,
             0.7304, 0.7671, 0.7825, 0.8146, 0.8172, 0.8352, 0.8448, 0.8528, 0.8678, 0.8744, 0.8873, 0.8784, 0.8907]
loss_val = [1.5198, 1.4159, 1.3242, 1.2402, 1.1658, 1.0947, 1.0381, 0.9865, 0.9298, 0.8740, 0.8241, 0.7810,
            0.7326, 0.6922, 0.6499, 0.6124, 0.5771, 0.5519, 0.5250, 0.4943, 0.4738, 0.4448, 0.4368, 0.4203, 0.3922]
acc_val = [0.4752, 0.5225, 0.5512, 0.5833, 0.5930, 0.6106, 0.6426, 0.6608, 0.6892, 0.7008, 0.7335, 0.7597,
           0.7904, 0.8036, 0.8230, 0.8298, 0.8376, 0.8458, 0.8551, 0.8706, 0.8784, 0.8896, 0.8839, 0.8921, 0.8997]

plt.figure()
plt.xlabel('Epoch')
plt.ylabel('Loss')

l1, = plt.plot(epoch, loss_train, color='blue', linewidth=2.0, label='train_loss')
l2, = plt.plot(epoch, loss_val, color='red', linewidth=2.0, label='validation_loss')

plt.legend(handles=[l1, l2])

plt.figure(num=2)
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
l1, = plt.plot(epoch, acc_train, color='blue', linewidth=2.0, label='train_accuracy')
l2, = plt.plot(epoch, acc_val, color='red', linewidth=2.0, label='validation_accuracy')

plt.show()