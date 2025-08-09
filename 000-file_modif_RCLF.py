import os, glob, sys
import string

'''
delete RCLF
'''

fiName= '001.txt'

fi= open(fiName,'r')
lines= fi.readlines()
fi.close()

fo= open('002.txt','w')

if 1:
  for line in lines:
    #if(len(line)<2): fo.write('\n')
    line= line.strip()
    if(len(line)==0): continue
    if 0:
      if(line[0] in string.ascii_uppercase):
        fo.write('\n')
    fo.write(line)
    if 0: fo.write(' ')
    if 1: fo.write('\n')
    #else:
  fo.write('\n')
      
  fo.close()

  sys.exit()

for line in lines:
  #if(len(line)<2): fo.write('\n')
  line= line.strip()
  if '\\' in line:
    continue
  if(len(line)>4):
    if(line[0] in string.ascii_uppercase):
      fo.write('\n')
    if(line[0] in '123456789*"'):
      fo.write('\n')
    if line[0] =='"':
      fo.write('\n')
    if line[0] =='-':
      fo.write('\n')
    fo.write(line)
    #if(line[-1] =='.'):
    #  fo.write('\n')
    #else:
    fo.write(' ')
    #if(line[0]=='!'): fo.write('\n')
    
fo.close()

sys.exit()

for line in lines:
  #if(len(line)<2): fo.write('\n')
  line= line.strip()
  if(len(line)>0):
    fo.write(line)
    fo.write('\n')
    
fo.close()

sys.exit()


