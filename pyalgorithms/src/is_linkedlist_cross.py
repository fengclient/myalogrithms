#coding=utf-8
'''
Created on 2012-3-4
validate if two linked lists are cross with each other.

@author: fengclient
'''
import random
random.seed()

class linknode():
    '''
    node composing a linked list
    '''
    def __init__(self, data, nextnode = None):
        self.data = data
        self.next = nextnode

def build_linked_list(length = 100):
    '''
    build a linked list with random value
    '''
    if length <= 0:
        return None
    return linknode(random.randint(1, 100), build_linked_list(length - 1))

def make_sure_length(linkedlist):
    count = 0
    while linkedlist:
        print linkedlist.data,
        count = count + 1
        linkedlist = linkedlist.next
    print ''
    return count

def end_of(linkedlist):
    while linkedlist.next:
        linkedlist = linkedlist.next
    return linkedlist

def has_cycle(linkedlist):
    return False if are_we_cross_cycle(linkedlist, linkedlist) else True

def are_we_cross_cycle(list1, list2):
    cursor1 = list1
    cursor2 = list2
    while cursor1 and cursor2.next and cursor1 != cursor2:
        cursor1 = cursor1.next
        cursor2 = cursor2.next.next
    if cursor1 == cursor2 and cursor1:
        return cursor1.data

def are_we_cross_ultimate(a, b):
    cycle_a = has_cycle(a)
    cycle_b = has_cycle(b)
    
    if cycle_a and cycle_b:
        cross = are_we_cross_cycle(a, b)
    elif cycle_a == cycle_b == False and end_of(a) == end_of(b):
        cross = end_of(a).data
    return (cycle_a, cycle_b, cross)

if __name__ == '__main__':
    print 'build linked list a , b , c'
    a = build_linked_list(12)
    print 'a ='
    make_sure_length(a)
    b = build_linked_list(14)
    print 'b ='
    make_sure_length(b)
    c = build_linked_list(5)
    print 'c =', make_sure_length(c)
    print 'a + c, b + c'
    end_of(a).next = c
    end_of(b).next = c
    print 'new a ='
    make_sure_length(a)
    print 'new b ='
    make_sure_length(b)
    (cycle_a, cycle_b, evidencenode) = are_we_cross_ultimate(a, b)
    print 'is a cycle:', cycle_a
    print 'is b cycle:', cycle_b
    print 'are we cross with each other(and where)?', evidencenode
