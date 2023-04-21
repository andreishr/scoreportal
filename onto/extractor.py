import os
from music21 import *
from dotenv import load_dotenv
from termcolor import colored, cprint
# Load environment variable
load_dotenv()
dir_path = os.getenv('SONG_PATH')
# Loop through each file in the directory [:1] only for testing things
for file_name in os.listdir(dir_path)[:1]:
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
        cprint('The score contains the following data:', 'green', attrs=["bold"])
        meta = score.metadata.all()
        for keyy, value in meta:
            print(colored(keyy, 'cyan', attrs=["bold"]), ":", value)


        '''
        Get all parts in the score
            use score.parts
            Another way:
            recurse() - iterating over the elements of a music score
            getElementsByClass('Instruments') - get all instruments/parts
            
        '''
        Parts = score.parts
        cprint('\n The score includes the following parts:', 'blue', attrs=["bold"])
        part_list = [f"{onePart}" for onePart in Parts]
        # PRint the list of instruments(parts)
        print(f"{part_list}\n")


        '''
        Get details for all parts:
            quarterLength - gets the part length in quarter length units
            getTimeSignatures()[0] - used to get the time signature of the part
            getInstruments()[0] - used to get the instrument of the part
            getElementsByClass('Measure')[0].getElementsByClass('Clef')[0] - used to het the clef of the part
        '''
        cprint('\n Details of each score part:', 'green', attrs=["bold"])
        for i, thisPart in enumerate(part_list):
            cprint(f'\n{thisPart} has the following details:', 'blue', attrs=['bold'])
            part = score.parts[i]
            partLength = part.quarterLength
            partSignature = part.getTimeSignatures()[0]
            partInstrument = part.getInstruments()[0]
            partClef = part.getElementsByClass('Measure')[0].getElementsByClass('Clef')[0]
            stringClef = str(partClef).split(".")[-1]
            stringTimeSign = str(partSignature).split(".")[-1]
            print(f"Has length: {partLength} quarter-length units")
            print(f"Has clef: {stringClef[:-1]}")
            print(f"Has time signature: {stringTimeSign[:-1]}")
            print(f"Has instrument: {partInstrument}")
        print('\n')


        '''
        Get all notes for an instrument(part)
            for each instrument get that specific part
            stripTies() is used to get the notes correctly
            get all the notes with recurse()
            for each note, any note attribute can be saved

        In addition: Build a dictionary containing parts and keys
        '''
        part_notes = {}
        for i, thisPart in enumerate(part_list):
            cprint(f"Notes for {thisPart} are:", 'yellow', attrs=['bold'])
            part = score.parts[i]
            part = part.stripTies()
            notes = part.recurse().notes
            note_list = []
            for thisNote in notes[:10]:
                note_list.append(thisNote)
                print(colored(f"Note pitch: {thisNote.pitch}", attrs=['bold']), colored(f"Note offset: {thisNote.offset}", attrs=['bold']))
            print('\n')
            part_notes[thisPart] = note_list
        # Print Dictionary:
        cprint('\n Dictionary with each part and notes:', 'blue', attrs=["bold"])
        print(f"{part_notes}\n")


        '''
        Get intervals on each part:
            interval.Interval() returns the interval between consecutive notes
        '''
        part_intervals = {}
        for part_note in part_notes:
            intervals = []
            stringPart = str(part_note).split(".")[-1]
            cprint(f"Intervals for {stringPart[:-1]} are:", 'yellow', attrs=['bold'])
            for i in range(len(part_notes[part_note])-1):
                oneinterval = interval.Interval(part_notes[part_note][i], part_notes[part_note][i+1])
                intervals.append(oneinterval)
            for thisInterval in intervals:
                print(colored(f"Interval name: {thisInterval.directedNiceName}", attrs=['bold']))
            print('\n')
            part_intervals[part_note] = intervals
        # Print Dictionary:
        cprint('\n Dictionary with each interval for a part:', 'blue', attrs=["bold"])
        print(part_intervals)


        '''
        Get chords for a specific part
            *schord represents the original score chordified at the beginning with .cordify() method
            Chords are extracted for each measure of the score; we get measure with getElementsByClass('Measures')
        .notes used for measure object gives the elements in the measures that contain notes (ex. chords)
        .elements used for measure object returns all elements in the specific measure
        For each measure we use .notes to get all the chords, and then we use .commonName and .pitches attributes
        in order to extract the name and pitch objects.
        '''
        cprint('\n Chordified score has following chords at each measure:', 'green', attrs=["bold"])
        schord.stripTies()
        measures = schord.getElementsByClass('Measure')
        chord_dict = {}
        for measure in measures[:10]:
            chord_list = []
            print(colored('At measure number: ', attrs=['bold']) + str(measure.number))
            for oneChord in measure.notes:
                chord_list.append(oneChord.commonName)
                chord_list.append(oneChord.pitches)
                print(colored('Chord: ', attrs=['bold']) + colored(oneChord.commonName, 'light_cyan') + 
                      colored(' having the notes: ', attrs=['bold']) + str([onePitch.name for onePitch in oneChord.pitches]))
            chord_dict[measure] = [(chord_list[i], chord_list[i+1]) for i in range(0, len(chord_list), 2)]
            print('\n')
        cprint('Dictionary with chords:', 'blue', attrs=["bold"])
        print(chord_dict)
    print('\n')


    
    


