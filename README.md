---
title: "README.md"
author: "fusionprogguy"
date: "Sunday, June 21, 2015"
output: html_document
---

# README

Project: [Fretboard Python Program](Fretboard.py)

This Python code in [Fretboard.py](Fretboard.py) can print out chords and scales in a text based format that you can cut and paste into a document to practice on your stringed instrument.

The purpose of the program was to learn more about chord and scale theory, and provide the user with visual material with which to learn where the notes are located on the fretboard, and to practice reaching those notes while playing chords or scales.

##Code outline for script [run_analysis.R](run_analysis.R)

The program asks you to chose between a guitar or a bass, and has different options for each selection. If you chose a guitar, you can chose between a 6 string or 7 string guitar. If you chose bass, you can select a 4 string, 5 string, or 6 string bass. For each of those you will have multiple tuning options.

You will then be asked what tuning your selected instrument has and given a list of options.

If you don't select a specific tuning for the bass or guitar, it will default to a 6 string guitar with standard tuning, or it will default to a 4 string bass with standard tuning.

The program will print out your entire fretboard with all notes from the open string to the 12th fret for each string. 

The program will ask you to enter a root note (eg E)

Then you will be asked to chose a chord from a list (eg maj7). It will then list the full name for the chord (eg augmented 7th sharp nine) and list all the intervals in this chord eg [1, 3, #5, b7, #9] and the corresponding half steps and notes.

Then the program will print out the fretboard again, with the positions of all the notes for the selected chord and key.

Finally, the program will ask you to pick a scale from a long list. After you type in the name, it will show you the scale formula and the intervals for example:

```
Scale: Byzantine
Formula: R, H, 1.5, H, W, H, 1.5, H
Intervals: 1, b2, 3, 4, 5, b6, 7
```

## Installation

If you don't have Python installed you can use various online webpages to run the code from your browser. If they have multiple version of Python available select the older one. Both websites provide an online compiler which allows you to compile source code and execute it online in more than 60 programming languages.

Two web pages that allow you to run source code are:
1. [http://www.tutorialspoint.com](http://www.tutorialspoint.com/execute_python_online.php)

2. [http://ideone.com](http://ideone.com/)

Simply copy and paste [Fretboard.py](Fretboard.py) and press "Execute" in tutorialspoint or "Run" in ideone.

## Using [Fretboard.py](Fretboard.py)

As I have set this project aside for the time being, I have taken out code which accepts user input so as to streamline testing. As the project is at the moment, there should be no errors, so will run smoothly using user input once small edits have been made. 

If you want to edit the code to allow for user input and remove default values, simply remove the # comment which references 'raw_input()' and comment out the line below it. For example, if you see:

```
    #instrument = raw_input().title()
    instrument = 'Guitar'
```
Change this to:

```
    instrument = raw_input().title()
    #instrument = 'Guitar'    
```

Simply find all instances with "= raw_input() and adjust the comments as described above.


## Credits

After having writen the code I've found other software developers who are into music and providing useful programs online for those wanting to learn the fretboard. 

Their guitar scale generator can be found here:
[http://www.fachords.com/guitar-scale-generator](http://www.fachords.com/guitar-scale-generator)

One limitation in comparison to my program is that Fachords only provides tunings for 6-string guitars, whereas my program offers bass and guitar from 4-7 strings. The code is easily modifyable to add more stringed instruments and tunings.

## Future updates

When I have time I would like to continue with my program by opening files with default settings instead of having to type them in each time, and adding options to create 1, 2, 3, or 4 octave practice runs to hit each part of the fretboard. 

I would also like add a tab print out feature, but also explore other visulisation options for those who do not like traditional tabs. The guitar scale generator by Fachords will surely be an inspiration for a text based version.

## Music Theory

For those new to music theory, here are some introductions to how scales and modes work, and the respective intervals between notes.

[https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes](https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes)
[https://en.wikibooks.org/wiki/Music_Theory/Scales_and_Intervals](https://en.wikibooks.org/wiki/Music_Theory/Scales_and_Intervals)
[https://en.wikipedia.org/?title=Scale_(music)](https://en.wikipedia.org/?title=Scale_(music))

## License

The scales and chords and related code in the files related to this project is distributed AS-IS and no responsibility implied or explicit can be addressed to the authors for its use or misuse. Any commercial use is prohibited without express permission.

## Contact

e-mail: steven.muschalik@gmail.com
Twitter: @StevenMuschalik