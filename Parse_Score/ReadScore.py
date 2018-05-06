# -*- coding: utf-8 -*-
'''
读取XML的最基本单元是 ReadValue()， 它把指定tag中间的text提取出来。

但用 ElementTree.iter（）直接读value会丢失原有的数据结构（ET这个library把XML提取成了一棵树）
所以需要以一定的层次性逐渐深入到底层value。

同时需要考虑某些信息的序列顺序（例如某个音符先于其他音符出现）。
只有顺序无关的数据才用dictionary存储，其他都用list。


INPUT : XML_FilePath
OUTPUT : stuctured_score (type:list)
'''

import xml.etree.ElementTree as ET

def ReadValue(element,tagName):
    value = []
    for subelem in element.iter(tag=tagName):
        value.append(subelem.text)
    #assert(len(value)==1)  # this function is built for reading only 1 value ,
                           # if not 1, there must be some logical error
    #print(value)
    if (len(value)==1):
        #print(type(value[0]))
        return value[0]
    else:
        return ''


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


def ReadXML(FilePath):
    print('Start Read File :'+FilePath)
    tree = ET.ElementTree(file=FilePath)
    root = tree.getroot()
    score = ReadScore(root)
    return score



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
