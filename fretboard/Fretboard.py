notes_sharp = ['A', 'A#' , 'B', 'C' , 'C#', 'D', 'D#' , 'E' , 'F' , 'F#', 'G' , 'G#' ]
notes_flat  = ['A', 'Bb' , 'B', 'C' , 'Db', 'D' ,'Eb' , 'E' , 'F' , 'Gb', 'G' , 'Ab' ]
steps = ['1', 'b2' , '2' , 'b3' , '3' , '4' , 'b5' , '5' , 'b6', '6' , 'b7', '7' , '1', 'b9', '9', 'b10', '10','11', 'b12','12','b13','13','b14','14','b15','15']

notes_dots = ['     ', '       ', '     ' , '  O  ', '     ' , '  O  ', '     ' ,'  O  ' , '     ' ,'  O  ', '     ' , '     ' , ' OO  ']
notes = notes_flat

import time
import re
import random 
from random import randint

# Open the file for reading fretboard settings
with open('settings.txt', 'r') as infile:
    data = infile.read()  # Read the contents of the file into memory.

# Return a list of the lines, breaking at line boundaries.
settings = data.splitlines()
print "Settings:", settings

# Print each line of the file
#for line in settings:
#    print line

instrument = str(settings[0])    # eg. Guitar or Bass
string_no = str(settings[1])     # Number of strings the guitar or bass has eg. 4, 5, 6, 7
tuning = str(settings[2])        # eg. Standard or Drop D
root_note = str(settings[3])     # eg. A, G, F# etc
chord_name = str(settings[4])    # eg 7#9#5
string_scale = str(settings[5])  # eg Major, Mixolydian


#Make all print statemens also go to a file
import sys
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger("fretboard_log.txt")

chord_dict = {
'major':['maj','1','3','5'],
'minor':['min','1','b3','5'],
'power cord':['5','1','5'],
'augmented':['+','1','3','#5'],
'diminished':['o','1','b3','b5'],
'suspended 4th':['sus4','1','4','5'],
'suspended 2nd':['sus2','1','2','5'],
'major w/ added 9th':['add9','1','3','5','9'],
'minor w/ added 9th':['m(add9)','1','b3','5','9'],
'major w/ added 6th':['6','1','3','5','6'],
'minor w/ added 6th':['m6','1','b3','5','6'],
'major w/ added 6th & 9th':['6/9','1','3','5','6','9'],
'minor with w/ added 6th & 9th':['m6/9','1','b3','5','6','9'],
'major 7th':['maj7','1','3','5','7'],
'minor 7th':['m7','1','b3','5','b7'],
'dominant seventh':['7','1','3','5','b7'],
'minor 7th flat five':['m7b5','1','b3','b5','b7'],
'diminished 7th':['o7','1','b3','b5','bb7'],
'seventh suspended 4th':['7sus4','1','4','5','b7'],
'minor major 7th':['m(maj7)','1','b3','5','7'],
'major 9th':['maj9','1','3','5','7','9'],
'minor 9th':['m9','1','b3','5','b7','9'],
'dominant 9th':['9','1','3','5','b7','9'],
'ninth suspended 4th':['9sus4','1','4','5','b7','9'],
'minor 11th':['m11','1','b3','5','b7','9','11'],
'11th':['11','1','3','5','b7','9','11'],
'major 13th':['maj13','1','3','5','7','9','b13'],
'minor 13th':['m13','1','b3','5','b7','9','11','13'],
'13th':['13','1','3','5','b7','9','13'],
'major 7th flat five':['maj7b5','1','3','b5','7'],
'major 7th sharp eleven':['maj7#11','1','3','5','7','#11'],
'augmented 7th':['+7','1','3','#5','b7'],
'seventh flat five':['7b5','1','3','b5','b7'],
'seventh flat nine':['7b9','1','3','5','b7','b9'],
'seventh sharp nine':['7#9','1','3','5','b7','#9'],
'augmented 7th flat nine':['7b9#5','1','3','#5','b7','b9'],
'augmented 7th sharp nine':['7#9#5','1','3','#5','b7','#9'],
'13th flat nine':['13b9','1','3','5','b7','b9','13'],
'13th sharp nine':['13#9','1','3','5','b7','#9','13'],
'test':['test','1','b3','bb5','b7','#9','##13'],
'all':['all', '1', 'b2' , '2' , 'b3' , '3' , '4' , 'b5' , '5' , 'b6', '6' , 'b7', '7']
}

