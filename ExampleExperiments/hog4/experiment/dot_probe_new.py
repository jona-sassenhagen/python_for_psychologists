#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals, print_function
from psychopy import visual, event, core, sound, monitors, gui
from random import choice, shuffle

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def draw_and_wait(stim, time=.9):
    "Draw one stimulus, flip, wait."
    stim.draw()
    win.flip()
    core.wait(.9)
    
def draw_and_wait_cues(stim_cue, stim_cond, duration):
    "Draw one stimulus, flip, wait."
    stim_cue.draw()
    stim_cond.draw()
    win.flip()
    core.wait(duration)


# Define functions for functionality that will be repeatedly accessed later
def display_text(text):
    "Display text and wait for a keypress."
    stim = visual.TextStim(win, text= text, color=(0, 0, 0))  # construct the stimulus
    stim.draw()  # draw it
    win.flip()  # put it on the screen
    event.waitKeys()  # wait until a key press
    win.flip()  # clear the screen
    core.wait(.5)  # the wait period is in seconds (i.e., 500 msec)
    
def display_text_and_image(text, image, duration):
    "Display text and wait for a keypress."
    text_ = visual.TextStim(win, text= text,pos=(0.0, -250), color="red")  # construct the stimulus
    text_.draw()  # draw it
    stim = visual.ImageStim(win, image)  # construct the stimulus
    stim.draw()  
    win.flip()  # clear the screen
    core.wait(duration)  # the wait period is in seconds (i.e., 500 msec)

def one_trial(cue_cond,cue_cond_pos, cue_neutral, cue_neutral_pos, target_pos, target_side, cue_duration):
    "Run one single trial, return RT and if the correct answer was given."
    correct_response = "x" if target_side == "left" else "m"                                 # Für target pos noch definieren, dass wenn target_pos = -500 target side = left
    fixation_directions = ("left", "right")

    # Fixation sign
    if (block % 2):
        fixation_dir = choice(fixation_directions)
        if (fixation_dir == "left"):
            fname = 'fingerloch_left.png'  # the files are expected to exist in the same directory as this script
        else:
            fname = 'fingerloch_right.png'  # the files are expected to exist in the same directory as this script
        stim = visual.ImageStim(win, fname)  # create the image stimulus
        fixation = "hole"

    else:
        stim = visual.TextStim(win, text= "+", height = 60, color=(0, 0, 0))
        fixation = "cross"
        fixation_dir = None
        
    draw_and_wait(stim)

    stim_cond = visual.TextStim(win, text= cue_cond,pos=(cue_cond_pos, 0),height = 45, color=(0, 0, 0))# eine funktion schreiben, die zwei cues auf einmal zeigt
    stim_neutral = visual.TextStim(win, text= cue_neutral,pos=(cue_neutral_pos, 0), height = 45, color=(0, 0, 0))
    draw_and_wait_cues(stim_neutral, stim_cond, cue_duration)

    
    target = visual.TextStim(win, text= "O", pos=(target_pos, 0), height = 45, color=(0, 0, 0))
    target.draw()
    win.flip()
    
    # Collect response
    clock.reset()  # response time will be in reference to this time point
    try:
        key, time = event.waitKeys(keyList=['x', 'm', 'q'], maxWait=2, timeStamped=clock)[0]
    except TypeError:
        key, time = "miss", -999  # for misses
    if key == "q":
        win.close()
        core.quit()
    # Was the response correct?
    correct =  key == correct_response  # i.e., does it equal the correct_response key?
    #if not correct:
        #error.play()
    return time, correct, key, fixation, fixation_dir


def one_block(n, n_trials=25, training=False):
    "Picking random factor settings, run n_trials trials, then display a message."
    cue_positions = (200,-200)  # set the possible options for each trial
    neutral_cues = list_neutral_cues
    cue_conditions = ("positive", "negative")
    target_positions = (200, -200)
    cue_durations = (.04, 1)
    for trial in range(n_trials):  # the loop will be run n_trials times
        if list_negative_cues and list_positive_cues:
                    cue_condition = choice(cue_conditions)  # damit Experiment nicht abgebrochen wird, weil eine der Listen schon leer
        elif not list_negative_cues:
            cue_condition = "positive" 
        elif not list_positive_cues:
            cue_condition = "negative"
            
        cue_cond = list_positive_cues.pop() if cue_condition == "positive" else list_negative_cues.pop()
        cue_cond_pos = choice(cue_positions)  # select factor settings
        cue_cond_side = "right" if cue_cond_pos == 200 else "right"
        cue_neutral = list_neutral_cues.pop()
        cue_neutral_pos = -cue_cond_pos
        cue_neutral_side = "right" if cue_cond_pos == -200 else "left"
        target_pos = choice(target_positions)
        target_side = "right" if target_pos == 200 else "left" 
        cue_duration = choice(cue_durations)
        time, correct, key, fixation, fixation_dir = one_trial(cue_cond, cue_cond_pos, cue_neutral,cue_neutral_pos, target_pos, target_side, cue_duration)  # run one trial with the randomly drawn parameters
        if not training:  # write the result to the file
            with open(logfile, "a") as f:  # the 'a' means we append to the file - with a 'w', it would be overwritten!
                print(subj_id, age, sex, house, nutella, movie, temp, block, trial, cue_cond, cue_condition, cue_cond_pos, cue_cond_side, cue_neutral,cue_neutral_pos, cue_neutral_side, target_pos, target_side, cue_duration, fixation, fixation_dir, str(key), str(correct), str(time),
                      sep=",", file=f)  # this "sep" separates the columns by a comma
    text = ("This was " + ("training " if training else " ") +
            "block " + str(n + 1) + ". Any key to continue.")
    display_text(text)

