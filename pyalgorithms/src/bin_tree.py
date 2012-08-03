'''
Created on 2012-8-3

@author: fengclient
'''
import random
import time
random.seed(time.ctime())

class treenode(object):
    '''
    classdocs
    '''

    def __init__(self, data):
        '''
        Constructor
        '''
        self.data = data
        self.left_node = None
        self.right_node = None

def traverse(node, func):
    '''
    traverse the tree
    '''
    if node == None:
        return
    func(node.data)
    traverse(node.left_node, func)
    traverse(node.right_node, func)

def do_something(data):
    print data

def build_tree(depth):
    if depth < 1:
        return None
    root = treenode(random.randint(1, 100))
    root.left_node = build_tree(depth - 1)
    root.right_node = build_tree(depth - 1)
    return root
    
if __name__ == '__main__':
    root = build_tree(10)
    traverse(root, do_something)
