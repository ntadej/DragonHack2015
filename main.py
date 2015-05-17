# coding: UTF-8
import sys
import time
import itertools
import json
import numpy as np
from numpy.fft import fft
from collections import deque

import threading as th
import flask as fl
from flask import Flask, render_template, request, Response, redirect, url_for
from server import MuseServer
from search_yt_by_word import Search
from detect_movement import pravila


app = Flask(__name__)
calculatedBeat = 0
mainLock = th.RLock()
search = Search()
currentSong = ""
yt_id = ""
itunes_link = ""

acc_data_num = 0
dq = deque()
headLock = th.RLock()

stopserve = False
stopserveLock = th.Lock()


def serve():
    global calculatedBeat, currentSong, yt_id, itunes_link, stopserve

    print("Starting server!!!")

    t = 5
    # time.sleep(t)
    while 1:
        stopserveLock.acquire()
        if stopserve:
            stopserve = False
            stopserveLock.release()
            print("Returning server1")
            return
        stopserveLock.release()






        acc_data_num = 0
        for i in range(10):
            stopserveLock.acquire()
            if stopserve:
                stopserve = False
                stopserveLock.release()
                print("Returning server2")
                return
            stopserveLock.release()

            server.acc_lock.acquire()
            tmp = list(zip(*server.acc_list))
            raw_tmp = tmp[:]
            server.acc_lock.release()

            n2 = len(tmp)
            tmp = tmp[acc_data_num:]
            acc_data_num = n2
            podatki = pravila(raw_tmp, duration=t/10)
            headLock.acquire()
            if "ndesno" in podatki:
                dq.append("ndesno")
            headLock.release()

            time.sleep(t / 10.0)



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



ser = th.Thread(target=serve)


@app.route('/restart')
def restart():
    print("restarting serve")
    global calculatedBeat, yt_id, ser, stopserve, server

    mainLock.acquire()
    calculatedBeat = 0
    yt_id = ""
    search.clear()
    mainLock.release()


    server.acc_lock.acquire()
    server.acc_list = []
    server.acc_lock.release()

    stopserveLock.acquire()
    stopserve = True
    stopserveLock.release()
    while True:
        stopserveLock.acquire()
        local = stopserve
        stopserveLock.release()
        if not local:
            ser = th.Thread(target=serve)
            ser.start()
            break

    return "100"



@app.route('/getnext')
def getnext():
    print("bpm")
    bpm = int(request.args.get("bpm", 80))
    print("bpm2")
    try:
        search_result = search.search_all(bpm)
    except Exception as e:
        print(e)
    print(search_result)

    song, yt, itunes = search_result

    return "{\"bpm\": %d, \"song\": \"%s\", \"yt_id\": \"%s\", " \
           "\"itunes_link\": \"%s\"}\n\n" % (bpm, song, yt, itunes)




@app.route('/')
def index():
    global calculatedBeat, yt_id

    mainLock.acquire()
    calculatedBeat = 0
    yt_id = ""
    search.clear()
    mainLock.release()

    return render_template('index.html')


@app.route('/status')
def status():
    def events():
        while 1:
            server.senstate_lock.acquire()
            event = server.senstate
            server.senstate_lock.release()
            if event:
                yield "event: status\ndata: %s\n\n" % (json.dumps(event))

            time.sleep(0.2)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


@app.route('/headswipe')
def headswipe():
    def events():
        while 1:
            headLock.acquire()
            event = len(dq) and dq.pop()
            dq.clear()
            headLock.release()
            if event != 0:
                yield "event: head\ndata: %s\n\n" % (event)

            time.sleep(0.1)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


@app.route('/blink')
def blink():
    def events():
        while 1:
            server.blink_lock.acquire()
            event = len(server.blink_list) and server.blink_list.pop()
            server.blink_lock.release()
            if event != 0:
                yield "event: blink\ndata: %s\n\n" % (event)

            time.sleep(0.05)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


@app.route('/jaw')
def jaw():
    def events():
        while 1:
            server.jaw_lock.acquire()
            event = len(server.jaw_list) and server.jaw_list.pop()
            server.jaw_lock.release()
            if event != 0:
                yield "event: jawclench\ndata: %s\n\n" % (event)

            time.sleep(0.05)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


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

    ser.start()
    print("Starting local server")
    # serve()
    app.run("0.0.0.0", port=8080, threaded=True)

