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

from frequencies import *
from doc_utils import *

from phrase import *

def generateUPDOWNlist(lmt100=True, show_detail=False, show_namelist=False):
    phraselist = JSON2PhraseList()
    phraselist.sort(key=lambda x: x.lift_up, reverse=True)
    uplist = [i for i in phraselist if i.supp_up > 0.105]
    up_namelist = showPhraseList(uplist, 200, show_detail=show_detail)

    phraselist.sort(key=lambda x: x.chisq_down, reverse=True)
    downlist = [i for i in phraselist if i.supp_down > 0.015 and i.conf_down > 0.2 and i.lift_down > 1]
    down_namelist = showPhraseList(downlist, 200, show_detail=show_detail)

    if show_namelist:
        print('\n------------------------------------------------------------------------------------\n')
        print('UP-DN')
        showNameList([i for i in up_namelist if i not in down_namelist])
        print('\nDN-UP')
        show_namelist: showNameList([i for i in down_namelist if i not in up_namelist])

    if lmt100: return up_namelist[0:100], down_namelist[0:100]
    else: return up_namelist, down_namelist

def main():
    up_list_100, down_list_100 = generateUPDOWNlist(lmt100=True, show_detail=False, show_namelist=False)
    showNameList(up_list_100)
    showNameList(down_list_100)

def test():
    pass

if __name__ == '__main__':
    main()
