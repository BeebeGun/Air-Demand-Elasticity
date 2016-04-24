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
