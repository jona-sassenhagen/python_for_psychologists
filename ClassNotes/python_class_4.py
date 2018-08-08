#!/usr/bin/python
#-- coding: UTF-8 --
from __future__ import unicode_literals, print_function  # diese 3 Zeilen sind hilfreich, weil Psychopy in Python 2 (nicht 3) programmiert ist
from psychopy import monitors, visual, core, event  # Psychopy Basismodule
from numpy import mean

# Bildschirmsetup
m = monitors.Monitor("name")
win = visual.Window(monitor=m)

# Generiere einen Instruktionstext
instructions = visual.TextStim(win, "Tiere: Taste 'S'. Pflanzen: Taste 'L'. Taste, um zu starten.")
# Vorbereiten auf Darstellung
instructions.draw()
# Anzeige
win.flip()
# Warten auf Knopfdruck
event.waitKeys()

tiere = ["Fisch", "Affe", "Schnecke"]
pflanzen = ["Birke", "Palme", "Rose"]
alle_worte = [tiere, pflanzen]  # eine liste aus listen - äquivalent zu [["Fisch", "Affe", "Schnecke"], ["Birke", "Palme", "Rose"]]
tiere_rts, pflanzen_rts = [], []

clock = core.Clock()  # eine Stopuhr
for subliste in alle_worte:
    for wort in subliste:
        w = visual.TextStim(win, wort)  # erstelle einen Textstimulus aus einem String
        w.draw()  # Textstimulus zeichnen
        win.flip()  # Zeichnung auf den Bildschirm schieben
        clock.reset()  # Stopuhr starten
        key = event.waitKeys()[0]  # waitKeys liefert uns eine Liste von Tasten, die in diesem Fall nur einen Eintrag hat
        # 'key' ist jetzt also der Knopf, den die Versuchsperson gedrueckt hat
        rt = clock.getTime()  # Stopuhr abfragen
        # 'rt' hat jetzt die Reaktionszeit (in Sekunden)
        
        # Reaktionszeit abspeichern
        if wort in tiere:
            tiere_rts.append(rt)  # Die Liste um einen Eintrag erweitern
            correct_key = "s"  # festlegen, welches die richtige Taste ist
        else:
            pflanzen_rts.append(rt)
            correct_key = "l"
        
        # Richtiger Knopfdruck?
        if correct_key != key:  # falscher knopfdruck!
            visual.TextStim(win, "Falsch! Weiter mit Taste.").draw()  # negatives feedback
            win.flip()
            event.waitKeys()

# Anzeige Feedback nach dem Experiment
res = """RT auf Tierworte: {}. RTs auf Pflanzenworte: {}. Taste zum fortfahren."""  # Textschablone

tiere_mean = round(mean(tiere_rts), 2)
pflanzen_mean = round(mean(pflanzen_rts), 2)
results = visual.TextStim(win, res.format(tiere_mean, pflanzen_mean))
results.draw()
win.flip()
event.waitKeys()



#Die Hausaufgabe ist:
# 1. Programmieren Sie das Script so um, dass der Versuchsperson nach *jedem 
# einzelnen* Durchlauf (jedem Wort) die Reaktionszeit für diesen Durchlauf 
# angezeigt wird, nicht erst am Ende des Experiments. (Sie müssen also nicht 
# mehr nach Bedingung unterteilen, oder mit einer liste von Reaktionszeiten 
# operieren!)

# 2. Programmieren Sie das Script so um, dass der Versuchsperson angezeigt wird, 
# ob die Reaktionszeit größer oder kleiner als .5 Sekunden/500 msec war.


# (Sie können die beiden kombinieren, also dass der Versuchsperson nach jedem 
# Durchlauf angezeigt wird, ob die Reaktionszeit schneller war als .5 Sekunden.)


# Fragen per Email an mich, oder im Repetitorium bei Hern Wallot! Besonders, 
# wenn Sie einfach nach einer Stunde nicht weiterkommen, einfach mal nachfragen.


# Wenn Sie unbedingt eine Bonusaufgabe wollen: schreiben Sie ein Experiment, bei 
# dem die Versuchspersonen als Antworttaste den Buchstaben drücken sollen, der 
# an der vorletzten Stelle im angezeigten Wort steht. Für falsche Knopfdrücke 
# soll die Versuchsperson getadelt werden.

# Das Beispielscript zeigt, wie Antworten abgefragt und überprüft werden können.

# (Sie können gern auch alle 3 Lösungen in einem kombinieren, dann müssen Sie 
# die ersten zwei nicht extra machen.)



# Bitte schicken Sie ihre Lösung als Antwort an diese Email, und verwenden Sie 
# Dateinamen, aus denen ihr Nachnahme hervorgeht.


# !!! Achtung: wenn sie als letzte Zeile event.waitKeys() setzen, bleibt das 
# Script hängen !!!


# In der nächsten Sitzung schauen wir uns Bilderstimuli und Soundstimuli an und 
# üben weiter mit den Dingen, die wir bereits gelernt haben.