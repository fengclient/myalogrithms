'''
Created on 2012-3-3

@author: xiaoftang
'''
import copy
from collections import deque

class state(object):
    '''
    classdocs
    '''
    instancecounter=0
    
    def __init__(self):
        '''
        Constructor
        '''
        self.a_points=[]
        self.b_points=[]
        self.points=deque(range(1,30))
        self.whosnext='a'
        self.instanceid=state.instancecounter+1
        state.instancecounter=state.instancecounter+1
    
    def clone(self):
        a=copy.deepcopy(self)
        a.instanceid=state.instancecounter+1
        state.instancecounter=state.instancecounter+1
        return a
    
    def shake(self,count):
        if count==0 or len(self.points)==0:
            return
        if self.whosnext=='a':
            self.a_points.append(self.points.popleft())
            print '[%s] a is counting at %s %s'%(self.instanceid,self.a_points[-1],self.a_points)
            #raw_input("Press Enter to continue...")
        else:
            self.b_points.append(self.points.popleft())
            print '[%s] b is counting at %s %s'%(self.instanceid,self.b_points[-1],self.b_points)
            #raw_input("Press Enter to continue...")
        
        self.shake(count-1)
    
    def switch(self):
        self.whosnext='b' if self.whosnext=='a' else 'a'