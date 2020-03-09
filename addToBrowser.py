from anki.hooks import addHook
from anki.lang import _

from .addDay import *


def addToBrowser(fun, text, shortcut=None):
    """fun -- function taking as argument: the browser
    text -- what to enter in the menu
    shortcut
    """
    def aux(browser):
        action = browser.form.menuEdit.addAction(text)
        action.triggered.connect(lambda: fun(browser))
    addHook("browser.setupMenus", aux)


def runBrowser(browser):
    cids = browser.selectedCards()
    addDelay(cids)


addToBrowser(runBrowser, _("Postpone cards"))
