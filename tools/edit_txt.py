import os
path = '/usr/kaggle/kaggle'
with open(os.path.join(path, 'cfg_fish', 'test.txt'), 'w') as f:
    for fname in os.listdir(os.path.join(path, 'test_stg1')): f.write(path+'/test_stg1/'+fname+'\n')
    for fname in os.listdir(os.path.join(path, 'test_stg2')): f.write(path+'/test_stg2/'+fname+'\n')

with open(os.path.join(path, 'cfg_fish', 'test.txt')) as f:
    results = f.readlines()

with open(os.path.join(path, 'cfg_fish', 'test.txt'), 'w') as f:
    for result in results:
        result = result.replace('._', '')
        f.write(result)