tuning_dict = {
'Guitar 7 Standard':['B','C','E','G','C','E','G'],
'Guitar 7 Big Guitar':['G','C','E','G','C','E','G'],
'Guitar 7 Brazilian':['C','E','A','D','G','B','E'],
'Guitar 7 1/3Rd Size':['F','Bb','D','F','Bb','D','F'],
'Guitar 7 Alt 1':['E','A','B','D','G','B','D'],
'Guitar 7 Alt 2':['E','G','B','D','G','B','D'],
'Guitar 7 Alt 3':['C','G','B','D','G','B','D'],
'Guitar 7 Alt 4':['D','G','C','D','G','A#','D'],
'Guitar 7 Alt 5':['B','F#','B','E','A','D','F#'],
'Guitar 7 Alt 6':['A','E','A','D','G','B','E'],
'Guitar 6 Standard':['E','A','D','G','B','E'],
'Guitar 6 Drop D':['D','A','D','G','B','E'],
'Guitar 6 Half Step Down':['D#','G#','C#','F#','A#','D#'],
'Guitar 6 Full Step Down':['D','G','C','F','A','D'],
'Guitar 6 1 and 1/2 Steps Down':['C#','F#','B','E','G#','C#'],
'Guitar 6 Double Drop D':['D','A','D','G','B','D'],
'Guitar 6 Drop C':['C','G','C','F','A','D'],
'Guitar 6 Drop C#':['C#','G#','C#','F#','A#','D#'],
'Guitar 6 Drop B':['B','F#','B','E','G#','C#'],
'Guitar 6 Drop A#':['A#','F','A#','D#','G','C'],
'Guitar 6 Drop A':['A','E','A','D','F#','B'],
'Guitar 6 Open D':['D','A','D','F#','A','D'],
'Guitar 6 Open D Minor':['D','A','D','F','A','D'],
'Guitar 6 Open G':['D','G','D','G','B','D'],
'Guitar 6 Open G Minor':['D','G','D','G','A#','D'],
'Guitar 6 Open C':['C','G','C','G','C','E'],
'Guitar 6 Open C#':['C#','F#','B','E','G#','C#'],
'Guitar 6 Open C Minor':['C','G','C','G','C','D#'],
'Guitar 6 Open E7':['E','G#','D','E','B','E'],
'Guitar 6 Open E Minor7':['E','B','D','G','B','E'],
'Guitar 6 Open G Major7':['D','G','D','F#','B','D'],
'Guitar 6 Open A Minor':['E','A','E','A','C','E'],
'Guitar 6 Open A Minor7':['E','A','E','G','C','E'],
'Guitar 6 Open E':['E','B','E','G#','B','E'],
'Guitar 6 Open A':['E','A','C#','E','A','E'],
'Guitar 6 C Tuning':['C','F','A#','D#','G','C'],
'Guitar 6 C# Tuning':['C#','F#','B','E','G#','C#'],
'Guitar 6 Bb Tuning':['A#','D#','G#','C#','F','A#'],
'Guitar 6 A to A (Baritone)':['A0','D','G','C','E','A'],
'Guitar 6 D A D D D D':['D','A','D','D','D','D'],
'Guitar 6 C G D G B D':['C','G','D','G','B','D'],
'Guitar 6 C G D G B E':['C','G','D','G','B','E'],
'Guitar 6 D A D E A D':['D','A','D','E','A','D'],
'Guitar 6 D G D G A D':['D','G','D','G','A','D'],
'Guitar 6 Open Dsus2':['D','A','D','G','A','D'],
'Guitar 6 Open Gsus2':['D','G','D','G','C','D'],
'Guitar 6 G6':['D','G','D','G','B','E'],
'Guitar 6 Modal G':['D','G','D','G','C','D'],
'Guitar 6 Overtone':['C','E','G','A#','C','D'],
'Guitar 6 Pentatonic':['A','C','D','E','G','A'],
'Guitar 6 Minor Third':['C','D#','F#','A','C','D#'],
'Guitar 6 Major Third':['C','E','G#','C','E','G#'],
'Guitar 6 All Fourths':['E','A','D','G','C','F'],
'Guitar 6 Augmented Fourths':['C','F#','C','F#','C','F#'],
'Guitar 6 Slow Motion':['D','G','D','F','C','D'],
'Guitar 6 Admiral':['C','G','D','G','B','C'],
'Guitar 6 Buzzard':['C','F','C','G','A#','F'],
'Guitar 6 Face':['C','G','D','G','A','D'],
'Guitar 6 Four and Twenty':['D','A','D','D','A','D'],
'Guitar 6 Ostrich':['D','D','D','D','D','D'],
'Guitar 6 Capo 200':['C','G','D','D#','D','D#'],
'Guitar 6 Balalaika':['E','A','D','E','E','A'],
'Guitar 6 Charango':['','G','C','E','A','E'],
'Guitar 6 Cittern One':['C','F','C','G','C','D'],
'Guitar 6 Cittern Two':['C','G','C','G','C','G'],
'Guitar 6 Dobro':['G','B','D','G','B','D'],
'Guitar 6 Lefty':['E','B','G','D','A','E'],
'Guitar 6 Mandoguitar':['C','G','D','A','E','B'],
'Guitar 6 Rusty Cage':['B','A','D','G','B','E'],
'Bass 4 Standard':['E','A','D','G'],
'Bass 4 Drop D':['D','A','D','G'],
'Bass 4 Semitone Flat':['D#','G#','C#','F#'],
'Bass 4 Drop D Semitone Flat':['C#','G#','C#','F#'],
'Bass 4 Low B':['B','E','A','D'],
'Bass 4 Open A':['E','A','E','A'],
'Bass 4 Open E':['E','B','E','G#'],
'Bass 4 Tenor Tuning':['A','D','G','C'],
'Bass 4 Piccolo Bass':['E','A','D','G'],
'Bass 4 Drop B':['B','A','D','G'],
'Bass 4 Old Skool Standard':['G','C','F','B'],
'Bass 5 Standard B':['B','E','A','D','G'],
'Bass 5 Standard C':['E','A','D','G','C'],
'Bass 5 Tenor Tuning':['A','D','G','C','F'],
'Bass 5 F# BEAD':['F#','B','E','A','D'],
'Bass 5 Drop D':['A','E','A','D','G'],
'Bass 6 Standard':['B','E','A','D','G','C'],
'Bass 6 E A D G C F':['E','A','D','G','C','F'],
'Bass 6 F# B E A D G':['F#','B','E','A','D','G']
}

