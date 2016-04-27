tf = open('data/origindestpairs.csv','r')

ports = {}
dists = {}

# skip headers
tf.readline()

for line in tf.readlines():
    data = [x for x in line.strip().split(',') if x != '']
    keys = ports.keys()
    if data[0] not in keys:
        vals = [data[1]]
        dist = [data[2]]
        ports[data[0]] = vals
        dists[data[0]] = dist
    else:
        port = ports.get(data[0])
        dist = dists.get(data[0])
        if data[1] not in port:
            port.append(data[1])
            dist.append(data[2])
            ports[data[0]] = port
            dists[data[0]] = dist

newfile = open('data/cleanedorgdest.csv', 'w')

for org in ports.keys():
    for i in range(len(ports.get(org))):
        newfile.write(org + ',' + ports.get(org)[i] + ',' + dists.get(org)[i] + '\n')


fa = open('finalairports.csv','r')
alldata = open('visualization/mapFiles/cleanedorgdest.csv', 'r')
newall = open('visualization/mapFiles/newcleanedorgdest.csv', 'w')

farr = []

for line in fa.readlines():
    data = [x for x in line.strip().split(',') if x != '']
    farr.append(data[0])

for line in alldata.readlines():
    data = [x for x in line.strip().split(',') if x != '']
    if data[0] in farr and data[1] in farr:
        newall.write(str(data[0]) + ',' + str(data[1]) + ',' + str(data[2]) + '\n')

fa.close()
alldata.close()
newall.close()

# clean all of the other data

# map IATA code to airport id

mapping = {}
ids = open('data/airportids.csv')

ids.readline()

for line in ids.readlines():
    data = [x for x in line.strip().split(',') if x != '']
    mapping[data[0]] = data[1]


newmapping = {}


for key in mapping.keys():
    if key in farr:
        newmapping[key] = mapping[key]

print(newmapping.values())

# start year loop here

masterdata = open('data/masterdata.csv', 'w')

for i in range(0,6):

    filename = 'data/201' + str(i) + '.csv'

    tf = open(filename,'r')

    # skip headers
    tf.readline()

    for line in tf.readlines():
        data = [x for x in line.strip().split(',') if x != '']
        if float(data[1]) >= 40:
            orgid = None
            destid = None
            if data[4] in newmapping.values():
                orgid = data[4]
            if data[5] in newmapping.values():
                destid = data[5]
            if orgid is not None and destid is not None:
                masterdata.write(str(data[0]) + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(data[3]) + ',' + str(data[4]) + ',' + str(data[5]) + 
                    ',' + str(data[6]) + ',' + str(data[7]) + ',' + str(data[8]) + '\n')
