import csv
import json
from collections import Counter

import phrase



def getListFromCSV(category):
    with open('limit_{}.csv'.format(category), newline='', encoding='utf-8') as file:
        lst = list(csv.reader(file))
        lst = lst[1:]
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

def COUNTERLIST2JSON(category, counterlist):
    with open('tfdoc_{}.json'.format(category), 'w') as file:
        json.dump(counterlist, file)
    print('Save Counterlist Complete')

def JSON2COUNTERLIST(category):
    with open('tfdoc_{}.json'.format(category), 'r') as file:
        counterlist = json.load(file)
    ret_counterlist = [Counter(i) for i in counterlist]
    print('Load Counterlist Complele')
    return ret_counterlist

if __name__ == '__main__':
    pass