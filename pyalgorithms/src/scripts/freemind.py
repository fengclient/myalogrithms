#coding=utf-8
'''
Created on 2012-3-19

@author: fengclient
'''
from lxml import etree as ET
import xlwt
from argparse import ArgumentParser

class FreeMindMap(object):
    '''
    classdocs
    '''
    
    def __init__(self, file_name_or_filelike_obj):
        '''
        Constructor
        '''
        f = file_name_or_filelike_obj
        we_own_it = not hasattr(f, 'read')
        if we_own_it:
            f = open(file_name_or_filelike_obj, 'r')
        self.xml = ET.fromstring(f.read())
        f.close()
    
    def get_origin_lines(self):
        '''
        traverse and build output
        '''
        context = ET.iterwalk(self.xml, events = ('start', 'end'), tag = '*')
        stack = []
        lines = []
        for (action, element) in context:
            if element.tag == 'node':
                if action == 'start':
                    stack.append(element)
                else: #action=='end'
                    stack.pop()
            elif element.tag == 'attribute':
                if action == 'start':# or action = 'end'
                    lines.append((tuple([e.attrib['TEXT'] for e in stack]), element.attrib['NAME'], element.attrib['VALUE']))
            else:
                pass
        return lines
    
    def get_workbook_lines(self, lines):
        '''
        (目录) Name Value
        title = [u'层级', u'目录 ', u'是否目录', u'用例名称', u'用例描述', u'前提条件', u'步骤', u'期待结果', u'用例类型']
        '''
        workbooklines = []
        existing_dirs = []
        for line in lines:
            case_dir = line[0]
            #create lines for directory of this case if it doesn't exist
            for i in range(1, len(case_dir)):
                dir_id = '-'.join(case_dir[:i + 1])
                if dir_id not in existing_dirs:
                    workbooklines.append((i, case_dir[i - 1], 1, case_dir[i], '', '', '', '', '0'))
                    existing_dirs.append(dir_id)
            #case description = case name
            workbooklines.append((len(case_dir), case_dir[-1], 0, line[1], line[1], '', '', line[2], '0'))
        return workbooklines
    
    def save_excel(self, output):
        origin_lines = self.get_origin_lines()
        wbk = xlwt.Workbook()
        sheet2 = wbk.add_sheet('FreeMind', cell_overwrite_ok = True)
        title = [u'层级', u'目录 ', u'是否目录', u'用例名称', u'用例描述', u'前提条件', u'步骤', u'期待结果', u'用例类型']
        #title = [e.encode(encoding = 'UTF-8', errors = 'strict') for e in title]
        lines = [tuple(title)]
        lines.extend(self.get_workbook_lines(origin_lines))
        for l in range(len(lines)):
            line = lines[l]
            for k in range(len(line)):
                sheet2.write(l, k, line[k])
        wbk.save(output)

if __name__ == '__main__':
    parser = ArgumentParser(description = 'convert freemind map(*.mm) to excel file(*.xls)')
    parser.add_argument('input', nargs = 1, metavar = '<freemind map *.mm>')
    parser.add_argument('output', nargs = 1, metavar = '<excel file *.xls>')
    ns = parser.parse_args()
    a = FreeMindMap(ns.input[0])
    a.save_excel(ns.output[0])
    print 'excel is writen as', ns.output[0]