ListScales = []
ListScales.append({"Scale":'Ahava Raba', "H_Steps":'R, H, 1.5, H, W, H, W, W', "L_Steps": ['1', 'b2', '3', '4', '5', 'b6', 'b7']}),
ListScales.append({"Scale":'Algerian',  "H_Steps":'R, W, H, W, H, H, H, 1.5, H', "L_Steps": ['1', '2', 'b3', '4', 'b5', 'bb6', 'bbb7']})
ListScales.append({"Scale":'Altered',  "H_Steps": 'R, H, W, H, W, W, W, W', "L_Steps": ['1', 'b2', 'b3', '3', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Arabian (a)',  "H_Steps": 'R, W, H, W, H, W, H, W, H', "L_Steps": ['1', '2', 'b3', '4', 'b5', 'b6', 'bb7']})
ListScales.append({"Scale":'Arabian (b)',  "H_Steps": 'R, W, W, H, H, W, W, W', "L_Steps": ['1', '2', '3', '4', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Augmented',  "H_Steps": 'R, 1.5, H, W, W, 1.5, H', "L_Steps": ['1', '#2', '3', '#4', '#5', '##6']})
ListScales.append({"Scale":'Auxiliary Diminished',  "H_Steps": 'R, W, H, W, H, W, H, W, H', "L_Steps": ['1', '2', 'b3', '4', 'b5', 'b6', 'bb7']})
ListScales.append({"Scale":'Auxiliary Diminished Blues',  "H_Steps": 'R, H, W, H, W, H, W, H, W', "L_Steps": ['1', 'b2', 'b3', '3', 'b5', 'bb6', 'bb7']})
ListScales.append({"Scale":'Balinese',  "H_Steps": 'R, H, W, 2, 1.5, W', "L_Steps": ['1', 'b2', 'b3', '##4', '###5']})
ListScales.append({"Scale":'Bebop Dominant',  "H_Steps": 'R, W, W, H, W, W, H, H, H', "L_Steps": ['1', '2', '3', '4', '5', '6', 'b7']})
ListScales.append({"Scale":'Bebop Half Diminished',  "H_Steps": 'R, H, W, W, H, H, H, 1.5, H', "L_Steps": ['1', 'b2', 'b3', '4', 'b5', 'bb6', 'bbb7']})
ListScales.append({"Scale":'Bebop Major',  "H_Steps": 'R, W, W, H, W, H, H, W, H', "L_Steps": ['1', '2', '3', '4', '5', 'b6', 'bb7']})
ListScales.append({"Scale":'Bebop Minor',  "H_Steps": 'R, W, H, H, H, W, W, H, W', "L_Steps": ['1', '2', 'b3', '3', 'bb5', 'bb6', 'bb7']})
ListScales.append({"Scale":'Blues',  "H_Steps": 'R, 1.5, W, H, H, 1.5, W', "L_Steps": ['1', '#2', '#3', '#4', '5', '#6']})
ListScales.append({"Scale":'Blues Variation 1',  "H_Steps": 'R, 1.5, W, H, H, 1.5, H, H', "L_Steps": ['1', '#2', '#3', '#4', '5', '#6', '7']})
ListScales.append({"Scale":'Blues Variation 2',  "H_Steps": 'R, 1.5, H, H, H, H, 1.5, H, H', "L_Steps": ['1', '#2', '3', '4', 'b5', 'bb6', 'b7']})
ListScales.append({"Scale":'Blues Variation 3',  "H_Steps": 'R, 1.5, H, H, H, H, W, H, HH', "L_Steps": ['1', '#2', '3', '4', 'b5', 'bb6', 'bb7']})
ListScales.append({"Scale":'Byzantine',  "H_Steps": 'R, H, 1.5, H, W, H, 1.5, H', "L_Steps": ['1', 'b2', '3', '4', '5', 'b6', '7']})
ListScales.append({"Scale":'Chinese',  "H_Steps": 'R, 2, W, H, 2, H', "L_Steps": ['1', '##2', '##3', '##4', '4x#']})
ListScales.append({"Scale":'Chinese 2',  "H_Steps": 'R, W, 1.5, W, W, 1.5', "L_Steps": ['1', '2', '#3', '##4', '##5']})
ListScales.append({"Scale":'Chinese Mongolian',  "H_Steps": 'R, W, W, 1.5, W, 1.5', "L_Steps": ['1', '2', '3', '##4', '##5']})
ListScales.append({"Scale":'Diatonic',  "H_Steps": 'R, W, W, 1.5, W, 1.5', "L_Steps": ['1', '2', '3', '##4', '##5']})
ListScales.append({"Scale":'Diminished',  "H_Steps": 'R, W, H, W, H, W, H, W, H', "L_Steps": ['1', '2', 'b3', '4', 'b5', 'b6', 'bb7']})
ListScales.append({"Scale":'Diminished, Half',  "H_Steps": 'R, H, W, H, W, H, H, W, W', "L_Steps": ['1', 'b2', 'b3', '3', 'b5', 'bb6', 'bbb7']})
ListScales.append({"Scale":'Diminished, Whole Tone',  "H_Steps": 'R, H, W, H, W, W, W, W', "L_Steps": ['1', 'b2', 'b3', '3', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Dominant 7th',  "H_Steps": 'R, W, W, H, W, W, H, W', "L_Steps": ['1', '2', '3', '4', '5', '6', 'b7']})
ListScales.append({"Scale":'Dominant Pentatonic',  "H_Steps": 'R, W, W, 1.5, 1.5, W', "L_Steps": ['1', '2', '3', '##4', '###5']})
ListScales.append({"Scale":'Dorian',  "H_Steps": 'R, W, H, W, W, W, H, W', "L_Steps": ['1', '2', 'b3', '4', '5', '6', 'b7']})
ListScales.append({"Scale":'Dorian #4',  "H_Steps": 'R, W, H, 1.5, H, W, H, W', "L_Steps": ['1', '2', 'b3', '#4', '5', '6', 'b7']})
ListScales.append({"Scale":'Double Harmonic',  "H_Steps": 'R, H, 1.5, H, W, H, 1.5, H', "L_Steps": ['1', 'b2', '3', '4', '5', 'b6', '7']})
ListScales.append({"Scale":'Egyptian',  "H_Steps": 'R, W, 1.5, W, W, 1.5', "L_Steps": ['1', '2', '#3', '##4', '##5']})
ListScales.append({"Scale":'Eight Tone Spanish',  "H_Steps": 'R, H, W, H, H, H, W, W, W', "L_Steps": ['1', 'b2', 'b3', '3', 'bb5', 'bbb6', 'bbb7']})
ListScales.append({"Scale":'Enigmatic',  "H_Steps": 'R, H, 1.5, W, W, W, H, H', "L_Steps": ['1', 'b2', '3', '#4', '#5', '#6', '7']})
ListScales.append({"Scale":'Ethiopian (A raray)',  "H_Steps": 'R, W, W, H, W, W, W, H', "L_Steps": ['1', '2', '3', '4', '5', '6', '7']})
ListScales.append({"Scale":'Ethiopian (Geez & Ezel)',  "H_Steps": 'R, W, H, W, W, H, W, W', "L_Steps": ['1', '2', 'b3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Half Diminished #2 (Locrian)',  "H_Steps": 'R, H, W, W, H, W, W, W', "L_Steps": ['1', 'b2', 'b3', '4', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Harmonic Minor',  "H_Steps": 'R, W, H, W, W, H, 1.5, H', "L_Steps": ['1', '2', 'b3', '4', '5', 'b6', '7']})
ListScales.append({"Scale":'Hawaiian',  "H_Steps": 'R, W, H, W, W, W, W, H', "L_Steps": ['1', '2', 'b3', '4', '5', '6', '7']})
ListScales.append({"Scale":'Hindu',  "H_Steps": 'R, W, W, H, W, H, W, W', "L_Steps": ['1', '2', '3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Hindustan',  "H_Steps": 'R, W, W, H, W, H, W, W', "L_Steps": ['1', '2', '3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Hirajoshi',  "H_Steps": 'R, W, H, 2, H, 2', "L_Steps": ['1', '2', 'b3', '##4', '#5']})
ListScales.append({"Scale":'Hirajoshi 2',  "H_Steps": 'R, 2, H, 2, W, H', "L_Steps": ['1', '##2', '#3', '4x#', '4x#']})
ListScales.append({"Scale":'Hungarian Gypsy Persian',  "H_Steps": 'R, H, 1.5, H, W, H, 1.5, H', "L_Steps": ['1', 'b2', '3', '4', '5', 'b6', '7']})
ListScales.append({"Scale":'Hungarian Major',  "H_Steps": 'R, 1.5, H, W, H, W, H, W', "L_Steps": ['1', '#2', '3', '#4', '5', '6', 'b7']})
ListScales.append({"Scale":'Ionian',  "H_Steps": 'R, W, W, H, W, W, W, H', "L_Steps": ['1', '2', '3', '4', '5', '6', '7']})
ListScales.append({"Scale":'Ionian #5',  "H_Steps": 'R, W, W, H, 1.5, H, W, H', "L_Steps": ['1', '2', '3', '4', '#5', '6', '7']})
ListScales.append({"Scale":'Iwato',  "H_Steps": 'R, H, 2, H, 2, W', "L_Steps": ['1', 'b2', '#3', '#4', '###5']})
ListScales.append({"Scale":'Japanese (A)',  "H_Steps": 'R, H, 2, W, H, 2', "L_Steps": ['1', 'b2', '#3', '##4', '#5']})
ListScales.append({"Scale":'Japanese (B)',  "H_Steps": 'R, W, 1.5, W, H, 2', "L_Steps": ['1', '2', '#3', '##4', '#5']})
ListScales.append({"Scale":'Japanese (Ichikosucho)',  "H_Steps": 'R, W, W, W, H, W, W, H', "L_Steps": ['1', '2', '3', '#4', '5', '6', '7']})
ListScales.append({"Scale":'Japanese (in sen)',  "H_Steps": 'R, H, 2, W, 1.5, W', "L_Steps": ['1', 'b2', '#3', '##4', '###5']})
ListScales.append({"Scale":'Japanese (Taishikicho)',  "H_Steps": 'R, W, W, H, H, H, W, H, HH', "L_Steps": ['1', '2', '3', '4', 'b5', 'bb6', 'bb7']})
ListScales.append({"Scale":'Jewish (Adonai Malakh)',  "H_Steps": 'R, H, H, H, W, W, W, H, W', "L_Steps": ['1', 'b2', 'bb3', 'b3', 'bb5', 'bb6', 'bb7']})
ListScales.append({"Scale":'Jewish (Magen Abot)',  "H_Steps": 'R, H, W, H, W, W, W, H, H', "L_Steps": ['1', 'b2', 'b3', '3', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Kumoi',  "H_Steps": 'R, W, H, 2, W, 1.5', "L_Steps": ['1', '2', 'b3', '##4', '##5']})
ListScales.append({"Scale":'Kumoi 2',  "H_Steps": 'R, H, 2, W, H, 2', "L_Steps": ['1', 'b2', '#3', '##4', '#5']})
ListScales.append({"Scale":'Leading Whole Tone',  "H_Steps": 'R, W, W, W, W, W, H, H', "L_Steps": ['1', '2', '3', '#4', '#5', '#6', '7']})
ListScales.append({"Scale":'Locrian',  "H_Steps": 'R, H, W, W, H, W, W, W', "L_Steps": ['1', 'b2', 'b3', '4', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Locrian 6',  "H_Steps": 'R, H, W, W, H, 1.5, W, H', "L_Steps": ['1', 'b2', 'b3', '4', 'b5', '6', '7']})
ListScales.append({"Scale":'Lydian',  "H_Steps": 'R, W, W, W, H, W, W, H', "L_Steps": ['1', '2', '3', '#4', '5', '6', '7']})
ListScales.append({"Scale":'Lydian #2',  "H_Steps": 'R, 1.5, H, W, H, W, W, H', "L_Steps": ['1', '#2', '3', '#4', '5', '6', '7']})
ListScales.append({"Scale":'Lydian Diminished',  "H_Steps": 'R, W, H, 1.5, H, W, W, H', "L_Steps": ['1', '2', 'b3', '#4', '5', '6', '7']})
ListScales.append({"Scale":'Lydian Minor',  "H_Steps": 'R, W, W, W, H, H, W, W', "L_Steps": ['1', '2', '3', '#4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Major',  "H_Steps": 'R, W, W, H, W, W, W, H', "L_Steps": ['1', '2', '3', '4', '5', '6', '7']})
ListScales.append({"Scale":'Major Blues',  "H_Steps": 'R, W, H, H, 1.5, W, 1.5', "L_Steps": ['1', '2', 'b3', '3', '5', '6']})
ListScales.append({"Scale":'Major Locrian',  "H_Steps": 'R, W, W, H, H, W, W, W', "L_Steps": ['1', '2', '3', '4', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Major Pentatonic',  "H_Steps": 'R, W, W, 1.5, W, 1.5', "L_Steps": ['1', '2', '3', '##4', '##5']})
ListScales.append({"Scale":'Melodic Minor',  "H_Steps": 'R, W, H, W, W, W, W, H', "L_Steps": ['1', '2', 'b3', '4', '5', '6', '7']})
ListScales.append({"Scale":'Minor Pentatonic',  "H_Steps": 'R, 1.5, W, W, 1.5, W', "L_Steps": ['1', '#2', '#3', '##4', '###5']})
ListScales.append({"Scale":'Mixo-Blues',  "H_Steps": 'R, 1.5, H, H, H, H, 1.5, W', "L_Steps": ['1', '#2', '3', '4', 'b5', 'bb6', 'b7']})
ListScales.append({"Scale":'Mixolydian',  "H_Steps": 'R, W, W, H, W, W, H, W', "L_Steps": ['1', '2', '3', '4', '5', '6', 'b7']})
ListScales.append({"Scale":'Mohammedan',  "H_Steps": 'R, W, H, W, W, H, 1.5, H', "L_Steps": ['1', '2', 'b3', '4', '5', 'b6', '7']})
ListScales.append({"Scale":'Moorish Phrygian',  "H_Steps": 'R, H, W, H, H, W, H, W, HH', "L_Steps": ['1', 'b2', 'b3', '3', 'bb5', 'bb6', 'bbb7']})
ListScales.append({"Scale":'Natural Minor',  "H_Steps": 'R, W, H, W, W, H, W, W', "L_Steps": ['1', '2', 'b3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Natural Pure Minor',  "H_Steps": 'R, W, H, W, W, H, W, W', "L_Steps": ['1', '2', 'b3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Neopolitan',  "H_Steps": 'R, H, W, W, W, H, 1.5, H', "L_Steps": ['1', 'b2', 'b3', '4', '5', 'b6', '7']})
ListScales.append({"Scale":'Neopolitan Major',  "H_Steps": 'R, H, W, W, W, W, W, H', "L_Steps": ['1', 'b2', 'b3', '4', '5', '6', '7']})
ListScales.append({"Scale":'Nine Tone',  "H_Steps": 'R, W, H, H, W, H, H, H, WH', "L_Steps": ['1', '2', 'b3', '3', 'b5', 'bb6', 'bbb7']})
ListScales.append({"Scale":'Oriental (a)',  "H_Steps": 'R, H, 1.5, H, H, W, W, W', "L_Steps": ['1', 'b2', '3', '4', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Overtone',  "H_Steps": 'R, W, W, W, H, W, H, W', "L_Steps": ['1', '2', '3', '#4', '5', '6', 'b7']})
ListScales.append({"Scale":'Overtone Dominant',  "H_Steps": 'R, W, W, W, H, W, H, W', "L_Steps": ['1', '2', '3', '#4', '5', '6', 'b7']})
ListScales.append({"Scale":'Pelog 2',  "H_Steps": 'R, H, W, 2, 1.5, W', "L_Steps": ['1', 'b2', 'b3', '##4', '###5']})
ListScales.append({"Scale":'Pelong',  "H_Steps": 'R, H, W, 2, H, 2', "L_Steps": ['1', 'b2', 'b3', '##4', '#5']})
ListScales.append({"Scale":'Pentatonic Blues',  "H_Steps": 'R, 1.5, W, H, H, 1.5, W', "L_Steps": ['1', '#2', '#3', '#4', '5', '#6']})
ListScales.append({"Scale":'Pentatonic Neutral',  "H_Steps": 'R, W, 1.5, W, 1.5, W', "L_Steps": ['1', '2', '#3', '##4', '###5']})
ListScales.append({"Scale":'Persian',  "H_Steps": 'R, H, 1.5, H, H, W, 1.5, H', "L_Steps": ['1', 'b2', '3', '4', 'b5', 'b6', '7']})
ListScales.append({"Scale":'Phrygian',  "H_Steps": 'R, H, W, W, W, H, W, W', "L_Steps": ['1', 'b2', 'b3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Phrygian Major',  "H_Steps": 'R, H, 1.5, H, W, H, W, W', "L_Steps": ['1', 'b2', '3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Prometheus',  "H_Steps": 'R, W, W, W, 1.5, H, W', "L_Steps": ['1', '2', '3', '#4', '##5', '#6']})
ListScales.append({"Scale":'Prometheus Neopolitan',  "H_Steps": 'R, H, 1.5, W, 1.5, H, W', "L_Steps": ['1', 'b2', '3', '#4', '##5', '#6']})
ListScales.append({"Scale":'Roumanian Minor',  "H_Steps": 'R, W, H, 1.5, H, W, H, W', "L_Steps": ['1', '2', 'b3', '#4', '5', '6', 'b7']})
ListScales.append({"Scale":'Six Tone Symmetrical',  "H_Steps": 'R, H, 1.5, H, 1.5, H, 1.5', "L_Steps": ['1', 'b2', '3', '4', '#5', '6']})
ListScales.append({"Scale":'Spanish Gypsy',  "H_Steps": 'R, H, 1.5, H, W, H, W, W', "L_Steps": ['1', 'b2', '3', '4', '5', 'b6', 'b7']})
ListScales.append({"Scale":'Super Locrian',  "H_Steps": 'R, H, W, H, W, W, W, W', "L_Steps": ['1', 'b2', 'b3', '3', 'b5', 'b6', 'b7']})
ListScales.append({"Scale":'Ultralocrian',  "H_Steps": 'R, H, W, H, W, W, H, 1.5', "L_Steps": ['1', 'b2', 'b3', '3', 'b5', 'b6', 'bb7']})
ListScales.append({"Scale":'All',  "H_Steps": 'R, H, H, H, H, H, H, H, H, H, H, H', "L_Steps": ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7']})
ListScales.append({"Scale":'Whole Tone',  "H_Steps": 'R, W, W, W, W, W, W', "L_Steps": ['1', '2', '3', '#4', '#5', '#6']})

ShortList_Scale = {
  'Major', 'Major Blues', 'Blues', 'Major Pentatonic', 'Pentatonic Blues', 'Melodic Minor', 'Natural Minor', 'Diminished', 'Mixolydian', 'Phrygian', 'Locrian', 'Spanish Gypsy'
}

def Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, valid_notes, bool_scale, bool_interval):
    #This function prints a character map of the fretboard
    
    #tuning_dict contains the dictionary for all the tunings
    #tuning contains the tuning for the instrument
    #valid_notes contains a list of notes that it will show
    #bool_interval is True or False and shows either notes or intervals
    
    #print "Tuning:", tuning_dict[tuning]
    #print "Valid notes:", valid_notes
    
    #if any of the open strings are sharp or flat
    bool_sharp_open = Bool_sharp_scale(tuning_dict[tuning])
    fret_sym = unichr(124)
    
    #bool_scale = False
    if bool_scale == True: #If you want a fretboard with scales
        #Find the Index of the chosen scale
        scale_interval = ""
        scale_steps = ""
        for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
            #print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
            if Scale["Scale"] == string_scale:  #if the scale matches a scale in ListScales
                scale_steps = Scale["H_Steps"]
                scale_interval = Scale["L_Steps"]
                break
    else: #If you want a fretboard with chords
        scale_interval = chord_dict[chord_name][1:]
    
    for open_string in reversed(range(len(tuning_dict[tuning]))):
        string_notes = ""
        O_string_note = tuning_dict[tuning][open_string]  #Open string of the instrument
        
        if len(O_string_note)>1:
            if O_string_note in notes_sharp: #If the open string note contains a sharp
                notes = notes_sharp
            if O_string_note in notes_flat: #If the open string note contains a flat
                notes = notes_flat
        else:
            notes = notes_flat
        
        for fret in range(13):
            #print open_string, fret, O_string_note
            step_from_note = (notes.index(O_string_note) + fret) % 12
            fret_note = notes[step_from_note]
            
            if fret_note in valid_notes:
                inte = valid_notes.index(fret_note)  #index of the fret_note relative to the root note
                if inte >= len(valid_notes):
                    print "STOP", fret_note, "inte", inte, "len", len(valid_notes), valid_notes
                else:
                    #print fret_note, inte, scale_interval[inte]
                    if bool_interval == True:
                        fret_note = scale_interval[inte]  #testing to replace the fret note name with the interval name instead
            
            if fret > 0:     #after the first fret
                #if len(fret_note)==1:   #if the note has only one character
                #    seg = "---"         #guitar segment for string
                #else:                   #if the note has a sharp or a flat (two characters)
                #    seg = "--"          #guitar segment for string

                seg = "-"*(4-len(fret_note))  #repeat the "-" chacter (4 times - the length of the fret note)
                
                if notes_sharp[step_from_note] in valid_notes or notes_flat[step_from_note] in valid_notes:
                    string_notes = string_notes + seg + fret_note + fret_sym
                else:
                    string_notes = string_notes + "----" + fret_sym 
            else:           #before the first fret
                if fret==0:
                    if bool_sharp_open: #if there any sharps in any of the the open tuning
                        if len(O_string_note)==2:
                            string_notes = string_notes + fret_note + fret_sym
                        else:
                            string_notes = " " + string_notes + fret_note + fret_sym
                    else:
                      seg = " "*(4-len(fret_note))
                      string_notes = seg + string_notes + fret_note + fret_sym
                      
        print string_notes
    
    #print dots and/or fret numbers below the fretboard
    dots = ""
    frets = ""
    logical_frets = False   #Either prints False = fret numbers or True = dots
    
    frets = " "*3
    dots = " "*3
    
    for fret in range(13):
        step_from_note = (fret) % 13
        dot = notes_dots[step_from_note]

        if fret <> 0:
          dots = dots + dot
          if fret < 10:
             frets = frets + "  " + str(fret) + "  "
          else:
             frets = frets + " " + str(fret) + "  "
        else:
          dots = dots
          frets = frets + str(fret) + "  "
    if logical_frets == False:
        print dots
    else:
        print frets

def Return_Interval(half_steps):  
    #half_steps is an integer that references the half steps in an interval
    #eg The half step 0 is interval '1'. The half step 7 is interval '5'
    return steps[half_steps]

def Return_Scale_Notes(root_note, notes, intervals):  #root_note is a string, intervals is a list eg ['1','b3','7']
    #Print out the interval, note, half-step, and note for the chosen chord
    #print "Root note:", root_note
    #print "Intervals:", intervals
    notes_from_root = list()
    interval_temp = ""
    for inter in intervals:
        step_from_note = 0
        step = 0
        b=inter.count('b') #Count the number of flats in the interval (eg b3)
        h=inter.count('#') #Count the number of sharps in the interval (eg #5)
        if b>1 or h>=1:
            if b>1: #flattened more than twice
                step=-b
                interval_temp=inter.replace("b", "")
            if h>=1: #sharpened more than once
                step=h
                interval_temp=inter.replace("#", "")
        else:
            interval_temp = inter
        
        #find the number of the interval, then add/substract the number of sharps/flats
        step_from_note = (notes.index(root_note) + steps.index(interval_temp)+step) % 12

        #add valid notes to notes_from_root
        notes_from_root.append(notes[step_from_note])
    return notes_from_root

def Return_Chord_Notes(root_note, chord_name):
    #Given the root_note and chord_name, this function returns a list with the notes in the chord eg. ['Ab', 'C', 'Eb'] for a Ab Major Chord
    
    #print "Root Note:", root_note
    #print "Chord Name: ", chord_name
    #print "Intervals:", chord_dict[chord_name]
    #print "Interval, steps, note"
    
    chord_notes=list()
    for chord in range(1,len(chord_dict[chord_name])):
        interval = chord_dict[chord_name][chord]
        interval_temp = interval
        step = 0
        step_from_note = 0
        #print "chord", chord, "interval", interval, "steps", steps.index(interval)+step
        b=interval.count('b') #Count the number of flats in the interval (eg b3)
        h=interval.count('#') #Count the number of sharps in the interval (eg #5)
        if b>1 or h>=1:
            if b>1: #flattened more than twice
                step=-b
                interval_temp=interval.replace("b", "")
            if h>=1: #sharpened more than once
                step=h
                interval_temp=interval.replace("#", "")
        
        #find the number of the interval, then add/substract the number of sharps/flats
        step_from_note = (notes.index(root_note) + steps.index(interval_temp)+step) % 12
        
        #add valid notes to chord_notes
        chord_notes.append(notes[step_from_note])
        #print interval, steps.index(interval_temp)+step, notes[step_from_note]
    #print "Notes in Chord:", chord_notes
    return chord_notes

#Returns true if the scale contains sharps or flats
def Bool_sharp_scale(scales):
    bool_sharp_scale = False    
    for scale in scales:
        if len(scale)==2:
            bool_sharp_scale = True
            break
    return bool_sharp_scale

#False = Don't show intervals on fretboard,  True = Show notes on fretboard
bool_interval = False

print " "
print "Would you like a guitar or a bass?"
while True:
    #instrument = raw_input().title()
    #instrument = 'Guitar'
    if len(instrument)==0: #If nothing was entered, set the default to guitar"
        instrument = 'Guitar'
        break
    if instrument == 'Bass':
        break
    if instrument == 'Guitar':
        break
    else:
        print "Only guitar and bass are allowed. Your " + instrument + " is not."
print "Selection: " + instrument
print " "

#print distinct list of strings the instrument can have
print "Your string options for " + instrument + " are:"
instrument_list=[]

for tuning_i, notes in tuning_dict.iteritems():
    #print "RE", re.findall('\d+', tuning)[0], tuning
    strings_inst = re.findall('\d+', tuning_i)[0] #creates a list of all the strings that an instrument can have
    if instrument.lower() in tuning_i.lower():
        if (strings_inst + " String "+ instrument) not in instrument_list:
            instrument_list.append(strings_inst + " String "+ instrument)
print instrument_list
print " "

#find the number of strings the instrument has
print "How many strings does your " + instrument.lower() + " have?"
valid_strings = False
while not(valid_strings):
    #string_no = raw_input()
    #string_no = '6'
    #print "STRING NO", string_no
    if len(string_no)==0: 
        if instrument == 'Bass': #If a bass is selected set default to 4 strings"
            string_no = '4'
            valid_strings = True
        if instrument == 'Guitar': #If a guitar is selected set default to 6 strings"
            string_no = '6'
            valid_strings = True
    if int(string_no)>0 and int(string_no)<8:
        if instrument == 'Bass' and (int(string_no)>3 and int(string_no)<7): #If a bass is selected set default to 4 strings"
            valid_strings = True
        if instrument == 'Guitar' and (int(string_no)>5 and int(string_no)<8): 
            valid_strings = True
    else:
        print "Not a valid number for " + instrument.lower()
print "Selection:", string_no
print " "

#Show possible tuning for the instrument and string number
print "What tuning does your " + string_no + " string " + instrument.lower() + " have?"
if len(tuning)==0:
  for tuning_i, notes in tuning_dict.iteritems() :
      if str(instrument.lower() + " " + string_no) in tuning_i.lower():
          #possible_tuning =  tuning_i.replace(instrument, "").replace(string_no, "")
          possible_tuning =  tuning_i.replace(instrument + " " + string_no, "")
          print possible_tuning
  print "Please select your tuning from the above list for your " + string_no + " string "


# Exit out of this loop if someone enters a bad selection 5 times
count = 0
while count <= 5:
    #tuning = raw_input().title()
    #tuning = 'Standard'
    #If no tuning is selected set defaults
    #print "TUNING", tuning, "STRING NO", string_no, "INSTRUMENT", instrument
    if len(tuning)==0: 
        if instrument == 'Guitar':
            tuning = 'Standard'
            print "AAA 1"
        if instrument == 'Bass':
            if string_no == '4':
                print "AAA 2"
                tuning = 'Standard'
            if string_no == '5':
                print "AAA 3"
                tuning = 'Standard B'
            if string_no == '6':
                print "AAA 4"
                tuning = 'Standard'
        your_tuning = str(instrument + " " + string_no + " " + tuning).title()
        count = count + 1 
        break
    else:
        your_tuning = str(instrument + " " + string_no + " " + tuning).title()
        #print "dict", tuning_dict[your_tuning]
        #print "Strip:", your_tuning.title().strip()
        if your_tuning.title() in tuning_dict.keys():
            your_tuning = str(instrument + " " + string_no + " " + tuning).title()
            #print "FOUND", your_tuning, "in tuning_dict"
            break
        else:
            print "Not valid tuning"
            count = count + 1
            break
print "Selection:", tuning
print " "
print "Tuning Instrument:", your_tuning.title()

#randomly chose either flats or sharp to display on fretboard
if randint(0, 1)==0: #random number 0 or 1
    notes = notes_flat
else:
    notes = notes_sharp

tuning = your_tuning

#print a character map of the fretboard for the instrument with the selected tuning
print "Tuning:", tuning_dict[tuning]
print " "

#time.sleep(5)
string_scale = 'All'
Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, notes, bool_scale = True, bool_interval = False)

string_scale = str(settings[5])  # use settings to set back to default

#print "Intervals and their half-steps"
#for chord in steps:
#    print chord, steps.index(chord)
#print "---------------------------------------------------------"

print " "
flat = False
sharp = True

#Continue while loop till a vaild note is chosen
while True: 
    print "Enter root note: (eg " + random.choice(notes_flat) + ")"
    #root_note = raw_input().title()   #eg C
    print "Selection:", root_note
    if len(root_note)==0: #If nothing was entered, set the default to "A"
        root_note = "A"
        flat = True
        break
    if root_note in notes_flat: #If the note contains a flat
        flat = True
        notes = notes_flat
        break
    if root_note in notes_sharp: #If the note contains a sharp
        sharp = True
        notes = notes_sharp
        break
    else:
        print root_note, " is an invalid note"

print " "
print "---------------------------------------------------------"

#Show list of possible chords to chose from
chord_str = ''
print "Chose your chord from the following list:"
for chord, chord_short in sorted(chord_dict.items()):
    chord_str = chord_str + chord_short[0] + ', '
print chord_str[:-2]  #remove the last comma
print "---------------------------------------------------------"

#Enter your chosen chord
valid_chord = False
#chord_name = ""
while not(valid_chord): #Continue the while loop till a valid chord is chosen
    print "Enter chord type: (eg " + random.choice(chord_dict.keys()) + ")"
    #chord_name = raw_input().strip().lower()
    #chord_name = '7#9#5'
    #print len(chord_name), chord_name
    if len(chord_name)==0: #If nothing was entered, set the default to "major"
        chord_name = "major"
        valid_chord = True
        break
    if chord_name in chord_dict.keys(): #Find the chord name in the key to the chord dictionary
        valid_chord = True    
        break
    else:
        for chord, chord_short in chord_dict.iteritems():
            if chord_name == chord_short[0] or chord_name == chord_dict[chord][0]:
                #print "Chord:", chord_name, chord
                chord_name = chord
                valid_chord = True
                break
        if valid_chord == True:
            break
        else:
            valid_chord = False
            print chord_name, " is an invalid chord"
print "Chord:", chord_name
print "---------------------------------------------------------"


#Print out the interval, note, half-step, and note for the chosen chord
print "Root note:", root_note
print "Chord Dictionary: ", chord_name, ":", chord_dict[chord_name]
print "Interval, steps, note"
chord_notes=list()
for chord in range(1,len(chord_dict[chord_name])):
    interval = chord_dict[chord_name][chord]
    interval_temp = interval
    step = 0
    step_from_note = 0
    #print "chord", chord, "interval", interval, "steps", steps.index(interval)+step
    b=interval.count('b') #Count the number of flats in the interval (eg b3)
    h=interval.count('#') #Count the number of sharps in the interval (eg #5)
    if b>1 or h>=1:
        if b>1: #flattened more than twice
            step=-b
            interval_temp=interval.replace("b", "")
        if h>=1: #sharpened more than once
            step=h
            interval_temp=interval.replace("#", "")
    #find the number of the interval, then add/substract the number of sharps/flats
    step_from_note = (notes.index(root_note) + steps.index(interval_temp)+step) % 12
    
    #add valid notes to chord_notes
    chord_notes.append(notes[step_from_note])
    print interval, steps.index(interval_temp)+step, notes[step_from_note]
print "---------------------------------------------------------"

#print "Chord notes: ", chord_notes
#print "---------------------------------------------------------"

print "Valid notes:", chord_notes
print " "

Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, chord_notes, bool_scale = False, bool_interval = False)
print " "
Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, chord_notes, bool_scale = False, bool_interval = True)
print " "
    
#Print out the fretboard for all root notes
print " "
print " "
print chord_name.title(), "Chord for 12 keys"
print "---------------------------------------------------------"
print " "
for root_note in notes_flat:
    chord_notes = Return_Chord_Notes(root_note, chord_name)
    print "Root Note:", root_note
    print "Chord Name:", chord_name.title()
    print "Intervals:", chord_dict[chord_name]   #chord_dict[chord_name][chord]
    print "Chord Notes:", chord_notes

    print " "
    Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, chord_notes, bool_scale = False, bool_interval = False)
    print " "
    Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, chord_notes, bool_scale = False, bool_interval = True)
    print " "

print "---------------------------------------------------------"

# exit()

#Show list of possible scales
print "What scale from the following list do you want to use?"

if len(string_scale) > 0:  #If the scale has already been selected
  print "Selection:", string_scale
else:  #If the scale has not yet been selected
    for Scale_i in ListScales:
        if Scale_i["Scale"] in ShortList_Scale:  #Using a short list of scales
            string_scale = string_scale + Scale_i["Scale"] + ", "
    
    print string_scale[:-2]
    
    #Keep asking for a scale till a valid one is chosen
    valid_scale = False
    pos_scale = [] #possible scale list of names that fit the string_scale
    while not(valid_scale):
        string_scale = raw_input().title()  #Wait for input from the user
        #string_scale = "Byzantine"
        if len(string_scale)==0 or string_scale=="": #If nothing was entered, set the default to Major"
            string_scale = 'Major'
            break
        else:
            for Scale_i in ListScales: #check through list of scales
                if string_scale in Scale_i["Scale"]: #pattern match string with list
                    pos_scale.append(Scale_i["Scale"]) #save to new possible list if the string is in any scale
                    if string_scale == Scale_i["Scale"] or string_scale.lower() == Scale_i["Scale"]:
                        #print "Valid scale", string_scale, "in ", Scale["Scale"]
                        valid_scale = True
                        break
            if valid_scale:
                #print "check len", string_scale
                break
            else:
                print string_scale + " is an invalid scale"
                for possible in pos_scale:
                    print "Try: " + possible
                del pos_scale[:] #delete the possible list after completion
                print " "

print " "
print " "
print string_scale.title(), "Scale in 12 keys"
print "---------------------------------------------------------"
print " "

#Find the Index of the chosen scale
scale_interval = ""
scale_steps = ""
for Scale in ListScales:  # s = scale, h = H_Steps, i = interval (L_Steps)
    #print Scale["Scale"], Scale["H_Steps"], Scale["L_Steps"]
    if Scale["Scale"] == string_scale:  #if the scale matches a scale in ListScales
        scale_steps = Scale["H_Steps"]
        scale_interval = Scale["L_Steps"]
        break

#Print the scales for each of the 12 keys
for root_note in notes_flat:
    scale_notes = Return_Scale_Notes(root_note, notes, scale_interval)
    
    print "Scale Name:", root_note, string_scale   #eg E Major
    print "Steps:",  scale_steps
    print "Intervals:", scale_interval
    print "Scale Notes:", scale_notes
    print " "
    
    Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, scale_notes, bool_scale = True, bool_interval = False)
    print " "
    Show_Fretboard(tuning_dict, tuning, notes_sharp, notes_flat, scale_notes, bool_scale = True, bool_interval = True)
    print " "

print "---------------------------------------------------------"
