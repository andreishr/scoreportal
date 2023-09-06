import os
from music21 import *
from dotenv import load_dotenv
from termcolor import colored, cprint
import json
from encoder import *

def save_dictionary_to_txt(dictionary, file_path):
    # with open(file_path, 'w') as file:
    #     for key, value in dictionary.items():
    #         file.write(f"{key}: {value}\n")
    with open(file_path, 'w') as file:
        json.dump(dictionary, file, cls=MusicElementEncoder)

# Load environment variable
load_dotenv()
dir_path = os.getenv('SONG_PATH')
dict_path = os.getenv('DICT_PATH')
# Declare dictionaries to be used for classes:
songCount = 0
# Loop through each file in the directory [:1] only for testing things
for file_name in os.listdir(dir_path):
    cprint(f'\n SONG: {file_name}', 'cyan', attrs=["bold"])
    song_dict = {}
    songAttr_dict = {}
    parts_dict = {}
    measures_dict = {}
    if file_name.endswith('.mxl'):
        # Parse the mxl file
        filepath = os.path.join(dir_path, file_name)
        score = converter.parse(filepath)
        schord = score.chordify()

        '''
        Get all metadata available in the mxl file
            metadata.all() returns object containing all metadata
            Get key-value pairs from metadata inside loop
        '''
        # cprint('The score contains the following data:', 'green', attrs=["bold"])
        meta = score.metadata
        meta_all = score.metadata.all()

        key_list = [elem[0] for elem in meta_all]
        if 'composer' in key_list:
            composer = meta.composer
        else:
            composer = 'Unknown'
        if 'title' in key_list:
            title = meta.title
        else:
            title = meta.movementName.split('.')[0]
        
        songAttr_dict['songDescription'] = [title, composer]
        # print(colored(f'Title: {title}', 'cyan', attrs=["bold"]))
        # print(colored(f'Composer: {composer}', 'cyan', attrs=["bold"]))

        '''
        Get all parts in the score
            use score.parts
            Another way:
            recurse() - iterating over the elements of a music score
            getElementsByClass('Instruments') - get all instruments/parts
            
        '''
        Parts = score.parts
        # cprint('\n The score includes the following parts:', 'blue', attrs=["bold"])
        part_list = [f"{onePart}" for onePart in Parts]
        # Print the list of instruments(parts)
        # print(f"{part_list}\n")


        '''
        Get details for all parts:
            quarterLength - gets the part length in quarter length units
            getTimeSignatures()[0] - used to get the time signature of the part
            getInstruments()[0] - used to get the instrument of the part
            getElementsByClass('Measure')[0].getElementsByClass('Clef')[0] - used to het the clef of the part
        '''
        '''
        Get all notes for an instrument(part)
            for each instrument get that specific part
            stripTies() is used to get the notes correctly
            get all the notes with recurse()
            for each note, any note attribute can be saved
        '''
        '''
        Get intervals on each part:
            interval.Interval() returns the interval between consecutive notes
        '''
        # cprint('\n Details of each score part:', 'green', attrs=["bold"])
        for i, thisPart in enumerate(part_list):
            # cprint(f'\n{thisPart} has the following details:', 'blue', attrs=['bold'])
            part = score.parts[i]
            partLength = part.quarterLength
            partSignature = part.getTimeSignatures()[0]
            partInstrument = str(part.getInstruments()[0]).split(':')[-1]
            partClef = part.getElementsByClass('Measure')[0].getElementsByClass('Clef')[0]
            stringClef = str(partClef).split(".")[-1]
            stringTimeSign = str(partSignature).split(".")[-1]
            if part.getElementsByClass('Measure')[0].getElementsByClass(key.Key): 
                scale_name = part.getElementsByClass('Measure')[0].getElementsByClass(key.Key)[0] 
            else:
                scale_name = "Undefined"         
            part = part.stripTies()
            notes = part.recurse().notes
            note_list = []
            for thisNote in notes:
                if thisNote.isChord:
                    for oneNote in thisNote.notes:
                        note_list.append(oneNote)
                else:    
                    note_list.append(thisNote)  
            interval_list = []
            j = 0
            for i in range(len(note_list)-1):
                oneinterval = interval.Interval(note_list[i], note_list[i+1])
                if oneinterval.isConsonant():
                    interval_list.append([oneinterval, "Consonant"])
                else:
                    interval_list.append([oneinterval, "Dissonant"])
            # for thisInterval in interval_list:
            #     print(colored(f"Interval name: {thisInterval[0].directedNiceName} between {thisInterval[1]} and {thisInterval[2]}", attrs=['bold']))
            parts_dict[str(thisPart).split('.')[2][:-1]] = [str(scale_name), partLength, stringClef[:-1], stringTimeSign[:-1], partInstrument, note_list, interval_list]
            # print("Part scale: " + str(scale_name))
            # print(f"Has length: {partLength} quarter-length units")
            # print(f"Has clef: {stringClef[:-1]}")
            # print(f"Has time signature: {stringTimeSign[:-1]}")
            # print(f"Has instrument: {partInstrument}")
        print('\n')
        songAttr_dict['Parts'] = parts_dict
        

        '''
        Get chords for a specific part
            *schord represents the original score chordified at the beginning with .cordify() method
            Chords are extracted for each measure of the score; we get measure with getElementsByClass('Measures')
        .notes used for measure object gives the elements in the measures that contain notes (ex. chords)
        .elements used for measure object returns all elements in the specific measure
        For each measure we use .notes to get all the chords, and then we use .commonName and .pitches attributes
        in order to extract the name and pitch objects.
        '''
    #     cprint('\n Chordified score has following chords at each measure:', 'green', attrs=["bold"])
        measures = schord.getElementsByClass('Measure')
        for measure in measures:
            chord_nr = 0
            chord_dict = {} 
            # print(colored('Measure number: ', 'blue', attrs = ["bold"]) + str(measure.measureNumber) + colored(' Measure duration: ', 'blue', attrs=["bold"]) + str(measure.barDuration))
            # cprint('Has chords:', 'green', attrs=['bold'])
            for elem in measure.secondsMap:
                note_list = []
                thisChord = elem['element']
                chordName = None
                chordStart = None
                chordDuration = None
                chordEnd = None
                if isinstance(thisChord, chord.Chord):
                    chordName = thisChord.commonName
                    chordStart = elem['offsetSeconds']
                    chordDuration = elem['durationSeconds']
                    chordEnd = elem['endTimeSeconds']
                    chordNotes = thisChord.notes
                    chordPitches = thisChord.pitches
                    # cprint(f'Name: {chordName}, Duration (in seconds): {chordDuration}, with notes:', attrs=['bold'])
                    # print(chordNotes)
                    # cprint(f'And pitches:', attrs=['bold'])
                    # print(chordPitches)
                    chord_dict[chord_nr] = [chordName, chordDuration, chordNotes]
                    chord_nr += 1
            measures_dict["M"+str(measure.measureNumber)]=[measure.measureNumber, measure.barDuration, chord_dict]
        songAttr_dict['Measures'] = measures_dict
        song_dict[str(file_name).split('.')[0]] = songAttr_dict
        # print(song_dict)
        new_file_name = file_name.replace(" ", "_").replace("\\", "_").replace('\n', '').replace("?", "_").replace("'", "_").replace("(", "").replace("(", "").replace("/", "")
        save_path = str(dict_path+ '/' + new_file_name)
        save_dictionary_to_txt(song_dict, f'{save_path}.json')
        print(f'Song number: {songCount}')
        print(file_name + 'was saved in JSON format.')
        songCount += 1
    #         chord_list = []
    #         print(colored('At measure number: ', attrs=['bold']) + str(measure.number))
    #         for oneChord in measure.notes:
    #             chord_list.append(oneChord.commonName)
    #             chord_list.append(oneChord.pitches)
    #             print(colored('Chord: ', attrs=['bold']) + colored(oneChord.commonName, 'light_cyan') + 
    #                   colored(' having the notes: ', attrs=['bold']) + str([onePitch for onePitch in oneChord.pitches]))
    #         chord_dict[measure] = [(chord_list[i], chord_list[i+1]) for i in range(0, len(chord_list), 2)]
    #         print('\n')
    #     cprint('Dictionary with chords:', 'blue', attrs=["bold"])
    #     print(chord_dict)
    # print('\n')


    
    


