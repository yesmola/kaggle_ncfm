import flask
import os
from flask import *
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

        config = tf.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = 0.5
        set_session(tf.Session(config=config))
        result = func()
        # result = os.path.join(file_path, 'results.csv')
        # os.system("rm /home/yuanye/backend/ori_imgs/*")
        return render_template('result.html', t1=result[0], t2=result[1], t3=result[2], t4=result[3],
                               t5=result[4], t6=result[5], t7=result[6], t8=result[7])


if __name__ == '__main__':
    app.run()