# gui for subject information like code or age

subj_info = gui.Dlg(title="**Dot-probe**")
subj_info.addText('Probandendaten')
subj_info.addField('Kürzel')
subj_info.addField('Alter:')
subj_info.addField('Geschlecht:', choices=["weiblich", "männlich"])
subj_info.addField('Welchem Haus Hogwarts ordnest du dich selbst zu?:', choices=["Hufflepuff", "Slytherin", "Ravenclaw", "Gryffindor"])
subj_info.addField('DIE Nutella oder DAS Nutella ?', choices=["die", "das"])
subj_info.addField('Der Pate oder Pulp Fiction ?', choices=["Der Pate", "Pulp Fiction"])
subj_info.addField('Präferierte Duschtemperatur (Grad Celsius):')

ok_data = subj_info.show()  # show dialog and wait for OK or Cancel


complete = len(subj_info.data) == len([True for x in subj_info.data if len(x) != 0])  #true, wenn Maske vollständig ausgefüllt

pictures = ['pulp_fiction.jpeg', 'pulp_fiction_2.jfif', 'pulp_fiction_car.jpeg','pulp_fiction_single.jpeg']
texts = ["Letzter Versuch...", "Auf jetzt...", "Und noch einmal...", "Versuchs nochmal..."]

if subj_info.OK and complete:  # or if ok_data is not None
    print(ok_data)
elif subj_info.OK and not complete: # wenn nicht vollständig ausgefüllt, wird schleife eingeleitet, in der Pbn immer wieder aufgefordert wird, alles auszufüllen
    subj_info.addText('Bitte alles ausfüllen!', color = "red")
    counter = 0
    while subj_info.OK and not complete:
        m = monitors.Monitor("default", width=28.8, distance=200)
        m.setSizePix([800, 600])
        win = visual.Window(
                    allowGUI=False, monitor=m,
                    bitsMode=None,
                    winType='pyglet', rgb=1,
                    fullscr=False,
                    screen=1, units="pix"
                    ) 
        fname = choice(pictures)  # the files are expected to exist in the same directory as this script
        text = texts.pop()
        display_text_and_image(text,fname,.8)
        win.close()
        ok_data = subj_info.show()  # show dialog and wait for OK or Cancel
        complete = len(subj_info.data) == len([True for x in subj_info.data if len(x) != 0])
        counter += 1
        print(ok_data)
        if not subj_info.OK or counter >= 4:
            core.quit()
            
else:
    print('Experiment abgebrochen')
    core.quit()

subj_id = subj_info.data[0]
age = subj_info.data[1]
sex = subj_info.data[2]
house = subj_info.data[3]
nutella = subj_info.data[4]
movie = subj_info.data[5]
temp = subj_info.data[6]


# With Psychopy, we have to manually create a monitor
m = monitors.Monitor("default", width=28.8, distance=200)
m.setSizePix([800, 600])

win = visual.Window(
                    allowGUI=False, monitor=m,
                    bitsMode=None,
                    winType='pyglet', rgb=1,
                    fullscr=True,
                    screen=1, units="pix"
                    )

clock = core.Clock()

# We write to a comma-separated log file - as the name, we chose the current date.
# For now, we just write the header column to the file.
logfile = str(subj_id) + ".csv"  # the 'str' converts the numeric time into a string
with open(logfile, "w") as f:  # note the 'w': it means a new file will be created
    print("subject,age,sex,house,nutella,movie,temperature,block,trial,cue_cond,cue_valence,cue_cond_pos,cue_cond_side,cue_neutral,cue_neutral_pos,cue_neutral_side,target_pos,target_side,duration,fixation,fixation_direction,response,correct,rt", file=f)
