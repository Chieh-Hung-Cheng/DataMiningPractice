import math

import doc_utils
import phrase


def calcCondiProbCgivenX(tfcounter, phraselist, lmttyp):
    ret_val = 0
    sum_all_tf = sum([i.tf_up for i in phraselist] if lmttyp=='up' else [i.tf_down for i in phraselist])
    for phr in phraselist:
        if phr.name in tfcounter:
            # print((phr.tf_up if lmttyp == 'up' else phr.tf_down) /sum_all_tf)
            ret_val += (phr.tf_up if lmttyp == 'up' else phr.tf_down) /sum_all_tf
    # ret_val *= (phrase.N_up if lmttyp == 'up' else phrase.N_down) / phrase.N_ttl # BIG PROBLEM
    return ret_val

def classifyByBayes(tfcounter, phraselist_up, phraselist_down):
    upscore = calcCondiProbCgivenX(tfcounter, phraselist_up, lmttyp='up')
    downsocre = calcCondiProbCgivenX(tfcounter, phraselist_down, lmttyp='down')
    if upscore > downsocre:
        print('Classified as UP: \nScore UP:{} > DOWN:{}'.format(upscore, downsocre))
    else:
        print('Classified as DOWN: \nScore UP:{} <= DOWN:{}'.format(upscore, downsocre))
if __name__ == '__main__':
    lmttyp = 'down'
    tgtidx = 5

    phraselist_up, phraselist_down = phrase.generateUPDOWNlist()
    tfdoc_counterlist = doc_utils.JSON2COUNTERLIST('up') if lmttyp == 'up' else doc_utils.JSON2COUNTERLIST('down')
    doc_list = doc_utils.getListFromCSV('up') if lmttyp == 'up' else doc_utils.getListFromCSV('down')

    sample_content = doc_list[tgtidx]
    sample_tfcounter = tfdoc_counterlist[tgtidx]
    print(sample_content)
    print(sample_tfcounter)

    print('Down P(C|X)', calcCondiProbCgivenX(sample_tfcounter, phraselist_down, lmttyp='down'))
    print('UP P(C|X)', calcCondiProbCgivenX(sample_tfcounter, phraselist_up, lmttyp='up'))

    classifyByBayes(sample_tfcounter, *phrase.generateUPDOWNlist())
