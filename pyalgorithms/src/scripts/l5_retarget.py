'''

retarget all routes to a new ip
'''
import os
import sys

#172.23.1.154 to 10.185.3.11
print 'argv:',sys.argv
sourceip=sys.argv[1]
targetip=sys.argv[2]
print 'sourceip:',sourceip
print 'targetip:',targetip
os.system('cat ../conf/routetb_info.route|grep %s >todo'%sourceip)
f=open('todo')
regcommand='./route_regist %s %s %s %s';
delcommand='./route_delnode %s %s %s %s';
for line in f:
  pieces_old=line.split(' ')
  pieces_new=line.split(' ')
  if pieces_new[2]==sourceip:
    pieces_new[2]=targetip
  regcmd=regcommand % tuple(pieces_new)
  delcmd=delcommand % tuple(pieces_old)
  print 'regcmd:',regcmd
  print 'delcmd:',delcmd
  os.system(regcmd)
  os.system(delcmd)
