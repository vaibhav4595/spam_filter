from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import numpy, math

dataSet = SupervisedDataSet(20, 1)
testDataSet = SupervisedDataSet(20, 1)
print "CONSTRUCTING DATASET"
trainFile = open("train.csv")
testFile = open("test.csv")

for line in trainFile.readlines(): # Converting our csv into dataset
    data = [float(x) for x in line.strip().split(',') if x != '']
    indata =  tuple(data[:20])
    outdata = tuple(data[20:])
    dataSet.addSample(indata,outdata)

for line in testFile.readlines():
    data = [float(x) for x in line.strip().split(',') if x != '']
    indata =  tuple(data[:20])
    outdata = tuple(data[20:])
    testDataSet.addSample(indata,outdata)


print "NORMALIZING DATASET"
mx = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float64)
for inp, out in dataSet:
    for i in range(0, len(inp)):
        mx[i]+=inp[i]
for i in range(0, len(mx)):
    mx[i] = mx[i] / len(dataSet)
nfactor = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float64)
for i in range(0, len(dataSet)):
    for j in range(0, len(nfactor)):
        t = dataSet.getSample(i)[0][j]
        nfactor[j] += (t - mx[j]) * (t - mx[j])
for i in range(0, len(nfactor)):
    nfactor[i] = nfactor[i]/len(dataSet)
    nfactor[i] = math.sqrt(nfactor[i])
print nfactor
for inp, out in dataSet:
    for i in range(0, len(inp)):
        if(nfactor[i]!=0):
            inp[i] = (inp[i] - mx[i])/nfactor[i]
    #print inp

print "TRAINING OUR NEURAL NET"
neuralNet = buildNetwork(20, 6, 1)
trainer = BackpropTrainer(neuralNet, dataSet)
t=""
trainErr = trainer.train()
while float(trainErr) > 0.01:
    trainErr = trainer.train()
    print trainErr

print "TESTING OUR NEURAL NET"
neuralNet.sortModules()
p = neuralNet.activateOnDataset(testDataSet)
avg = 0
for i in p:
    avg += i[0]
avg = avg/len(p)
print avg
tp = 0
tn = 0
fp = 0
fn = 0
for i in range(0, len(p)):
    isSpam = testDataSet.getSample(i)[1][0]
    if p[i][0] < avg:
        if isSpam == 0.0:
            tn += 1
        else:
            fp += 1
    else:
        if isSpam == 1.0:
            tp += 1
        else:
            fn += 1

print tn+tn, fp+fn
print tp, tn, fp, fn
print "Precision = ", (float(tp)/(tp+fp))
print "Recall = ", (float(tp)/(tp+fn))
print "Accuracy = ", ((float(tp) + tn)/(tp+tn+fp+fn))
