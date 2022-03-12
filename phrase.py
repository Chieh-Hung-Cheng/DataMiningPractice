import math
import doc_utils

N_up = 612  # 613-1
N_down = 126  # 127-1
N_ttl = 738  # 613+127-1-1


class Phrase:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.tf_all = self.tf_up + self.tf_down
        self.df_all = self.df_up + self.df_down
        for elm in ['up', 'down']:
            self.calc_MI(elm)
            self.calc_tfidf(elm)
            self.calc_assocs(elm)
            self.calc_chisq(elm)

    def __gt__(self, other):
        if self.conf_up > other.conf_up:
            return True
        elif self.conf_up == other.conf_up:
            if self.supp_up > other.supp_up:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        frqstr = 'Phrase:{}\nUP: tf={}, df={} / {}\nDN: tf={}, df={} / {}\nALL: tf={}, df={} / {}\n' \
            .format(self.name, self.tf_up, self.df_up, N_up, self.tf_down, self.df_down, N_down, self.tf_all, self.df_all, N_ttl)
        ascstr = 'UP: MI={:.3f}, tfidf={:.3f}, support={:.3f}, confidence={:.3f}, lift={:.3f}, CHISQ={:.3f}\nDN: MI={:.3f}, tfidf={:.3f}, support={:.3f}, confidence={:.3f}, lift={:.3f}, CHISQ={:.3f}' \
            .format(self.MI_up, self.tfidf_up, self.supp_up, self.conf_up, self.lift_up, self.chisq_up,
                    self.MI_down, self.tfidf_down, self.supp_down, self.conf_down, self.lift_down, self.chisq_down)

        return frqstr + ascstr + '\n -------------------------------------------------------------------------------------------'

    def calc_MI(self, lmttyp):
        # MI = log(N(XY) / (N(X)N(Y)), belongs to df
        if lmttyp == 'up':
            self.MI_up = math.log((self.df_up + 1e-4) / (N_up * self.df_all))
        elif lmttyp == 'down':
            self.MI_down = math.log((self.df_down + 1e-4) / (N_down * self.df_all))

    def calc_tfidf(self, lmttyp):
        # tf-idf = (1+log(tf)) * log(N_ttl/df) ???
        N_tmp = N_up if lmttyp == 'up' else N_down
        if lmttyp == 'up':
            self.tfidf_up = (1 + math.log(self.tf_up + 1e-4)) * math.log(N_ttl / self.df_all)
        elif lmttyp == 'down':
            self.tfidf_down = (1 + math.log(self.tf_down + 1e-4)) * math.log(N_ttl / self.df_all)

    def calc_assocs(self, lmttyp):
        # Support P(XY) = N(XY)/N_ttl
        # Confidence(X->Y) P(Y|X) = P(XY)/P(X) = N(XY)/N(X)
        # Lift P(XY)/(P(X)P(Y)) = N_ttl*N(XY)/(N(X)N(Y))
        # Feature (X) -> up or down (Y)
        if lmttyp == 'up':
            self.supp_up = self.df_up / N_ttl
            self.conf_up = self.df_up / self.df_all
            self.lift_up = (N_ttl * self.df_up) / (self.df_all * N_up)
        elif lmttyp == 'down':
            self.supp_down = self.df_down / N_ttl
            self.conf_down = self.df_down / self.df_all
            self.lift_down = (N_ttl * self.df_down) / (self.df_all * N_down)

    def calc_chisq(self, lmttyp):
        if lmttyp == 'up':
            expected = self.df_all * N_up / N_ttl
            self.chisq_up = (1 if self.df_up > expected else -1)*(self.df_up - expected)**2 / expected
        elif lmttyp == 'down':
            expected = self.df_all * N_down / N_ttl
            self.chisq_down = (1 if self.df_down > expected else -1) * (self.df_down - expected)**2 / expected



def generatePhraseList(save=True):
    tf_up = doc_utils.JSON2COUNTER('up', 'tf')
    df_up = doc_utils.JSON2COUNTER('up', 'df')
    tf_down = doc_utils.JSON2COUNTER('down', 'tf')
    df_down = doc_utils.JSON2COUNTER('down', 'df')
    tf_all = doc_utils.JSON2COUNTER('all', 'tf')
    df_all = doc_utils.JSON2COUNTER('all', 'df')

    ret_lst = []
    for key, val in df_all.most_common():
        phrase = Phrase(name=key,
                        tf_up=tf_up[key] if key in tf_up else 0,
                        df_up=df_up[key] if key in df_up else 0,
                        tf_down=tf_down[key] if key in tf_down else 0,
                        df_down=df_down[key] if key in df_down else 0
                        )
        ret_lst.append(phrase)
    if save: doc_utils.PhraseList2JSON(ret_lst)
    return ret_lst

def showPhraseList(lst):
    for idx, elm in enumerate(lst):
        print('{} {}'.format(idx, elm))

def showNameList(*args):
    for phraselist in args:
        cnt = 0
        for elm in phraselist:
            print('{}'.format(elm.name), end=' ')
            if cnt == 9:
                cnt = 0
                print('')
            else:
                cnt += 1
        print('Num: {}\n'.format(len(phraselist)))

def filter(phraselist, **kwargs):
    ret_phlst = phraselist.copy()
    for key, val in kwargs.items():
        ret_phlst = [i for i in ret_phlst if i.__dict__[key] > val]
    return ret_phlst

def generateUPDOWNlist(lmt100=True, show_detail=False, show_name=False):
    phraselist = doc_utils.JSON2PhraseList()
    phraselist.sort(key=lambda x: x.lift_up, reverse=True)
    uplist = filter(phraselist, supp_up=0.105)

    phraselist.sort(key=lambda x: x.chisq_down, reverse=True)
    downlist = filter(phraselist, supp_down=0.015, conf_down=0.2, lift_down=1)

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

if __name__ == '__main__':
    generate = False
    if(generate): phraselist = generatePhraseList()
    else: phraselist = doc_utils.JSON2PhraseList()
    showPhraseList(phraselist[0:10])
