from yahoo_finance import Share
import json

import warnings
import requests
import contextlib

try:
    from functools import partialmethod
except ImportError:
    # Python 2 fallback: https://gist.github.com/carymrobbins/8940382
    from functools import partial

    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self

            return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

@contextlib.contextmanager
def no_ssl_verification():
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)

    warnings.filterwarnings('ignore', 'Unverified HTTPS request')
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request


def getPrice(tkr):
    tkr = tkr.upper()
    url = 'https://www.blackrock.com/tools/hackathon/security-data?identifiers=' + tkr + '&query=' + tkr
    params = dict(exchangeAcronym = "NASDAQ")
    resp = requests.get(url = url, params = params)
    data = json.loads(resp.text)
    exchange = str(data['resultMap']['SECURITY'][0]['exchangeAcronym'])
    assetType = str(data['resultMap']['SECURITY'][0]['assetType'])
    stock = Share(tkr)
    name = stock.get_name()
    volume = stock.get_volume()
    price = stock.get_price()
    currency = stock.get_currency()
    change = str(stock.get_percent_change())
    if("+" in change):
        change = "up " + change[1:]
    elif ("-" in change):
        change = "down " + change[1:]
    else:
        change = "same as yesterday."
    ret = name + " is a " + assetType.lower() + " and has a trade volume of " + volume + " shares with a value of " + str(price) + " " + currency + " per share which is " + str(change) + " from yesterday on the " + exchange + " exchange."
    return ret

def isValid(tkr):
    tkr = tkr.upper()
    if (" " in tkr):
        return False
    stock = Share(tkr)
    name = stock.get_name()
    if(name == None):
        return False
    else:
        return True
