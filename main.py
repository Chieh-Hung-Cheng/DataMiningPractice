import os
import sys
import time

import numpy as np
import math
from tqdm import tqdm
import json

import monpa
from collections import Counter
import csv


def getPhraseLongEnough(sentance, typ = 'LIST'):
    slices = monpa.cut(sentance)
    '''ret_slices = []
    for i in slices:
        if(len(i)>=2):
            ret_slices.append(i)
    return ret_slices'''
    if typ == 'LIST': return [i for i in slices if len(i) >= 2]
    elif typ == 'SET': return [i for i in set(slices) if len(i)>=2]

def getListFromCSV(category):
    with open('limit_{}.csv'.format(category), newline='', encoding='utf-8') as file:
        lst = list(csv.reader(file))
    return lst


def generateTermFreq(category, save=True):
    # category = 'up' || 'down'
    csvlist = getListFromCSV(category)

    counter = Counter()
    for idx, elm in enumerate(tqdm(csvlist)):
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

    if save: COUNTER2JSON(category)

def COUNTER2JSON(category, counter):
    with open('tf_{}.json'.format(category), 'w') as file:
        json.dump(counter, file)

def JSON2COUNTER(category):
    with open('tf_{}.json'.format(category), 'r') as file:
        counter = Counter(json.load(file))
        return counter


def main():
    generateDocFreq('up', False)
    print(JSON2COUNTER('up'))



if __name__ == '__main__':
    main()
