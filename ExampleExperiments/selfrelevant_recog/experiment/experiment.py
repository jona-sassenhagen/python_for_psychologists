# imports 
from __future__ import unicode_literals, print_function
from psychopy import visual, event, core, monitors
from random import choice

# creating a monitor
m = monitors.Monitor("default", width=28.8, distance=200)
m.setSizePix([800, 600])
win = visual.Window(allowGUI=False, monitor=m, bitsMode=None, winType='pyglet', color=(1,1,1), fullscr=False, screen=1, units="pix")

clock = core.Clock() 

# creating a logfile
logfile = "log" + str(clock.getTime()) + choice('abcdefghijklmnopqrstuvwxyz') + ".csv"
with open(logfile, "w") as f:
    print("block,trial,congruence,label,correct,rt", file=f)

n_experiment_blocks = 4

def draw_and_wait(stim, time=.495):
    "Draw one stimulus, flip, wait."
    stim.draw()
    win.flip()
    core.wait(time)

def display_text(text):
    "Display text and wait for a keypress."
    stim = visual.TextStim(win, text=text, color=(-1, -1, -1)) #construct the stimulus
    stim.draw()  # draw it
    win.flip()  # put it on the screen
    event.waitKeys()  # wait until a key press
    win.flip()  # clear the screen
    core.wait(.5)  # wait a specific period


def one_trial(congruence, label):
    
    # define the fixation cross
    stim = visual.TextStim(win, text="+", color=(-1, -1, -1))
    draw_and_wait(stim) 
    
    if label == "Ich":
        stim = visual.TextStim(win, text="Ich", color=(-1, -1, -1), pos=(-150, 0)) #show "Ich"-label
        stim.draw()
        if congruence == True: # conruence = Ich + Dreieck
            fname = 'dreieck.png'
            stim = visual.ImageStim(win, fname, pos=(150, 0), size=(100, 100))
            stim.draw()
        else: 
            fname = 'kreis.png'
            stim = visual.ImageStim(win, fname, pos=(150, 0), size=(50, 50))
            stim.draw()
    else:
        stim = visual.TextStim(win, text="Stuhl", color=(-1, -1, -1), pos=(-150, 0)) #show "Stuhl"-label
        stim.draw()
        if congruence == True: # conruence = Stuhl + Kreis
            fname = 'kreis.png'
            stim = visual.ImageStim(win, fname, pos=(150, 0), size=(50, 50))
            stim.draw()
        else: 
            fname = 'dreieck.png'
            stim = visual.ImageStim(win, fname, pos=(150, 0), size=(100, 100))
            stim.draw()
    win.flip() 

    # collect response
    clock.reset()
    try:
        key, time = event.waitKeys(keyList=['c', 'm', 'q'], maxWait=3, timeStamped=clock)[0]
    except TypeError:
        key, time = "miss", -999  
    if key == "q":
        win.close()
        core.quit()
        
    # response: correct = "m", incorrect = "c" + error
    if congruence == True:
        correct = key == 'm'
    else:
        correct = key == 'c'
    if not correct:
        fname = 'error.png' 
        stim = visual.ImageStim(win, fname, size=(150, 150))
        draw_and_wait(stim)
    return time, correct

def one_block(n, n_trials=10):
    "Picking factor settings, run n_trials trials and display a message afterwards."
    labels = ("Ich", "Stuhl")  # possible options for labels for each trial
    congruences = (True, False)
    for trial in range(n_trials):  # the loop will be run n_trials times
        label = choice(labels)
        congruence = choice(congruences)
        time, correct = one_trial(congruence, label)  # run one trial with the randomly drawn parameters
        with open(logfile, "a") as f:  # the 'a' means we append to the file - with a 'w', it would be overwritten!
            print(n+1, trial, str(congruence), label, str(correct), str(time), sep=",", file=f)  
    if n+1 == n_experiment_blocks:
        text = ("Thank you for your participation. Press any key to finish.")
    else:
        text = ("This was block " + str(n + 1) + " of " + str(n_experiment_blocks) + " blocks in total. Press any key to continue.")
    display_text(text)

# First: Show the instruction screen 
text = ("""Before starting the experiment, you need to learn the following associations:
    
    The word Ich is associated with a triangle.
    The word Stuhl is associated with a circle.

Please remember these associations well.

In the following experiment you will be shown a word and a geometric figure (circle or triangle) at the same time.

Press 'm'  when you have learned the shown combination.
Otherwise press 'c'.

Press any key to continue.""")
display_text(text)

# Second: Run the experiment and quit afterwards
for block in range(n_experiment_blocks):
    one_block(block) 
win.close()
core.quit()
