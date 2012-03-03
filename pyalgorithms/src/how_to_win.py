'''
Created on 2012-3-3

@author: xiaoftang
'''
import sys
import tree
import state

def shakeit(node):
    '''
    shake the tree identified by node. 
    '''
    data=node.data
    if len(data.points)>0:
        state1=data.clone()
        state1.shake(1)
        state1.switch()
        node1=tree.treenode(state1)
        state2=data.clone()
        state2.shake(2)
        state2.switch()
        node2=tree.treenode(state2)
        node.subnodes.append(node1)
        node.subnodes.append(node2)
    else:
        return
    
    for n in node.subnodes:
        shakeit(n)

if __name__ == '__main__':
    #state is a tuple with 3 elements: a_points,b_points,current_point,max_point,whosnext
    initstate=state.state()
    rootnode=tree.treenode(initstate)
    shakeit(rootnode)
    
def printtree(node):
    if len(node.data.subnodes)==0:
        print 'a_points:',node.data.a_points
        print 'b_points:',node.data.b_points
        winner='a' if node.a_points[-1]==30 else 'b'
        print 'winner is:',winner
    else:
        for i in node.subnodes:
            printtree(i)
        

