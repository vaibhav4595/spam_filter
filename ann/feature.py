import os
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from itertools import groupby

def words(entry):
    return filter(lambda w: len(w) > 0,
                [w.strip("0123456789!:,.?(){}[]") for w in entry.split()])


def yuli(entry):
    d = {}
    stemmer = PorterStemmer()
    for w in words(entry):
        w = stemmer.stem(w).lower()
        try:
            d[w] += 1
        except KeyError:
            d[w] = 1
    M1 = float(len(d))
    M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(d.values()))])

    try:
        return (M1*M1)/(M2-M1)
    except ZeroDivisionError:
        return 0



def calc(tokens):
    total = 0
    short = 0
    longt = 0
    word_length = 0
    sentence = 0
    for each in tokens:
        if len(each) > 5:
            longt += 1
        else:
            short += 1
        total += 1
        word_length += len(each)
        if each == '.':
            sentence += 1

    return (total, short, longt, word_length, sentence)
    

def calc2(string):
    totalc = 0
    alphac = 0
    digic = 0
    white = 0
    upc = 0
    dic = {'*':0, ',':0, '_':0, '+':0, '=':0, '%':0, '$':0, '@':0, '/':0}

    for each in string:
        totalc += 1
        if each.isalpha():
            alphac += 1
        if each.isdigit():
            digic += 1
        if each.isupper():
            upc += 1
        if each == ' ':
            white += 1
        if each in ['*', ',', '_' ,'+', '=', '%', '$', '@', '/']:
            dic[each] += 1

    return (totalc, alphac , digic , white , upc ,  dic)
            

def main():
    fw = open('test.csv', 'a')
    path = 'data/test'
    for root, dirs, files in os.walk(path):
        if len(files) != 0:
            for each in files:
                if '/ham' in root:
                    belong = 0
                else:
                    belong = 1
                fp = open(os.path.join(root, each))
                string = str.decode(fp.read(), "UTF-8", "ignore")
                tokens = word_tokenize(string)
                yule_measure = yuli(string)
                tupp = calc2(string)
                tupp2 = calc(tokens)
                wrstring = ''
                wrstring = wrstring + str(yule_measure) + ','
                for cmon in tupp2:
                    wrstring = wrstring + str(cmon) + ','
                for j in xrange(0, 5):
                    wrstring = wrstring + str(tupp[j]) + ','
                for each in tupp[5]:
                    wrstring = wrstring + str(tupp[5][each]) + ','
                wrstring = wrstring + str(belong)
                fw.write(wrstring)
                fw.write('\n')
    fw.close()
main()
