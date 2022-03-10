from phrase import N_ttl, N_up, N_down
import math

def tfidf(tf_ctr, df_ctr):
    # return a sorted LIST
    # tf-idf = (1+log(tf)) * log(N_ttl/df)
    ret_dict = {}
    for idx, elm in enumerate(tf_ctr.most_common()):
        ret_dict[elm[0]] = (1 + math.log(elm[1])) * math.log(N_ttl / df_ctr[elm[0]])

    return sorted(ret_dict.items(), key=lambda x: x[1], reverse=True)


def MI_tfidf(lmttyp, tf_ctr, df_ctr, df_all_ctr):
    # tf-idf = (1+log(tf)) * log(N_ttl/df)
    # MI = log(N(XY) / N(X)N(Y)), belongs to df
    N_tmp = N_up if lmttyp == 'up' else N_down
    ret_dict = {}
    for idx, elm in enumerate(tf_ctr.most_common()):
        # elm[0]: feature, elm[1]: count
        MI = math.log(df_ctr[elm[0]] / (N_tmp * df_all_ctr[elm[0]]))
        tid = (1 + math.log(elm[1])) * math.log(N_tmp / df_ctr[elm[0]])
        ret_dict[elm[0]] = MI * tid

    return sorted(ret_dict.items(), key=lambda x: x[1], reverse=True)


def associations(lmttyp, df_ctr, df_all_ctr):
    # Support P(XY) = N(XY)/N_ttl
    # Confidence(X->Y) P(Y|X) = P(XY)/P(X) = N(XY)/N(X)
    # Lift P(XY)/(P(X)P(Y)) = N_ttl*N(XY)/(N(X)N(Y))
    # Feature (X) -> up or down (Y)
    N_tmp = N_up if lmttyp == 'up' else N_down

    sup_dict = {}
    cfd_dict = {}
    lft_dict = {}
    for idx, elm in enumerate(df_ctr.most_common()):
        # elm[0]: feature, elm[1]: counts
        sup_dict[elm[0]] = df_ctr[elm[0]] / N_ttl
        cfd_dict[elm[0]] = df_ctr[elm[0]] / df_all_ctr[elm[0]]
        lft_dict[elm[0]] = (N_ttl * df_ctr[elm[0]]) / (df_all_ctr[elm[0]] * N_tmp)
    ret_sup_lst = sorted(sup_dict.items(), key=lambda x: x[1], reverse=True)
    ret_cfd_lst = sorted(cfd_dict.items(), key=lambda x: x[1], reverse=True)
    ret_lft_lst = sorted(lft_dict.items(), key=lambda x: x[1], reverse=True)
    return ret_sup_lst, ret_cfd_lst, ret_lft_lst