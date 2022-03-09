from tqdm import tqdm
from doc_utils import *

def generateTermFreq(category, save=True):
    # category = 'up' || 'down'
    csvlist = getListFromCSV(category)

    counter = Counter()
    for idx, elm in enumerate(tqdm(csvlist)):
        if idx == 0: continue
        counter += Counter(getPhraseLongEnough(elm[1]))
    print(counter)
    if save: COUNTER2JSON(category, counter)

def generateDocFreq(category, save=True):
    csvlist = getListFromCSV(category)

    counter = Counter()
    for idx, elm in enumerate(tqdm(csvlist)):
        if idx == 0: continue
        counter += Counter(getPhraseLongEnough(elm[1], typ='SET'))
    print(counter)

    if save: COUNTER2JSON(category, counter, frqtype='df')

def generateAllFreqs(save=True):
    generateTermFreq('up', save)
    generateDocFreq('up', save)
    generateTermFreq('down', save)
    generateDocFreq('down', save)
    