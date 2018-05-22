# -*- coding: utf-8 -*-
'''
读取XML的最基本单元是 ReadValue()， 它把指定tag中间的text提取出来。

但用 ElementTree.iter（）直接读value会丢失原有的数据结构（ET这个library把XML提取成了一棵树）
所以需要以一定的层次性逐渐深入到底层value。

同时需要考虑某些信息的序列顺序（例如某个音符先于其他音符出现）。
只有顺序无关的数据才用dictionary存储，其他都用list。


>>> INPUT : XML_FilePath
>>> OUTPUT : stuctured_score (type:list)
'''

import xml.etree.ElementTree as ET

'''
in ET, We use "element.iter(tag=tagName)" to read the sub-element
Since XML is a nested structure, we need to call .iter() recursively
'''
def ReadValue(element,tagName):
    value = []
    for subelem in element.iter(tag=tagName):
        value.append(subelem.text)
    #assert(len(value)==1)  # this function is built for reading only 1 value ,
                           # if not 1, there must be some logical error
    #print(value)
    if (len(value)==1):
        return value[0]
    else:
        return ''

#  (Read Atrribute) & (Read Note) is for reading Attr & Note in measures
def ReadAtrribute(attr):  
    info = {}

    cnt = 0
    for division in attr.iter(tag='divisions'):
        assert(cnt==0)
        info['divisions'] = ReadValue(attr,'divisions')
        cnt += 1

    cnt = 0
    for key in attr.iter(tag='key'):
        assert(cnt==0)
        info['key-fifths'] = ReadValue(key,'fifths')
        info['key-mode'] = ReadValue(key,'mode')
        cnt += 1

    cnt = 0
    for time in attr.iter(tag='time'):
        assert(cnt==0)
        info['time-beats'] = ReadValue(time,'beats')
        info['time-beat-type'] = ReadValue(time,'beat-type')
        cnt += 1

    cnt = 0
    for clef in attr.iter(tag='clef'):
        assert(cnt==0)
        info['clef-sign'] = ReadValue(clef,'sign')
        info['clef-line'] = ReadValue(clef,'line')
        cnt += 1

    #print(info)
    return info

#  (Read Atrribute) & (Read Note) is for reading Attr & Note in measures
def ReadNote(note):
    NoteDic = {}

    cnt = 0
    for pitch in note.iter(tag='pitch'):
        assert(cnt==0)
        NoteDic['pitch-step'] = ReadValue(pitch,'step')
        NoteDic['pitch-octave'] = ReadValue(pitch,'octave')
        NoteDic['pitch-alter'] = ReadValue(pitch,'alter')
        cnt += 1
    NoteDic['duration'] = ReadValue(note,'duration')
    NoteDic['type'] = ReadValue(note,'type')
    NoteDic['stem'] = ReadValue(note,'stem')

    #print(NoteDic)
    return NoteDic

# Read Measure calls (Read Atrribute) & (Read Note) 
def ReadMeasure(measure):
    measure_num = int(measure.attrib['number'])
    info_list = []
    note_list = []
    for attr in measure.iter(tag='attributes'):
        info = ReadAtrribute(attr)
        info_list.append(info)
    for note in measure.iter(tag='note'):
        noteValue = ReadNote(note)
        note_list.append(noteValue)

    return measure_num,info_list,note_list

def ReadScore(root):
    part_list = []
    for part_child in root.iter(tag='part'):
        measure_list = []
        for measure_child in part_child.iter(tag='measure'):
            num,info,notes = ReadMeasure(measure_child)
            measure_list.append((num,info,notes))
        part_list.append(measure_list)
    return part_list

'''
这是真正被外部用到的函数：ReadXML
input：FilePath
output：score （list）

它将XML装入内存解析为一棵ElementTree。
然后将root传给子函数去解析。
'''
def ReadXML(FilePath):
    print('Start Read File :'+FilePath)
    tree = ET.ElementTree(file=FilePath)
    root = tree.getroot()
    score = ReadScore(root)
    return score
'''
score这个list里, 每个元素是一个part（一般的乐谱只有1个part）
每个part（list）内有多个measure（list），也就是乐谱上的一个小节。
measure[0]、measure[1]、measure[2]分别对应：小节#编号、当前小节的info、小节内的音符
!!! -->通常，第一小节的info信息是重要的，它会有'key-mode'、'time-beats'、'time-beat-type'等信息
    -->其后的小节，这些信息如果没有变化，就不再重复给出。
type(info) = dict
type(note) = dict, 但我们把同一小节里的 notes 存在一个 list 里，以确保它们依然有序。
'''

if __name__ == '__main__':
    #pass
    FileName = 'test2.xml'
    score = ReadXML(FileName)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    for part in score:
        for measure in part:
            print(measure[0])
            print(measure[1])
            print(measure[2])
            print('----------------------')
