from ab_compare import AbCompare

#tokenization, stopping, stemming


def calc_features_all(query_list, text):#will return a feature vector

    v = AbCompare()
    num_queries = len(query_list)
    relations = list()

    avg_relation = 0
    relation_sum = 0

    for query in query_list:#this will make relations a list with len = num_queries
        curr_relation = v.relation(v.concordance(query.lower()), v.concordance(text.lower()))
        relations.append(curr_relation)

    return relations#a list with n elements, where n= number of

def calc_features_form(query_list, text, avg = True, sum = False):#will return a scalar, and text should be preprocessed

    v = AbCompare()
    num_queries = len(query_list)
    relations = list()

    avg_relation = 0
    relation_sum = 0

    for query in query_list:#this will make relations a list with len = num_queries
        curr_relation = v.relation(v.concordance(query.lower()), v.concordance(text.lower()))
        relations.append(curr_relation)

    if avg == True:
        res = sum(relations)/len(relations)
    if sum == True:
        res = sum(relations)
    return res
