# imports

from __future__ import unicode_literals, print_function

from psychopy import visual, event, core, monitors

from random import choice



# With Psychopy, we have to manually create a monitor

m = monitors.Monitor("default", width=28.8, distance=200)

m.setSizePix([800, 600])



win = visual.Window(

                    allowGUI=False, monitor=m,

                    bitsMode=None,

                    winType='pyglet', rgb=1,

                    fullscr=False,

                    screen=1, units="pix"

                    )



# We need to create a Clock object to check response times

clock = core.Clock()



# We write to a comma-separated log file - as the name, we chose the current date.

# For now, we just write the header column to the file.

logfile = "log" + str(clock.getTime()) + ".csv"  # the 'str' converts the numeric time into a string

with open(logfile, "w") as f:  # note the 'w': it means a new file will be created

    print("block,trial,label,congruence,correct,rt", file=f)



n_experiment_blocks = 4

n_trials = 10

size_pic_x = 200

size_pic_y = size_pic_x

pos_label = -250

pos_animal = -pos_label



# Define functions for functionality that will be repeatedly accessed later

def draw_and_wait(stim, time=.745):

    "Draw one stimulus, flip, wait."

    stim.draw()

    win.flip()

    core.wait(.495)



def display_text(text):

    "Display text and wait for a keypress."

    stim = visual.TextStim(win, text=text, color=(0, 0, 0))  # construct the stimulus

    stim.draw()  # draw it

    win.flip()  # put it on the screen

    event.waitKeys()  # wait until a key press

    win.flip()  # clear the screen

    core.wait(.5)  # the wait period is in seconds (i.e., 500 msec) 





def one_trial(label, congruence):

    "Run one trial"

    #fixation cross

    stim = visual.TextStim(win, text='+', color=(0, 0, 0))

    draw_and_wait(stim)

    

    #show the label

    stim = visual.TextStim(win, text=label, pos=(pos_label, 0), color=(-1, -1, -1)) #Label steht immer links

    stim.draw()

    congruent = "owl.jpg" if label == "Ich" else "bug.jpg"

    incongruent = "owl.jpg" if label == "Stuhl" else "bug.jpg"

    fname = congruent if congruence else incongruent

    stim = visual.ImageStim(win, fname, size=(size_pic_x,size_pic_y), pos=(pos_animal, 0)) 

    stim.draw()

    win.flip() #jetzt wird das ganze angezeigt

    

    # Collect response

    clock.reset()  # response time will be in reference to this time point

    try:

        key, time = event.waitKeys(keyList=['c', 'm', 'q'], maxWait=5, timeStamped=clock)[0] #wartet 5s

    except TypeError:

        key, time = "miss", -999  # for misses

    if key == "q":

        win.close()

        core.quit()

    if congruence == True:

        correct = key == 'c'

    else:

        correct = key == 'm'

    # Falls eine falsche Antwort gegeben wurde, Signal:

    if not correct:

        fname = 'falsch.jpg'

        stim = visual.ImageStim(win, fname, size=(size_pic_x,size_pic_y))

        draw_and_wait(stim)

    return time, correct





def one_block(n, n_trials):

    "Picking random factor settings, run n_trials trials, then display a message."

    labels = ("Ich", "Stuhl")# labels, damit man die randomisieren kann

    congruences = (True, False)

    for trial in range(n_trials):  # the loop will be run n_trials times

        label = choice(labels)  # select factor settings

        congruence = choice(congruences)

        time, correct = one_trial(label, congruence)  # run one trial with the randomly drawn parameters

        with open(logfile, "a") as f:  # the 'a' means we append to the file - with a 'w', it would be overwritten!

            print(n+1, trial+1, label, str(congruence), str(correct), str(time), # checken, ob bei cong wirklich ein str hin muss

                      sep=",", file=f)  # Werte durch Kommata trennen. Wenn man nicht n+1 schreibt, steht im logfile 0 fuer Block1

    if n+1 == n_experiment_blocks:

        text= ("Danke fuer Ihre Teilnahme. Druecken Sie eine Taste um das Experiment zu beenden.")

    else:

        text = ("Das war Block " + str(n + 1) + " von " + str(n_experiment_blocks) + ". Druecken Sie eine Taste zum Fortfahren.")

    display_text(text)



# Display mit der Instruktion

text = ("""

In diesem Experiment sollen Sie sich zwei Woerter mit jeweils einem zugehoerigen Tier merken und darauf reagieren. 
Dabei gehoert immer das Wort Ich zur Eule und das Wort Stuhl zum Marienkaefer.

Ihre Aufgabe ist es, per Tastendruck anzugeben, ob dies die Kombination ist, die Sie zu Beginn gelernt haben.
Wenn Ja, druecken Sie die Taste "C", wenn Nein, druecken Sie die Taste "M".
Vor jedem Durchgang erscheint ein Kreuz, das Sie zunaechst anschauen sollen.

Bitte praegen Sie sich die Zuordnung jetzt ein und druecken Sie dann eine der beiden Tasten.

""")

display_text(text)





# Run experiment

for block in range(n_experiment_blocks):

    one_block(block,n_trials)



win.close()

core.quit()



