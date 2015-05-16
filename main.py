# coding: UTF-8
import time
import numpy as np
from numpy.fft import fft

import flask as fl
from flask import Flask, render_template, request, Response, redirect, url_for
from server import acc_lock, acc_list


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=8080)

    if 0:
        t = 5

        while 1:
            acc_lock.acquire()
            tmp = list(zip(*acc_list))
            acc_list = []
            acc_lock.release()

            if tmp:
                size = len(tmp[0])
                fs = [i / t for i in range(size // 2)]
                tmp = [np.array(x) - sum(x) / len(x) for x in tmp]
                acc_fft = [fft(x)[: size // 2] for x in tmp]
                imax = [sorted(enumerate(x), key=lambda k: abs(k[1]))[-1] for x in acc_fft]
                print(fs[imax[0][0]], fs[imax[0][0]] * 60)

            time.sleep(t)
