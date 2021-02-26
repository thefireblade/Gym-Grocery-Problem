from os import listdir
from os.path import isfile, join
mypath = "./graph_files/bench0_4/"
onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)