import csv
import string

f1 = open('/home/yuanye/fish_data/submit2.csv', 'a')
f2 = open('/home/yuanye/fish_data/submit1_full_aug.csv', 'r')
f3 = open('/home/yuanye/fish_data/submit2_full_aug.csv', 'r')
f4 = open('/home/yuanye/fish_data/submit2_cls_aug.csv', 'r')

reader1 = csv.reader(f2)
reader2 = csv.reader(f3)
reader3 = csv.reader(f4)

for i, row in enumerate(reader1):
    if i == 0:
        continue
    # image_name = 'test_stg2/' + row[0]
    image_name = row[0]
    data = ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[
        7] + ',' + row[8]
    f1.write('%s\n' % (image_name + data))

for i, row in enumerate(reader2):
    if i == 0:
        continue
    image_name = 'test_stg2/' + row[0]
    # image_name = row[0]
    data = ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[
        7] + ',' + row[8]
    f1.write('%s\n' % (image_name + data))

for i, row in enumerate(reader3):
    if i == 0:
        continue
    image_name = 'test_stg2/' + row[0]
    # image_name = row[0]
    data = ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[
        7] + ',' + row[8]
    f1.write('%s\n' % (image_name + data))

f1.close()
f2.close()
f3.close()
f4.close()
print('Submission file successfully generated!')