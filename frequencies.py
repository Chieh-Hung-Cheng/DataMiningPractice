from tqdm import tqdm
import doc_utils
from collections import Counter

def generateTermFreq(save=True):
    categories = ['up', 'down']
    counter_ttl = Counter()
    for category in categories:
        csvlist = doc_utils.getListFromCSV(category)

        counter = Counter()
        for idx, elm in enumerate(tqdm(csvlist)):
            if idx == 0: continue
            counter += Counter(doc_utils.getPhraseLongEnoughImproved(elm[1], typ='LIST'))
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
            if idx == 0: continue
            counter += Counter(doc_utils.getPhraseLongEnoughImproved(elm[1], typ='SET'))
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

if __name__ == '__main__':
    generateAllFreqs()