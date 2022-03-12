from tqdm import tqdm
import doc_utils
from collections import Counter

import monpa
from monpa import utils

def getPhraseLongEnough(sentance, typ='LIST'):
    slices = monpa.cut(sentance)
    if typ == 'LIST': return [i for i in slices if len(i) >= 2]
    elif typ == 'SET': return [i for i in set(slices) if len(i) >= 2]

def getPhraseLongEnoughImproved(sentance, typ="LIST", part=False):
    short_sentances = utils.short_sentence(sentance)
    slices = []
    for elm in short_sentances:
        if part: slices += monpa.pseg(elm)
        else: slices += monpa.cut(elm)
    if typ == 'LIST':
        if part: return [i for i in slices if len(i[0]) >= 2]
        else : return [i for i in slices if len(i) >= 2]
    elif typ == 'SET':
        if part: [i for i in set(slices) if len(i[0]) >= 2]
        else: return [i for i in set(slices) if len(i) >= 2]

def generateTermFreq(save=True):
    categories = ['up', 'down']
    counter_ttl = Counter()
    for category in categories:
        csvlist = doc_utils.getListFromCSV(category)

        counter = Counter()
        for idx, elm in enumerate(tqdm(csvlist)):
            # if idx == 0: continue
            counter += Counter(getPhraseLongEnoughImproved(elm[1], typ='LIST'))
        print(counter)

        if save: doc_utils.COUNTER2JSON(category, counter)
        counter_ttl += counter
    print('TF_counter_ttl', counter_ttl)
    if save: doc_utils.COUNTER2JSON('all', counter_ttl, 'tf')

def generateDocFreq(save=True):
    categories = ['up', 'down']
    counter_ttl = Counter()
    for category in categories:
        csvlist = doc_utils.getListFromCSV(category)

        counter = Counter()
        for idx, elm in enumerate(tqdm(csvlist)):
            # if idx == 0: continue
            counter += Counter(getPhraseLongEnoughImproved(elm[1], typ='SET'))
        print(counter)

        if save: doc_utils.COUNTER2JSON(category, counter, frqtype='df')
        counter_ttl += counter
    print('DF_counter_ttl', counter_ttl)
    if save: doc_utils.COUNTER2JSON('all', counter_ttl, 'df')

def generateFreq(lmttyp, frqtyp):
    # Make it more succinct?
    pass

def generateAllFreqs(save=True):
    generateTermFreq(save)
    generateDocFreq(save)

def generateTermFreqEachDoc(save=True):
    categories = ['up', 'down']
    for category in categories:
        csvlist = doc_utils.getListFromCSV(category)

        counterlist = []
        for idx, elm in enumerate(tqdm(csvlist)):
            # if idx == 0: continue
            counterlist.append(getPhraseLongEnoughImproved(elm[1], typ='LIST'))
        if save: doc_utils.COUNTERLIST2JSON(category, counterlist)

if __name__ == '__main__':
    generateTermFreqEachDoc()