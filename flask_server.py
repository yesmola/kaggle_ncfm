import flask
import os
from flask import send_file
import multiprocessing
from backend import func

app = flask.Flask(__name__)

file_path = '/home/yuanye/backend'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        f.save("/home/yuanye/backend/ori_imgs/test.jpg")
        FishNames = ['ALB', 'BET', 'DOL', 'LAG', 'NoF', 'OTHER', 'SHARK', 'YFT']
        result = func()
        # result = os.path.join(file_path, 'results.csv')
        # os.system("rm /home/yuanye/backend/ori_imgs/*")
        return FishNames[result.index(max(result))]


if __name__ == '__main__':
    app.run()
