import pybrain as py
import numpy as np
import pickle
from sklearn.externals import joblib
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.validation import CrossValidator


def readdata():

    #import crude oil prices
    crude = [0.0] * 12

    oil_data = open('data/DCOILWTICO.csv','r')
    #skip headers
    oil_data.readline()
    for line in oil_data.readlines():
        data = [x for x in line.strip().split(',') if x != '']
        if (int(data[1]) == 2015):
            crude[int(data[0])-1] = float(data[2])

    print(crude)

    #number of inputs, number of outputs
    ds = SupervisedDataSet(5,1)

    tf = open('data/2015.csv','r')

    # skip headers
    tf.readline()

    for line in tf.readlines():
        data = [x for x in line.strip().split(',') if x != '']
        if float(data[1]) != 0:
            indata =  (float(data[3]), float(data[4]), float(data[6]), float(data[7]), crude[int(data[7])-1])
            outdata = (float(data[2])/float(data[1]))
            ds.addSample(indata,outdata)

    return ds

def buildnetwork(ds):

    # number of inputs, hidden neurons, number of outputs
    n = buildNetwork(ds.indim, 100, ds.outdim, recurrent=False)
    print("Building Trainer...")
    t = BackpropTrainer(n,learningrate=0.01,momentum=0.5,verbose=True)

    # print("Cross Validator Initiating...")
    # cv=CrossValidator(trainer=t, dataset=ds, n_folds=5)
    # print("Cross Validating...")
    # CrossValidator.validate(cv)

    return n

    # t.trainOnDataset(ds,1000)
    # t.testOnData(verbose=True)

def serialize(net):
    s = joblib.dump(net, 'serializednetwork/nn.pkl')
    return s

def predict(serial, data):
    net = joblib.load('serializednetwork/nn.pkl')
    return net.activate(data)

if __name__ == '__main__':
    print("Reading data...")
    data = readdata()
    print("Building network...")
    network = buildnetwork(data)
    print("Serializing network...")
    nn = serialize(network)
    print("Predicting...")
    print(predict(nn, [94,12266,12339,634,2015]))