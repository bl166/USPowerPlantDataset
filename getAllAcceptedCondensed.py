'''
getAllAcceptedCondensed.py

This script walks through Turk folders, finds all condensed accepted annotations,
and merge them into one single file named "accepted_ann_json.txt". If the file already 
exists, the old file will be renamed first, with time added to it to avoid conficts.

Author: Boning Li
Email: boning.li@duke.edu
Developed for Duke Data+ 2017: Electricity Access
Jul 31, 2017
'''

import os
import json
import datetime

# The folder where all returned annotations are checked
#folder = '/home/hyperion/dataplus/dataplus/TurkMulti/folders/' # obsolete
folder = '/home/hyperion/dataplus/dataplus/Turkv3/MTurkAnnotationTool/HITBatches/'

# Names of all immediate subfolders where all accepted.txt and its condensed form are generated
paths = next(os.walk(folder))[1]

# Iterate and read all condensedfromaccepted.txt
f_name = 'condensed_accepted.txt'
#f_name = 'condensedfromaccepted.txt' # obsolete
out_name = 'accepted_ann_json.txt'
json_base = []
for path in paths:
    f_path = os.path.join(folder,path,f_name)
    if not os.path.isfile(f_path):
        continue
    with open(f_path,'r') as f:
    	json_temp = []
    	while 1:
    		try:
    			json_text = f.readline()
    			json_temp.append(json.loads(json_text))
    		except:
    			break        
    json_base = json_base+json_temp
    print('Done '+path)
    print('Current annotation count: %d'%(len(json_base)))

# Save to file
if os.path.isfile(out_name):
    dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    os.rename(out_name,out_name[:-4]+'_'+dt+'.txt')
with open(out_name, 'a') as output:
	for base in json_base:
		json.dump(base,output)
		output.write('\n')
    
    
