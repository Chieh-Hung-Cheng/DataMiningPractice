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
    phraselist.sort(key=lambda x: x.lift_up, reverse=True)
    phraselist = [i for i in phraselist if i.supp_up>0.3]
    showList(phraselist, 100)

def test():
    pass

if __name__ == '__main__':
    main()
