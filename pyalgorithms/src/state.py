'''
Created on 2012-3-3

@author: xiaoftang
'''
import copy

class state(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.a_points=[]
        self.b_points=[]
        self.points=range(1,30)
        self.whosnext='a'
    
    def clone(self):
        a=copy.deepcopy(self)
        return a
    
    def shake(self,count):
        if count==0 or len(self.points)==0:
            return
        if self.whosnext=='a':
            self.a_points.append(self.points.pop())
        else:
            self.b_points.append(self.points.pop())
        
        self.shake(count-1)
    
    def switch(self):
        self.whosnext='b' if self.whosnext=='a' else 'a'