import os
from music21 import *
from dotenv import load_dotenv
from termcolor import colored, cprint
# Load environment variable
load_dotenv()
dir_path = os.getenv('SONG_PATH')
# Loop through each file in the directory [:1] only for testing things
for file_name in os.listdir(dir_path)[:4]:
    if file_name.endswith('.mxl'):
        # Parse the mxl file
        filepath = os.path.join(dir_path, file_name)
        score = converter.parse(filepath)
        

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
            recurse() - iterating over the elements of a music score
            getElementsByClass('Instruments') - get all instruments/parts
            Another way is to use score.parts
        '''
        Instruments = score.recurse().getElementsByClass('Instrument')
        cprint('\n The score includes the following elements:', 'blue', attrs=["bold"])
        instrument_list = [f"{oneInstrument}" for oneInstrument in Instruments]
        # PRint the list of instruments(parts)
        print(f"{instrument_list}\n")


        '''
        Get clefs for all parts

        '''
        cprint('\n Clefs of each score part:', 'blue', attrs=["bold"])
        for i, thisInstrument in enumerate(instrument_list):
            part = score.parts[i]
            partSignature = part.getTimeSignatures()[0]
            partClef = part.getElementsByClass('Measure')[0].getElementsByClass('Clef')[0]
            stringClef = str(partClef).split(".")[-1]
            print(f"{thisInstrument} part has clef: {stringClef[:-1]}")
            print(f"{thisInstrument} part has timse signature: {partSignature}")
        print('\n')


        '''
        Get all notes for an instrument(part)
            for each instrument get that specific part
            stripTies() is used to get the notes correctly
            get all the notes with recurse()
            for each note, any note attribute can be saved

        In addition: Build a dictionary containing parts and keys
        '''
        instruments_notes = {}
        for i, thisInstrument in enumerate(instrument_list):
            cprint(f"Notes for {thisInstrument} are:", 'yellow', attrs=['bold'])
            part = score.parts[i]
            part = part.stripTies()
            notes = part.recurse().notes
            note_list = []
            for thisNote in notes[:10]:
                note_list.append(thisNote)
                print(colored(f"Note pitch: {thisNote.pitch}", attrs=['bold']), colored(f"Note offset: {thisNote.offset}", attrs=['bold']))
            print('\n')
            instruments_notes[thisInstrument] = note_list

        # Print Dictionary:
        cprint('\n Dictionary with each part and notes:', 'blue', attrs=["bold"])
        print(instruments_notes)


    print('\n')


    
    


