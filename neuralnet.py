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
    crude = [[0.0 for x in range(13)] for y in range(6)]

    oil_data = open('data/DCOILWTICO.csv','r')

    # print(crude)
    #skip headers
    oil_data.readline()
    for line in oil_data.readlines():
        data = [x for x in line.strip().split(',') if x != '']
        if (int(data[1]) <= 2015 and int(data[1]) >= 2010):
            crude[int(data[1])-2010][0] = int(data[1])
            crude[int(data[1])-2010][int(data[0])] = float(data[2])

    print(len(crude[0]))

    #number of inputs, number of outputs
    ds = SupervisedDataSet(6,1)

    # start year loop here
    # for i in range(0,6):

        # filename = 'data/201' + str(i) + '.csv'

    filename = 'data/masterdata.csv'

    tf = open(filename,'r')

    # skip headers
    tf.readline()

    for line in tf.readlines():
        data = [x for x in line.strip().split(',') if x != '']
        if float(data[1]) >= 40:
            # distance, origin, destination, year, month, fuel price
            indata =  [float(data[3])/6089, float(data[4])/16647, float(data[5])/16647, float(data[7])/2015, float(data[8])/12, crude[int(data[7])-2010][int(data[8])]/109.53]
            outdata = [float(data[2])/float(data[1])]
            ds.addSample(indata,outdata)

    # end year loop here

    return ds

def buildnetwork(ds):

    # number of inputs, hidden neurons, number of outputs
    tstdata, trndata = ds.splitWithProportion( 0.25 )
    n = buildNetwork(ds.indim, 100, ds.outdim, recurrent=False)
    n.randomize()
    print("Building Trainer...")
    # t = BackpropTrainer(n,learningrate=0.01,momentum=0.01,verbose=True)
    # t.trainOnDataset(tstdata, 3)

    t = BackpropTrainer(n, ds)
    for epoch in range(0, 1000):                                                                   
        error = t.train()
        if error < 0.001:
            break  

    # print("Cross Validator Initiating...")
    # cv=CrossValidator(trainer=t, dataset=ds, n_folds=10)
    # print("Cross Validating...")
    # CrossValidator.validate(cv)

    return n

    # t.trainOnDataset(ds,1000)
    # t.testOnData(verbose=True)

def serialize(net):
    s = joblib.dump(net, 'serializednetwork/nn.pkl')
    return s

def predict(data):
    print("Predicting")
    net = joblib.load('serializednetwork/nn.pkl')
    return net.activate(data)

#if __name__ == '__main__':
def nnetBegin():
    #global nn
    # print("Reading data...")
    # data = readdata()
    # print("Building network...")
    # network = buildnetwork(data)
    # print("Serializing network...")
    # nn = serialize(network)
    net = net = joblib.load('serializednetwork/nn.pkl')
    #print("Predicting...")
    #print(predict(nn, [94,12266,12339,634,2015]))