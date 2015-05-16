# coding: UTF-8
import sys
import time
import numpy as np
from numpy.fft import fft

import threading as th
import flask as fl
from flask import Flask, render_template, request, Response, redirect, url_for
from server import MuseServer


app = Flask(__name__)


def serve():
    t = 5

    while 1:
        server.acc_lock.acquire()
        tmp = list(zip(*server.acc_list))
        server.acc_list = []
        server.acc_lock.release()

        if tmp:
            size = len(tmp[0])
            fs = [i / t for i in range(size // 2)]
            tmp = [np.array(x) - sum(x) / len(x) for x in tmp]
            acc_fft = [fft(x)[: size // 2] for x in tmp]
            imax = [sorted(enumerate(x), key=lambda k: abs(k[1]))[-1] for x in acc_fft]
            print(fs[imax[0][0]], fs[imax[0][0]] * 60)

        time.sleep(t)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bpm')
def bpm():
    return Response("100", mimetype="text/event-stream")


if __name__ == '__main__':
    server = MuseServer()
    server.start()

    ser = th.Thread(target=serve)
    ser.start()
    print("Starting local server")
    # serve()
    app.run("0.0.0.0", port=8080)

