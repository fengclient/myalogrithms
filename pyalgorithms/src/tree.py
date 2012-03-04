'''
Created on 2012-3-3
Implement the following C# function to output all the values of the binary 
tree nodes at the specified depth from the root. Root has depth 0. Start 
from the leftmost node. An iterative solution is preferred over a recursive one.
[traversal, iterate, look through, traverse]

@author: fengclient
'''

class treenode(object):
    '''
    classdocs
    '''

    def __init__(self, data):
        '''
        Constructor
        '''
        self.data = data
        self.subnodes = []

def traverse(node, func):
    '''
    traverse the tree
    '''
    if len(node.subnodes) == 0:
        func(node.data)
    else:
        for i in node.subnodes:
            traverse(i, func)
