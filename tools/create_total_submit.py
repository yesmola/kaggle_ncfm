import csv
import string

f1 = open('/home/yuanye/fish_data/submit.csv', 'a')
f2 = open('/home/yuanye/fish_data/submit2_full.csv', 'r')

reader = csv.reader(f2)

for i, row in enumerate(reader):
    if i == 0:
        continue
    image_name = 'test_stg2/' + row[0]
    # image_name = row[0]
    data = ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[
        7] + ',' + row[8]
    f1.write('%s\n' % (image_name + data))

f1.close()
f2.close()
print('Submission file successfully generated!')