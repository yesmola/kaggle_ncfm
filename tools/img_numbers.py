import os

root_path = '/home/yuanye/fish_data/preprocessed_train'

classes = ['ALB', 'BET', 'DOL', 'LAG', 'NoF', 'OTHER', 'SHARK', 'YFT']
bad_nums = [8, 1, 0, 0, 0, 0, 1, 3]

# 原始图像个数：1711 199 117 67 465 299 175 731
ori_nums = [1711, 199, 117, 67, 465, 299, 175, 731]
ori_sum = 3764

aug_nums = [3422, 1194, 702, 804, 465, 1794, 1050, 2924]
aug_sum = 12355
for cls in classes:
    print('{}:{}'.format(cls, len(os.listdir(os.path.join(root_path, cls)))))


