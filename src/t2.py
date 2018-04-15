#! /usr/bin/python 

message = "HelloPython v003"


f = open("testfile", 'w')

d = { u"name01": u"value01", u"name02" : u"value02"}
c = "***"
sout = ""
for k,v in d.items():
    #  print(k,v)
    formatted = "{:4} {:8} {:8}\r\n".format(c, k, v)
    print formatted
    f.write( formatted )

f.close()


