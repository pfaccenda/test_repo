import json, os, sys, pprint

fname_in = "keys.json"
fname_out = "tags.json"
infile = open( fname_in,  'r')
outfile=open( fname_out, 'w')


with open("keys.json") as json_file:
    json_data = json.load(json_file)


s=[]
d={}
for k,v in json_data.iteritems():
   print k,"=",v
   d["Key"]=k
   d["Value"]=v
   s.append( d )

s2=json.dumps(s, sort_keys=True, indent=4)
print s2

outfile.writelines(s2)
outfile.close()

