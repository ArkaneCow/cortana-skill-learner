import json
from vocabulary.vocabulary import Vocabulary as vb

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



def define_word(word):
    definitions = vb.meaning(word)
    if (definitions is None):
        return "Word not found"
    else:
        worddefs = json.loads(definitions)
        ret = word + ": "
        i = 0
        while (i < 4 and i < len(worddefs)):
            ret += str(i + 1) + ". " + worddefs[i]['text'] + "; "
            i+=1
        ret = ret[:-2]
        return ret

def synonym(word):
    syn = vb.synonym(word)
    if (syn == False):
        return "No Synonyms Founds"
    syns = json.loads(syn)
    ret = "Synonyms are "
    i = 0
    while (i < 4 and i < len(syns)):
        ret += syns[i]['text'] + ", "
        i += 1
    ret = ret[:-2]
    return ret


def antonym(word):
    ant = vb.antonym(word)
    if (ant == False):
        return "No Antonyms Found"
    ants = json.loads(ant)
    ret = "Antonyms are "
    i = 0
    while (i < 4 and i < len(ants)):
        ret += ants[i]['text'] + ", "
        i += 1
    ret = ret[:-2]
    return ret