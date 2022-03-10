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


def main():
    phraselist = JSON2PhraseList()
    '''phraselist.sort(key=lambda x: x.lift_up, reverse=True)
    subphraselist = [i for i in phraselist if i.supp_up>0.13]
    showList(subphraselist, 200)'''

    phraselist.sort(key=lambda x:x.tf_down, reverse=True)
    subphraselist = [i for i in phraselist if i.supp_down>0.015 and i.conf_down>0.2 and  i.lift_down>1]
    showList(subphraselist, 200)

def test():
    pass

if __name__ == '__main__':
    main()
