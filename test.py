import json
from vocabulary.vocabulary import Vocabulary as vb

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

print (define_word ("lemon"))