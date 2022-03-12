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

def main():
    force = False
    if (not os.path.exists('tf_up.json')) or force: generateAllFreqs()
    if (not os.path.exists('phraselist.json')) or force: generatePhraseList()
    if (not os.path.exists('tfdoc_up.json')) or force: generateTermFreqEachDoc()
    phraselist_up, phraselist_down = generateUPDOWNlist()
    showNameList(phraselist_up)
    showNameList(phraselist_down)
    findMostRelevantArticles(66, phraselist_up, 'up')

def test():
    phraselist_up, phraselist_down = generateUPDOWNlist()
    showNameList(phraselist_up, phraselist_down)
if __name__ == '__main__':
    main()
