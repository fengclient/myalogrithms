#coding=utf-8
'''
Created on 2012-3-2

problem:
person A and person B are counting from 1 to 30.
each could count 1 or 2 steps per 1 round in turn.
the person who count on 30 win this game.

for this program, i just want to emunate all possibliy to see if
we have a pattern to win.

有这样一个数字游戏：
A,B两个人交叉连续数数，从1数到30，谁先数到30谁就赢了。
规则：每人一次只能数一个或两个连续的数字
比如：A每次可以数：1 或者 1,2 然后就轮到B数了，
      B只能接着数 3 或者 3,4 然后有轮到A数了......
就这样，A,B交叉连续数数，谁数到30数就赢。

请问，以什么规律赢得比赛呢？

答案: 谁先数到3的倍数, 就能数到30, 因为他总能补足

为什么会有如下结果?
total possibility: 144
total instances: 287

@author: fengclient
'''
import tree
import state

def shakeit(node):
    '''
    shake the tree identified by node. 
    '''
    data = node.data
    if len(data.points) > 0:
        state1 = data.clone()
        state1.shake(1)
        state1.switch()
        node1 = tree.treenode(state1)
        state2 = data.clone()
        state2.shake(2)
        state2.switch()
        node2 = tree.treenode(state2)
        node.subnodes.append(node1)
        node.subnodes.append(node2)
    else:
        return
    
    for n in node.subnodes:
        shakeit(n)

possibility = 0

def printdata(data):
    global possibility
    possibility = possibility + 1
    print 'a_points:', data.a_points
    print 'b_points:', data.b_points
    winner = 'a' if data.a_points[-1] == 10 else 'b'
    print 'winner is:', winner

if __name__ == '__main__':
    global possibility
    initstate = state.state()
    rootnode = tree.treenode(initstate)
    shakeit(rootnode)
    tree.traverse(rootnode, printdata)
    print 'total possibility:', possibility
    print 'total instances:', state.state.instancecounter
    

        

