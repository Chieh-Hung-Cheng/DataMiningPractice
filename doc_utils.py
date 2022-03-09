import monpa
import csv
import json
from collections import Counter


def getPhraseLongEnough(sentance, typ = 'LIST'):
    slices = monpa.cut(sentance)
    if typ == 'LIST': return [i for i in slices if len(i) >= 2]
    elif typ == 'SET': return [i for i in set(slices) if len(i) >= 2]

def getListFromCSV(category):
    with open('limit_{}.csv'.format(category), newline='', encoding='utf-8') as file:
        lst = list(csv.reader(file))
    return lst

def COUNTER2JSON(category, counter, frqtype='tf'):
    with open('{}_{}.json'.format(frqtype, category), 'w') as file:
        json.dump(counter, file)

def JSON2COUNTER(category, frqtype='tf'):
    with open('{}_{}.json'.format(frqtype, category), 'r') as file:
        counter = Counter(json.load(file))
        return counter