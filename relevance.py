import math
import numpy as np

import doc_utils
import phrase

def calc_tfCountVector(tfdoc_counter, phraselist100):
    ret_vec = []
    for phrase in phraselist100:
        if phrase.name in tfdoc_counter:
            ret_vec.append(tfdoc_counter[phrase.name])
        else:
            ret_vec.append(0)
    return ret_vec

def calc_tfCountVectorList(tfdoc_counterlist, phraselist100):
    ret_vectorlist = []
    for tfdoc_counter in tfdoc_counterlist:
        ret_vectorlist.append(calc_tfCountVector(tfdoc_counter, phraselist100))
    return ret_vectorlist

def calc_costhetalist(veclist, tgtidx):
    tgtvec = veclist[tgtidx]
    tgtvec_norm = np.linalg.norm(tgtvec)
    ret_costhetalist = []

    for idx, vec in enumerate(veclist):
        costheta = np.dot(tgtvec, vec) / (tgtvec_norm*np.linalg.norm(vec))
        ret_costhetalist.append((idx, costheta.tolist()))
    return ret_costhetalist

def findMostRelevantArticles(tgtidx, phraselist, lmttyp, num=5):
    tfdoc_counterlist = doc_utils.JSON2COUNTERLIST('up') if lmttyp=='up' else doc_utils.JSON2COUNTERLIST('down')
    doc_list = doc_utils.getListFromCSV('up') if lmttyp=='up' else doc_utils.getListFromCSV('up')
    vectorlist = calc_tfCountVectorList(tfdoc_counterlist, phraselist)
    costheta_list = calc_costhetalist(vectorlist, tgtidx)
    costheta_list_sorted = sorted(costheta_list, key=lambda x: x[1], reverse=True)
    for i in range(5):
        if i==0: print('Query index:{} \nContent:\n{}\n'.format(tgtidx, doc_list[costheta_list_sorted[i][0]]))
        else:
            print('Relevance NO.{}, with Cosine(Theta)={}'.format(i, costheta_list_sorted[i][1]))
            print('Content:\n{}\n'.format(doc_list[costheta_list_sorted[i][0]]))


if __name__ == '__main__':
    pass