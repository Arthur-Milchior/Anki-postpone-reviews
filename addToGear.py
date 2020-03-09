from anki.find import Finder
from anki.hooks import addHook
from anki.lang import _
from aqt import mw

from .addDay import *


def addActionToGear(fun, text):
    """fun -- takes an argument, the did
    text -- what's written in the gear."""
    def aux(m, did):
        a = m.addAction(text)
        a.triggered.connect(lambda b, did=did: fun(did))
    addHook("showDeckOptions", aux)


def cidsInDid(did):
    deck = mw.col.decks.get(did)
    deckName = deck['name']
    return mw.col.findCards(f"\"deck:{deckName}\"")


def postponeFromDid(did):
    cids = cidsInDid(did)
    addDelay(cids)


addActionToGear(postponeFromDid, _("Postpone cards"))
