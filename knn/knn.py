import get_vectors
from sklearn.metrics.pairwise import cosine_similarity
from operator import itemgetter

def knn(k, vectors, matrix, docs):
    big_arr = []
    ind_count = 0
    for each in matrix:
        arr = []
        for i in xrange(0, k):
            arr.append((each[i], i))
        arr.sort(key=itemgetter(0), reverse = True)
        for i in xrange(k, len(each)):
            if each[i] > arr[-1][0]:
                arr.pop()
                arr.append((each[i], i))
                arr.sort(key=itemgetter(0), reverse = True)
        count_ham = 0
        count_spam = 0
        for each in arr:
            if each[1] < docs.hams_train:
                count_ham += 1
            else:
                count_spam += 1
        if count_spam > count_ham:
            classify = 1
        else:
            classify = 0
        if ind_count < docs.hams_test:
            setter = 0
        else:
            setter = 1
        big_arr.append((classify, setter))
        ind_count += 1

    return big_arr

def accuracy(arr):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for each in arr:
        if each[0] == 1:
            if each[1] == 1:
                tp += 1
            else:
                fp += 1
        elif each[0] == 0:
            if each[1] == 1:
                fn += 1
            else:
                tn += 1
    print "Precision is ", float(tp) / float(tp + fp)
    print "Recall is ", float(tp) / float(tp + fn)
    print "Accuracy is ", float(tp + tn) / float(tp + tn + fp + fn)

def main():
    docs = get_vectors.document('data/train/ham', 'data/train/spam')
    docs.set_test_vectors('data/test/ham', 'data/test/spam')
    vectors = docs.get_vectors()
    similarity_matrix = cosine_similarity(vectors[0:docs.len_test], vectors[docs.len_test:])
    print "======================================"
    print "At K = 3"
    arr = knn(3, vectors, similarity_matrix, docs)
    accuracy(arr)
    print "======================================"
    print "\n======================================"
    print "At K = 4"
    arr = knn(4, vectors, similarity_matrix, docs)
    accuracy(arr)
    print "======================================"
    print "\n======================================"
    print "At K = 5"
    arr = knn(5, vectors, similarity_matrix, docs)
    accuracy(arr)
    print "======================================"

main()    
