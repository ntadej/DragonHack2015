import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt


def correlate(a, b):
    return ifft(fft(a) * np.conjugate(fft(b))) / len(a)


def correlate2(a, b, norm=1):
    N = len(a)
    at = list(a) + [0] * N
    bt = list(b) + [0] * N
    res = ifft(fft(at) * np.conjugate(fft(bt)))[:N]
    if not norm:
        return res / N
    res2 = []
    for n, c in enumerate(res):
        res2.append(c / (N - n))

    return np.array(res2)


def parse(filename, sensor):
    f = open(filename, "r")
    times = []
    data = []
    time0 = 0
    for line in f:
        lsplit = line.split(", ")
        if not time0:
            time0 = float(lsplit[0])
        if lsplit[1] == sensor:
            times.append(float(lsplit[0]) - time0)
            data.append(list(map(float, lsplit[2:])))

    data = list(zip(*data))

    data = list(map(lambda x: np.array(x) - sum(x) / len(x), data))

    return times, data


if __name__ == "__main__":
    yess = []
    nos = []
    nolen = 8
    yeslen = 9
    for i in range(nolen):
        nos.append(parse("data/yes-no/no%d.csv" % (i + 1), "/muse/eeg")[1])
    for i in range(yeslen):
        yess.append(parse("data/yes-no/yes%d.csv" % (i + 1), "/muse/eeg")[1])

    size = min([len(yes[0]) for yes in yess] + [len(no[0]) for no in nos])

    print(size)
    sens_n = 3
    for i, yes1 in enumerate(yess):
        for j, yes2 in enumerate(yess):
            if i == j:
                continue
            plt.plot(correlate2(yes1[sens_n][:size], yes2[sens_n][:size]), "b")
    for i, no1 in enumerate(nos):
        for j, no2 in enumerate(nos):
            if i == j:
                continue
            plt.plot(correlate2(no1[sens_n][:size], no2[sens_n][:size]), "k", alpha=0.7)

    for yes1 in yess:
        for no2 in nos:
            plt.plot(correlate2(yes1[sens_n][:size], no2[sens_n][:size]), "r", alpha=0.5)

    plt.ylim(-1000, 1000)
    plt.show()



