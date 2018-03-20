#!/usr/bin/python
#-- coding: UTF-8 --

from __future__ import unicode_literals, print_function
from psychopy import visual, event, core, monitors
from random import choice


m = monitors.Monitor("default", width=28.8, distance=200)
m.setSizePix([800, 600])

win = visual.Window(
                    allowGUI=False, monitor=m,
                    bitsMode=None,
                    winType='pyglet', rgb=1,
                    fullscr=False,
                    screen=1, units="pix"
                    )


clock = core.Clock()



logfile = "log" + str(clock.getTime()) + ".csv"
with open(logfile, "w") as f:
    print("block,trial,congruence,label,correct,rt", file=f)

n_experiment_blocks = 4

def draw_and_wait(stim, time=.495):
    "Draw one stimulus, flip, wait."
    stim.draw()
    win.flip()
    core.wait(time)



def one_trial(congruence, label):
    "Run one single trial, return RT and if the correct answer was given."

    stim = visual.TextStim(win, text="o", color=(-1, -1, -1))
    draw_and_wait(stim)
    
    if label == 'Ich': 
        stim = visual.TextStim(win, text='Ich', pos=(-250,0), color=(-1, -1, -1))
        stim.draw()
        if congruence == True:
            fname = 'snake.png'
            stim = visual.ImageStim(win, fname, pos=(250,0), size=(200,200))
            stim.draw()
        else: 
            fname = 'spider.png'
            stim = visual.ImageStim(win, fname, pos=(250,0), size=(200,200))
            stim.draw()
    else:
        stim = visual.TextStim(win, text='Stuhl', pos=(-250,0), color=(-1, -1, -1))
        stim.draw()
        if congruence == True:
            fname = 'spider.png'
            stim = visual.ImageStim(win, fname, pos=(250,0), size=(200,200))
            stim.draw()
        else: 
            fname = 'snake.png'
            stim = visual.ImageStim(win, fname, pos=(250,0), size=(200,200))
            stim.draw()
    win.flip()
    

    clock.reset()
    try:
        key, time = event.waitKeys(keyList=['m', 'c', 'q'], maxWait=3, timeStamped=clock)[0]
    except TypeError:
        key, time = "miss", -999
    if key == "q":
        win.close()
        core.quit()
    
    if congruence == True:
        correct = key == 'm'
    else:
        correct = key == 'c'
    
    if not correct: 
        fname = 'error.png'
        stim = visual.ImageStim(win, fname, size=(200,200))
        draw_and_wait(stim)
    return time, correct 
    
def display_text(text):
    "Display text and wait for a keypress."
    stim = visual.TextStim(win, text= text, color=(-1, -1, -1))
    stim.draw()
    win.flip()
    event.waitKeys()
    win.flip()
    core.wait(.495)
    
    
    
def one_block(n, n_trials=8):
    labels = ("Ich", "Stuhl")
    congruences = (True, False)
    for trial in range(n_trials):
        label = choice(labels)
        congruence = choice(congruences)
        time, correct = one_trial(congruence, label)

        with open(logfile, "a") as f:
            print(n, trial, str(congruence), label, str(correct), str(time),sep=",", file=f)
    if n+1 == n_experiment_blocks:
        text = ("Thank you again for your participation. Press any key to finish.")
    else:
        text = ("This was block" + str(n + 1) + " of " + str(n_experiment_blocks) + " blocks in total. Press any key to continue.")
    display_text(text)



text = ("""
Welcome to this experiment and thank you for participation!

Please, 

- Press 'm' if 'Ich' or 'Stuhl' matches the associated picture.

- Press 'c' if .'Ich' or 'Stuhl' do not match the associated picture.

Press any key to continue.
""")
display_text(text)




for block in range(n_experiment_blocks):
    one_block(block)


win.close()
core.quit()
