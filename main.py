# coding: UTF-8
import sys
import time
import itertools
import numpy as np
from numpy.fft import fft


import threading as th
import flask as fl
from flask import Flask, render_template, request, Response, redirect, url_for
from server import MuseServer
from search_yt_by_word import Search

app = Flask(__name__)
calculatedBeat = 0
mainLock = th.RLock()
search = Search()
currentSong = ""
yt_id = ""
itunes_link = ""


def serve():
    global calculatedBeat, currentSong, yt_id, itunes_link

    t = 5

    while 1:
        server.acc_lock.acquire()
        tmp = list(zip(*server.acc_list))
        server.acc_list = []
        server.acc_lock.release()

        if tmp and tmp[0]:
            size = len(tmp[0])
            fs = [i / t for i in range(size // 2)]
            tmp = [np.array(x) - sum(x) / len(x) for x in tmp]
            acc_fft = [fft(x)[: size // 2] for x in tmp]
            imax = [sorted(enumerate(x), key=lambda k: abs(k[1]))[-1] for x in acc_fft]
            print(fs[imax[0][0]], fs[imax[0][0]] * 60)

            mainLock.acquire()
            calculatedBeat = fs[imax[0][0]] * 60
            local_beat = calculatedBeat
            mainLock.release()

            search_result = search.search_all(local_beat)

            mainLock.acquire()
            currentSong, yt_id, itunes_link = search_result
            mainLock.release()

        time.sleep(t)


@app.route('/')
def index():
    global calculatedBeat

    mainLock.acquire()
    calculatedBeat = 0
    yt_id = ""
    search.clear()
    mainLock.release()

    return render_template('index.html')

@app.route('/bpm')
def bpm():
    def events():
        while 1:
            mainLock.acquire()
            tmpCalculatedBeat = calculatedBeat
            mainLock.release()
            if tmpCalculatedBeat != 0 and yt_id != "" and currentSong != "":
                yield "event: calculated\ndata: {\"bpm\": %d, \"song\": \"%s\", \"yt_id\": \"%s\", \"itunes_link\": \"%s\"}\n\n" % (tmpCalculatedBeat, currentSong, yt_id, itunes_link)

            server.acc_lock.acquire()
            tmpMove = 0
            if server.acc_list and server.acc_list[-1]:
                tmpMove = server.acc_list[-1][0]
            server.acc_lock.release()
            if tmpMove != 0:
                yield "event: move\ndata: %d\n\n" % (tmpMove)

            #yield "event: test\ndata: %d\n\n" % (calculatedBeat)
            time.sleep(0.02)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


if __name__ == '__main__':
    server = MuseServer()
    server.start()

    ser = th.Thread(target=serve)
    ser.start()
    print("Starting local server")
    # serve()
    app.run("0.0.0.0", port=8080, threaded=True)

