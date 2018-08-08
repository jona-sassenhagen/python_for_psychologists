#!/usr/bin/python
#-- coding: UTF-8 --
from __future__ import unicode_literals, print_function

# In dieser Sitzung haben wir kennen gelernt:
# - 'x if cond else y' - Syntax
# - , wie man mit Psychopy Bilder anzeigen, Töne abspielen und wie man mit Python in Dateien schreiben kann
# - enumerate


# Eine neue Datei erstellen
with open("testfile.csv", "w") as f:  # erzeugt eine Datei im Verzeichnis, in dem das Psychopy-Script ist
    print("Zeile 1", file=f)          # alternativ vollen Dateinamen angeben

# An eine Datei anhängen - zb. Reaktionszeiten
with open("testfile.csv", "a") as f:
    print("Zeile 2", file=f)


from psychopy import visual, event, core, sound, monitors

m = monitors.Monitor("test")
win = visual.Window(monitor=m, units='pix',
                   fullscr=False
                    )


visual.TextStim(win, "Es geht los ... \n\n\nMit Knopfdruck anfangen.").draw()
win.flip()
key = event.waitKeys()[0]


# If/Else-Conditionals
esc_in_key = "Ja" if "esc" in key else "No"
print(esc_in_key)


# enumerate(), um beim iterieren einen laufenden Index zu haben
words = ["Das", "ist", "ein", "Satz"]

clock = core.Clock()
for index, word in enumerate(words):
    visual.TextStim(win, word, height=30, color=(.5, .5, 1)).draw()
    win.flip()
    clock.reset()
    event.waitKeys()
    rt = clock.getTime()
    visual.TextStim(win, "Das war Wort Nummer " + str(index + 1)).draw()
    win.flip()
    event.waitKeys()
    with open("testfile.csv", "a") as f:
        print("rt was: ", + str(rt), file=f)



# Einen nervigen Warnton abspielen
sound.Sound().play()


# Ein Bild anzeigen
visual.ImageStim("bild.jpg").draw()  # dieses Bild muss natürlich existieren ...
win.flip()
event.waitKeys()



# Today's Homework Assignment:

# Ihre Aufgabe ist folgende: programmieren Sie ein psychopy-Script, dass der 
# Reihe nach drei Stimuli abspielt, auf einen Tastendruck wartet, und die 
# Reaktionszeit (Zeit zw. Stimulus und Knopfdruck) jeweils in eine Datei 
# schreibt #(natürlich immer die gleiche Datei).
# Als Stimuli können Sie frei kombinieren aus Worten/Text, Bildern und # Tönen/Soundfiles.

# Fangen Sie auch schon einmal über ein Experiment nachzudenken an. Es kann 
# ruhig blödsinnig sein und es gibt keinen Abzug dafür, aber wenn Sie eine echte 
# Forschungsfrage haben, geht das auch. In der nächsten Sitzung schließen wir 
# mit Psychopy ab, danach geht es an die Datenanalyse.
