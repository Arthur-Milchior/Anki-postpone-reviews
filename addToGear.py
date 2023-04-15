from anki.find import Finder
from aqt.gui_hooks import deck_browser_will_show_options_menu
from aqt import mw

from .addDay import addDelay


def addActionToGear(fun, text):
    """fun -- takes an argument, the did
    text -- what's written in the gear."""
    def aux(m, did):
        a = m.addAction(text)
        a.triggered.connect(lambda b, did=did: fun(did))
    deck_browser_will_show_options_menu.append(aux)


def cidsInDid(did):
    deck = mw.col.decks.get(did)
    deckName = deck['name']
    return mw.col.findCards(f"\"deck:{deckName}\"")


def postponeFromDid(did):
    cids = cidsInDid(did)
    addDelay(cids)


addActionToGear(postponeFromDid, "Postpone cards")
