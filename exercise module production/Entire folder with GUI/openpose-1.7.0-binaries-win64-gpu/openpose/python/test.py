import glob
import os

files = glob.glob('../../movenet/live_json/*')
path = os.path.join("../../movenet/live_json", "1")
#print(files)
for f in files:
    print(f)



#os.mkdir(path)