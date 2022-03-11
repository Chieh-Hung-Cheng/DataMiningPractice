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

def generateUPDOWNlist(lmt100=True, show_detail=False, show_name=False):
    phraselist = JSON2PhraseList()
    phraselist.sort(key=lambda x: x.lift_up, reverse=True)
    uplist = [i for i in phraselist if i.supp_up > 0.105]

    phraselist.sort(key=lambda x: x.chisq_down, reverse=True)
    downlist = [i for i in phraselist if i.supp_down > 0.015 and i.conf_down > 0.2 and i.lift_down > 1]

    if show_detail:
        showPhraseList(uplist)
        showPhraseList(downlist)
    if show_name:
        showNameList(uplist)
        showNameList(downlist)
    uplist_exclude = [i for i in uplist if i not in downlist]
    downlist_exclude = [i for i in downlist if i not in uplist]

    if lmt100: return uplist_exclude[0:100], downlist_exclude[0:100]
    else: return uplist_exclude, downlist_exclude


def main():
    if not os.path.exists('tf_up.json'): generateAllFreqs()
    if not os.path.exists('phraselist.json'): generatePhraseList()
    phraselist_up, phraselist_down = generateUPDOWNlist()
    showNameList(phraselist_up)
    showNameList(phraselist_down)

def test():
    pass

if __name__ == '__main__':
    main()
