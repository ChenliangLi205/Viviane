import ReadScore

def ReadFirstNote(FileName):
    '''Read the first note, return a dict'''
    score = ReadScore.ReadXML(FileName)
    _,_,notes = score[0][0]
    print(notes[0])
    return notes[0]
# the returned notes(dict) is like this:
# {'pitch-step': 'B', 'pitch-octave': '4', 'pitch-alter': '', 'duration': '480', 'type': 'quarter', 'chord': False}


if __name__ == '__main__':
    #pass

    FileName = input("Enter your MusicXML File name (default 'test.xml')");
    if FileName:
        if FileName[-4:] != '.xml':
            FileName = FileName + '.xml'
    else:
        FileName = 'test.xml'
    note = ReadFirstNote(FileName)
    