# eichtig, dass keine Leerzeichen zwischen spaltennamen, da sonst teil des namens

n_experiment_blocks = 4
n_training_blocks = 0


list_neutral_cues = ["Anruf", "Anzug", "Apfel", "August", "April", "Ausweis", "Bahnhof", "Balkon", "Baum", "Berg", "Bildschirm", "Bus", "Computer", "Dezember", "Dienstag", "Drucker", 
"Eintrittskarte", "Einwohner", "Fahrschein", "Februar", "Fernseher", "Finger", "Flughafen", "Flur", "Füller", "Fuß", "Fußboden", "Garten", "Gast", "Geburtstag",
"Hafen", "Herr", "Hut", "Januar", "Juli", "Juni", "Kaffee", "Kakao", "Keller", "Kellner", "Kleiderhaken", "Koch", "Kugelschrieber", "Kunde", "Laden", "Locher", 
"Löffel", "Mai", "März", "Markt", "Marktplatz", "Monitor", "Name", "November", "Oktober", "Park", "Pass", "Passant", "Platz", "Projektor", "Pullover", 
"RadiergummI", "Rock", "Schinken", "Schlüssel", "Schrank", "Septmeber", "Sessel", "Strumpf", "Stuhl", "Supermarkt", "Tag", "Tee", "Teppich", "Tisch", "Wagen", 
"Wind", "Zeiger", "Zucker", "Zug", "Zuschauer", "Adresse", "Apfelsine", "Apotheke", "Bank", "Bankkarte", "Bedienung", "Beschreibung", "Bestellung", 
"Bibliothek", "Bluse", "Brille", "Brücke", "Cola", "Decke", "Diskette", "Dolmetscherin", "Dose", "Dusche", "Eile"]

list_positive_cues = ["Attraktivität", "Anerkennung", "Belohnung", "Bereicherung", "Bewunderung", "Beliebtheit", "Dankbarkeit", "Ehrlichkeit", "Eleganz", "Entspannung", "Erfolg", 
"Frieden", "Freundschaft", "Frohsinn", "Freiheit", "Genuss", "Gerechtigkeit", "Gesundheit", "Glück", "Geschenk", "Harmonie", "Herzlichkeit", "Höflichkeit", "Hilfsbereitschaft", 
"Kraft", "Kostbarkeit", "Lachen", "Lebensfreude", "Liebe", "Leidenschaft", "Mut", "Optimismus", "Reichtum", "Rücksichtnahme", "Schönheit", "Schatz", "Sicherheit", "Solidarität", 
"Spaß", "Stärke", "Sympathie", "Treue", "Tapferkeit", "Unterstützung", "Vergnügen", "Verehrung", "Wohlstand", "Wohlbefinden", "Zufriedenheit", "Zuverlässigkeit"]  #Umlaute v.a. ä machen manchmal Probleme

list_negative_cues = ["Mord", "Totschlag", "Schmerz", "Leid", "Waffe", "Tod", "Wunde", "Trauer", "Trennung", "Heimweh", "Gefängnis", "Einsamkeit", "Regen", "Depression", "Krankheit", 
"Angst", "Verletzung", "Hass", "Wut", "Panik", "Rache", "Gestank", "Folter", "Krieg", "Bombe", "Droge", "Sucht", "Verzweiflung", "Unfall", "Qual", "Neid", "Ekel", "Terror", "Unglück", 
"Anschlag", "Koma", "Hässlichkeit", "Dummheit", "Sturz", "Schleim", "Übelkeit", "Schock", "Schrei", "Armut", "Pessimismus", "Schrott", "Geisel", "Müll", "Feind", "Horror"]

shuffle(list_neutral_cues)
shuffle(list_positive_cues)
shuffle(list_negative_cues)



# Show the instruction screen
text = ("""
Press "x" if the O appears on the left and "m" if it appears on the right.
Each dot is preceded by a fixation sign and two words.
We begin with 2 training blocks.

Any key to continue. Press "q" instead of "x"/"m" to quit.
""")
display_text(text)

# Run the training
for block in range(n_training_blocks): # ? = anzahl der triningsblöcke /zahl eintragen
    one_block(block, training=True) # ? = anzahl der trials pro block /zahl eintragen

text = ("""
Training finished. The actual experiment begins.
Any key to continue.
""")
display_text(text)

# Run the actual experiment
for block in range(n_experiment_blocks): # anzahl der blöcke /zahl
    one_block(block) # anzahl der trials pro block /zahl

# Finish
text = """Experiment finished. Thank you!"""
fname = "der_pate.jpg"
display_text_and_image(text, fname, 2)

win.close()
core.quit()