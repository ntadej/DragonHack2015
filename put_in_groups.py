from sklearn import svm
from correlate import *

def naredi_grupe():
    """
    s clf.fit se nauči
    s clf.predict(X) dobiš prediction za X
    """
    yess = []
    nos = []
    nolen = 8
    yeslen = 9
    for i in range(nolen):
        nos.append(parse("data/yes-no/no%d.csv" % (i + 1), "/muse/eeg")[1])
    for i in range(yeslen):
        yess.append(parse("data/yes-no/yes%d.csv" % (i + 1), "/muse/eeg")[1])

    size = min([len(yes[0]) for yes in yess] + [len(no[0]) for no in nos])

    vsi = yess[:-1] + nos[:-1]
    vsi2 = []
    dolzinaSignala = 700
    for i in vsi:
        vsi2 += [i[0][:dolzinaSignala]]
    pravilni = ['yes' for i in range(yeslen-1)]
    pravilni += ['no' for i in range(nolen-1)]
    clf = svm.SVC()
    clf.fit(vsi2, pravilni)
    print(clf.predict(yess[-1][0][:dolzinaSignala]))
    print(clf.predict(nos[-1][0][:dolzinaSignala]))

naredi_grupe()