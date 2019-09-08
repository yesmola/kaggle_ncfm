import flask
import os
from flask import send_file
from backend import func
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

app = flask.Flask(__name__)

file_path = '/home/yuanye/backend'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        f.save("/home/yuanye/backend/ori_imgs/test.jpg")
        fish = ['ALB', 'BET', 'DOL', 'LAG', 'NoF', 'OTHER', 'SHARK', 'YFT']
        config = tf.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = 0.5
        set_session(tf.Session(config=config))
        result = func()
        # result = os.path.join(file_path, 'results.csv')
        # os.system("rm /home/yuanye/backend/ori_imgs/*")
        return fish[result.index(max(result))]


if __name__ == '__main__':
    app.run()
