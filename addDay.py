from anki.find import Finder
from anki.hooks import addHook
from aqt import mw
from aqt.qt import QAction
from aqt.utils import getText, showWarning, tooltip
from anki.lang import _
from .config import getIntervalCoefficient, getIntervalForNegativeCoefficient
# From https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except


def RepresentsInt(s):
    try:
        return int(s)
    except ValueError:
        return None


def getDelay():
    return getDelayWithResponse()[0]


def getDelayWithResponse():
    (s, r) = getText("How many days would you like to postpone your cards? (negative number to subtract days)")
    if r:
        return (RepresentsInt(s), r)
    return (None, r)


def getReviewCards():
    finder = Finder(mw.col)
    cids = finder.findCards("is:review")
    return cids


def addDelay(cids):
    (delay, delayResp) = getDelayWithResponse()
    if delay is None:
        if delayResp:
            showWarning("Please enter an integral number of days")
        return

    mw.checkpoint("Adding delay")
    mw.progress.start()

    ivlDelay = max(0, round(delay * (getIntervalCoefficient()
                                     if delay > 0 else getIntervalForNegativeCoefficient())))
    for cid in cids:
        card = mw.col.getCard(cid)
        if card.type != 2:
            continue
        card.ivl += ivlDelay
        if card.odid:  # Also update cards in filtered decks
            card.odue += delay
        else:
            card.due += delay
        card.flush()

    mw.progress.finish()
    mw.col.reset()
    mw.reset()

    tooltip(_("""Delay added."""))
