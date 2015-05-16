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
    oci1_time, oci1_eeg = parse("data/oci1.csv", "/muse/eeg")
    oci2_time, oci2_eeg = parse("data/oci2.csv", "/muse/eeg")
    clean_time, clean_eeg = parse("data/clean.csv", "/muse/eeg")

    size = min(len(oci1_time), len(oci2_time), len(clean_time))

    print(size, oci1_time[:size])

    plt.plot(correlate2(oci1_eeg[0][:size], oci2_eeg[0][:size]) + 100)
    plt.plot(correlate2(oci1_eeg[0][:size], clean_eeg[0][:size]) - 100)
    plt.plot(correlate2(oci2_eeg[0][:size], clean_eeg[0][:size]))

    plt.legend(["oci1-2", "oci1-clean", "oci2-clean"])

    plt.show()



