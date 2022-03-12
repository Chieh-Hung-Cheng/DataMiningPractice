import argparse
import os
import sys
import time
parser = argparse.ArgumentParser()
parser.parse_args()

import numpy as np
import math
from tqdm import tqdm
import json

import monpa
from collections import Counter
import csv

from frequencies import *
from doc_utils import *
from phrase import *
from relevance import *
from NaiveBayes import *

def main():
    force = False
    if (not os.path.exists('tf_up.json')) or force: generateAllFreqs()
    if (not os.path.exists('phraselist.json')) or force: generatePhraseList()
    if (not os.path.exists('tfdoc_up.json')) or force: generateTermFreqEachDoc()
    # Q1
    phraselist_up, phraselist_down = generateUPDOWNlist()
    showNameList(phraselist_up)
    showNameList(phraselist_down)

    # Q2
    findMostRelevantArticles(66, phraselist_up, 'up')
    findMostRelevantArticles(55, phraselist_down, 'down')

    # Q3
    lmttyp = 'down'
    tgtidx = 69
    sample_content = (doc_utils.getListFromCSV('up') if lmttyp == 'up' else doc_utils.getListFromCSV('down'))[tgtidx]
    sample_tfcounter = (doc_utils.JSON2COUNTERLIST('up') if lmttyp == 'up' else doc_utils.JSON2COUNTERLIST('down'))[tgtidx]
    print('\n\n\n', sample_content)
    classifyByBayes(sample_tfcounter, *phrase.generateUPDOWNlist())

def test():
    phraselist_up, phraselist_down = generateUPDOWNlist()
    showNameList(phraselist_up, phraselist_down)
if __name__ == '__main__':
    main()
