import monpa
from monpa import utils

import csv
import json
from collections import Counter

import phrase

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

def getListFromCSV(category):
    with open('limit_{}.csv'.format(category), newline='', encoding='utf-8') as file:
        lst = list(csv.reader(file))
    return lst

def COUNTER2JSON(category, counter, frqtype='tf'):
    with open('{}_{}.json'.format(frqtype, category), 'w') as file:
        json.dump(counter, file)
        print('Save Counter Complete')

def JSON2COUNTER(category, frqtype='tf'):
    with open('{}_{}.json'.format(frqtype, category), 'r') as file:
        counter = Counter(json.load(file))
        print('Load Counter Complete')
        return counter

def PhraseList2JSON(phraselist):
    with open('phraselist.json', 'w') as file:
        json.dump(phraselist, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        print('Save Phrase List Complete')

def JSON2PhraseList(path='phraselist.json'):
    with open(path, 'r') as file:
        dictlist = json.load(file)
    ret_list = []
    for elm in dictlist:
        ret_list.append(phrase.Phrase(**elm))
    print('Load Phrase List Complete')
    return ret_list

if __name__ == '__main__':
    lst = getListFromCSV('up')
    print(lst[1][1])
    print(getPhraseLongEnough(lst[1][1]))
    print(getPhraseLongEnoughImproved(lst[1][1]))