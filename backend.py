import os
from PIL import Image
from shutil import copyfile
import re
from predict_fish import predict_imgs


def func():
    img_path = '/home/yuanye/backend/ori_imgs'
    code_path = '/usr/kaggle/kaggle/darknet'
    path = '/home/yuanye/backend/cropped_imgs'

    with open(code_path + '/test.txt', 'w') as f:
        imgs = os.listdir(img_path)
        f.truncate()
        for img in imgs:
            f.write(os.path.join(img_path, img) + '\n')
    f.close()
    os.system("cd /usr/kaggle/kaggle/darknet; ./darknet detector test cfg/"
              "voc.data cfg/yolov3-voc.cfg weights/yolov3-voc_7000.weights -ext_output < test.txt > result.txt")

    with open(code_path + '/result.txt') as f:
        results = f.readlines()
    line_id, file_id = 0, 0
    detects = []

    current_name = ''
    while True:
        if line_id + 1 == len(results):
            if results[line_id].startswith('Enter'):
                if results[line_id] == 'Enter Image Path: ':
                    break
                # result1 = results[line_id].split('/')
                # result1 = results[line_id].split('/')
                name = results[line_id].split('/')[5].split(':')[0]
                fname = name
                current_name = fname
                copyfile(os.path.join(img_path, fname), os.path.join(path, 'cls', 'test_cls', name))
            else:
                detects.append([int(s) for s in re.findall(r'\d+', results[line_id])])
                detects = sorted(detects)
                im = Image.open(os.path.join(img_path, current_name))
                bbox = detects[-1][1:]
                bbox = [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]
                im = im.crop(bbox)
                im.save(os.path.join(path, 'cls', 'test_cls', current_name))
            break

        if results[line_id].startswith('Enter'):
            result = results[line_id]
            stgs = result.split('/')
            stg = stgs[4]
            name = result.split('/')[5].split(':')[0]
            fname = name
            current_name = fname
            if results[line_id + 1].startswith('Enter'):
                copyfile(os.path.join(img_path, fname), os.path.join(path, 'full', 'test_cls2', name))
                file_id += 1
            else:
                detects = []

        elif (results[line_id].startswith('fish')):
            detects.append([int(s) for s in re.findall(r'\d+', results[line_id])])
            if results[line_id + 1].startswith('Enter'):
                im = Image.open(os.path.join(img_path, current_name))
                bbox = detects[-1][1:]
                bbox = [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]
                im = im.crop(bbox)
                im.save(os.path.join(path, 'cls', 'test_cls', current_name))
                file_id += 1
        else:
            line_id += 1
            continue
        line_id += 1

    f.close()

    # os.system("rm /home/yuanye/backend/ori_imgs/*")

    f_submit = open('/home/yuanye/backend/results.csv', 'w')
    f_submit.truncate()
    f_submit.write('image,ALB,BET,DOL,LAG,NoF,OTHER,SHARK,YFT\n')
    f_submit.close()
    num_cls = len(os.listdir("/home/yuanye/backend/cropped_imgs/cls/test_cls"))
    if num_cls > 0:
        predict_imgs(False, num_cls)

    num_full = len(os.listdir("/home/yuanye/backend/cropped_imgs/full/test_cls2"))
    if num_full > 0:
        predict_imgs(True, num_full)


if __name__ == '__main__':
    func()

