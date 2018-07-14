# -*- coding: utf-8 -*-
from Parse_Score.ReadScore import ReadXML


NOTE_LIST = [
    'A2', 'A3', 'A4', 'A5',
    'B2', 'B3', 'B4', 'B5',
    'C2', 'C3', 'C4', 'C5',
    'D2', 'D3', 'D4', 'D5',
    'E2', 'E3', 'E4', 'E5',
    'F2', 'F3', 'F4', 'F5',
    'G2', 'G3', 'G4', 'G5'
]


def xml2notes(path):
    """
    用来从xml中获取音符
    :param path: xml文件地址
    :return: 一个1维list，list中的元素是一个音符(tuple)。音符[0]是一个字符串，A3这种，音符[1]是一个数字，记录duration
    """
    notes = []
    score = ReadXML(path)
    part = score[0]
    for measure in part:
        attrs_measure = measure[1] # 音节的各种属性
        notes_measure = measure[2] # 音节里所有的单音
        if len(notes_measure): # 音节不为空
            for note_dict in notes_measure: # 单音
                if 'pitch-step' in note_dict.keys(): # 含有音符信息
                    this_note = note_dict['pitch-step'] + note_dict['pitch-octave'] + note_dict['pitch-alter']
                    notes.append((this_note, int(note_dict['duration'])))
                else:
                    assert this_note
                    notes.append((this_note, int(note_dict['duration'])))
    return notes


def notes2classes(notes):
    """
    :param notes: xml2notes的输出
    :return: 一个 1d list，就是把A3这种音符换成了数字表示的标签
    """
    return list(map(note2class, notes))


def note2class(note):
    """
    :param note: 一个单音
    """
    global NOTE_LIST
    return NOTE_LIST.index(note[0]), note[1]

if __name__ == '__main__':
    f = 'Data/Piano/004.xml'
    print(notes2classes(xml2notes(f)))

