from nltk import word_tokenize
import os
import sys
import math

ham_dict = {}
spam_dict = {}
tp = 0
fp = 0
tn = 0
fn = 0

def read_hams(path):
    files = os.walk(path).next()[2]
    for each in files:
        file_content = str.decode(open(os.path.join(path, each)).read(), "UTF-8", "ignore")
        try:
            tokens = word_tokenize(file_content)
            for every in tokens:
                if not ham_dict.has_key(every):
                    ham_dict[every] = 1
                else:
                    ham_dict[every] += 1
        except:
            print os.path.join(path, each), ' could not be decoded .. moving further'

def read_spams(path):
    files = os.walk(path).next()[2]
    for each in files:
        file_content = str.decode(open(os.path.join(path, each)).read(), "UTF-8", "ignore")
        try:
            tokens = word_tokenize(file_content)
            for every in tokens:
                if not spam_dict.has_key(every):
                    spam_dict[every] = 1
                else:
                    spam_dict[every] += 1
        except:
           print os.path.join(path, each), ' could not be decoded .. moving further'

def test_hams(path, cal):
    files = os.walk(path).next()[2]
    total_files = len(files)
    not_decoded = 0
    true = 0
    false = 0
    for each in files:
        file_content = str.decode(open(os.path.join(path, each)).read(), "UTF-8", "ignore")
        spammines = 0
        hammines = 0
        tokens = word_tokenize(file_content)
        for every in tokens:
            if spam_dict.has_key(every):
                c_spam = spam_dict[every]
            else:
                c_spam = 0
            if ham_dict.has_key(every):
                c_ham = ham_dict[every]
            else:
                c_ham = 0
            if (c_spam != 0) and (c_ham != 0):
                c_spammi = float(c_spam) / (float(c_spam) + float(c_ham))
                c_hammi = float(c_ham) / (float(c_spam) + float(c_ham))
                spammines += math.log(c_spammi)
                hammines += math.log(c_hammi)
        if spammines > hammines:
            false += 1
            cal['fp'] += 1
        else:
            true += 1
            cal['tn'] += 1
    #print "accuracy is ", float(true) / float(total_files)
                    
def test_spams(path, cal):
    files = os.walk(path).next()[2]
    total_files = len(files)
    not_decoded = 0
    true = 0
    false = 0
    for each in files:
        file_content = str.decode(open(os.path.join(path, each)).read(), "UTF-8", "ignore")
        spammines = 0
        hammines = 0
        tokens = word_tokenize(file_content)
        for every in tokens:
            if spam_dict.has_key(every):
                c_spam = spam_dict[every]
            else:
                c_spam = 0
            if ham_dict.has_key(every):
                c_ham = ham_dict[every]
            else:
                c_ham = 0
            if (c_spam != 0) and (c_ham != 0):
                c_spammi = float(c_spam) / (float(c_spam) + float(c_ham))
                c_hammi = float(c_ham) / (float(c_spam) + float(c_ham))
                spammines += math.log(c_spammi)
                hammines += math.log(c_hammi)
        if spammines < hammines:
            false += 1
            cal['fn'] += 1
        else:
            true += 1
            cal['tp'] += 1
    #print "accuracy is ", float(true) / float(total_files)

def accuracy(cal):
    tp = cal['tp']
    fp = cal['fp']
    tn = cal['tn']
    fn = cal['fn']
    print tp, fp, tn ,fn
    print "NAIVE BAYES WORKING OUT"
    print "======================================================="
    print "Precision is ", float(tp) / float(tp + fp)
    print "Recall is ", float(tp) / float(tp + fn)
    print "Accuracy is ", float(tp + tn) / float(tp + tn + fp + fn)
    print "======================================================="

def main():
    cal = {'tp':0, 'tn':0, 'fp':0, 'fn':0}
    read_hams('data/train/ham')
    read_spams('data/train/spam')
    test_hams('data/test/ham', cal)
    test_spams('data/test/spam', cal)
    accuracy(cal)

main()
