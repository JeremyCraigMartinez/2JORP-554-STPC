import string
class RouterInfo:
    def __init__(self, host, baseport):
        self.host, self.baseport = host, baseport;
    def __str__(self):
        return "{0} {1}".format(self.host, self.baseport)

class LinkInfo:
    def __init__(self, cost, locallink, remotelink):
        self.cost, self.locallink, self.remotelink = cost, locallink, remotelink;
    def __str__(self):
        return "{0} {1} {2}".format(self.cost, self.locallink, self.remotelink)
        
def readrouters(testname):
    f = open(testname+'/routers')
    lines = f.readlines()
    table = {}
    for line in lines:
        if line[0]=='#': continue
        words = string.split(line)
        table[words[0]] = RouterInfo(words[1], int(words[2]))
    f.close()
    return table

def readlinks(testname, router):
    f = open(testname+'/'+router+'.cfg')
    lines = f.readlines()
    table = {}
    for line in lines:
        if line[0]=='#': continue
        words = string.split(line)
        table[words[0]] = LinkInfo(int(words[1]), int(words[2]), int(words[3]))
    f.close()
    return table