import math
import numpy as np

import doc_utils
import phrase
import frequencies
from collections import Counter

def calc_tfCountVector(tfdoc_counter, phraselist200):
    ret_vec = []
    for phr in phraselist200:
        if phr.name in tfdoc_counter:
            ret_vec.append(tfdoc_counter[phr.name])
        else:
            ret_vec.append(0)
    return ret_vec

def calc_tfCountVectorList(tfdoc_counterlist, phraselist200):
    ret_vectorlist = []
    for tfdoc_counter in tfdoc_counterlist:
        ret_vectorlist.append(calc_tfCountVector(tfdoc_counter, phraselist200))
    return ret_vectorlist

# def calc_costhetalist(veclist, tgtidx):
def calc_costhetalist(veclist, tgtvec):
    #tgtvec = veclist[tgtidx]
    tgtvec_norm = np.linalg.norm(tgtvec)
    ret_costhetalist = []

    for idx, vec in enumerate(veclist):
        costheta = np.dot(tgtvec, vec) / (tgtvec_norm*np.linalg.norm(vec))
        ret_costhetalist.append((idx, costheta.tolist()))
    return ret_costhetalist

def findMostRelevantArticles(tgtidx, phraselist, lmttyp, num=5):
    tfdoc_counterlist = doc_utils.JSON2COUNTERLIST('up') if lmttyp=='up' else doc_utils.JSON2COUNTERLIST('down')
    doc_list = doc_utils.getListFromCSV('up') if lmttyp=='up' else doc_utils.getListFromCSV('down')
    vectorlist = calc_tfCountVectorList(tfdoc_counterlist, phraselist)
    costheta_list = calc_costhetalist(vectorlist, vectorlist[tgtidx]) #tgtidx)
    costheta_list_sorted = sorted(costheta_list, key=lambda x: x[1], reverse=True)
    for i in range(5):
        if i==0: print('Query index:{} \nContent:\n{}\n'.format(tgtidx, doc_list[costheta_list_sorted[i][0]]))
        else:
            print('Relevance NO.{}, with Cosine(Theta)={}'.format(i, costheta_list_sorted[i][1]))
            print('Content:\n{}\n'.format(doc_list[costheta_list_sorted[i][0]]))

def searchByString(ArticleString, phraselist200, knn_categorize=False):
    tgtctr = Counter(frequencies.getPhraseLongEnoughImproved(ArticleString))
    tgtvec = calc_tfCountVector(tgtctr, phraselist200)

    tfdoc_counterlist = doc_utils.JSON2COUNTERLIST('up')+doc_utils.JSON2COUNTERLIST('down')
    doc_list = doc_utils.getListFromCSV('up') + doc_utils.getListFromCSV('down')
    vectorlist = calc_tfCountVectorList(tfdoc_counterlist, phraselist200)

    costheta_list = calc_costhetalist(vectorlist, tgtvec)
    costheta_list_sorted = sorted(costheta_list, key=lambda x: x[1], reverse=True)

    for i in range(5):
        print('Relevance NO.{}, with Cosine(Theta)={}'.format(i+1, costheta_list_sorted[i][1]))
        print('Content:\n{}\n'.format(doc_list[costheta_list_sorted[i][0]]))

    if knn_categorize:
        num = 5
        cnt = [0,0]
        for idx in range(num):
            if costheta_list_sorted[idx][0] < phrase.N_up: cnt[0]+=1
            else: cnt[1]+=1
        if(cnt[0]>=cnt[1]): print('KNN categorize as UP, with score UP:{} >= DOWN:{}'.format(cnt[0], cnt[1]))
        else: print('KNN categorize as DOWN, with score UP{} < DOWN{}'.format(cnt[0], cnt[1]))


if __name__ == '__main__':
    pass