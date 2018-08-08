#!/usr/bin/python
#-- coding: UTF-8 --
from __future__ import unicode_literals, print_function

from psychopy import event, core, monitors, sound, visual
from random import choice, shuffle, randint

win = visual.Window(allowGUI=False, #monitor=m,
                    fullscr=False, winType='pyglet', units='pix', rgb=-.5,
                    )

clock = core.Clock()

try:
    s = sound.Sound(octave=4)
    def bad_feedback():
        s.play()
        core.wait(2.5)
except:
    def bad_feedback():
        for _ in range(10):
            visual.TextStim(win, "Fehler!!!").draw()
            win.flip()
            core.wait(.1)
            win.flip()
            core.wait(.1)
        core.wait(.5)

keys = ['s', 'l']

fname = "names_{}.csv".format(core.getAbsTime())
with open(fname, 'w') as f:
    print("trial_id,word,correct_key,button,rt", file=f)

umlaut_dict = {
    "ß":"ss",
    "ü":"ue",
    "ä":"ae",
    "ö":"oe",
    }
def fix_umlaut(w):
    try:
        return "".join([umlaut_dict.get(c.lower(), c.lower()) for c in w])
    except:
        return w

words = "Jagen,Verfolgen,Angreifen,Verschlingen,Beißen,Mord,Raub,Brandstiftung,Einbruch,Erpressung,Kotzen,Würgen,Husten,Keuchen,Spucken,Lachen,Sprechen,Singen,Sagen,Fragen,Mögen,Lieben,Begehren,Verehren,Hochachten,Demokratie,Diktatur,Monarchie,Kommunismus,Kapitalismus,Börse,Kredit,Schulden,Zinsen,Aktien,Golf,Basketball,Fußball,Tennis,Rugby,Sprinten,Joggen,Laufen,Rennen,Springen,Schleichen,Kriechen,Hüpfen,Gehen,Wandern,Hören,Sehen,Fühlen,Schmecken,Riechen,Methan,Sauerstoff,Helium,Stickstoff,Chlor,Platin,Kupfer,Eisen,Silber,Gold,Diamant,Quarz,Granit,Marmor,Beton,Burg,Haus,Hütte,Halle,Garage,Hammer,Zange,Lötkolben,Feile,Säge,Axt,Beil,Keule,Schwert,Bogen,Geige,Klavier,Flöte,Schlagzeug,Gitarre,Rock,Ledermantel,Jeans,Jacke,Hose,Socken,Pullover,Hemd,Krawatte,Schal,Tee,Kaffee,Wasser,Trinkschokolade,Saft,Bier,Wein,Whisky,Scotch,Rum,Cola,Fanta,Sprite,Pepsi,Mezzo-Mix,Kuchen,Brötchen,Kekse,Waffeln,Windbeutel,Joghurt,Käse,Quark,Sahne,Buttermilch,Steak,Schnitzel,Geflügel,Filet,Braten,Richter,Polizist,Lehrer,Pfarrer,Professor,Chirurg,Psychiater,Urologe,Hausarzt,Notarzt,Tischler,Schreiner,Maurer,Schmied,Steinmetz,Efeu,Algen,Moos,Bambus,Kaktus,Rose,Lilie,Tulpe,Orchidee,Veilchen,Birke,Eiche,Trauerweide,Fichte,Ahorn,Qualle,Lama,Fledermaus,Affe,Gnu,Amsel,Pinguin,Spatz,Adler,Storch,Hai,Karpfen,Goldfisch,Lachs,Forelle,Puma,Löwe,Leopard,Tiger,Panther"
words = words.split(",")
if choice([True, False]):
    words = list(reversed(words))
words2 = [w for w in words]
shuffle(words2)

names = {"Johannes", "Klaus", "Antonia", "Harald", "Nelly", "Leonie", "Michael", "Katrin", "David", "Jaqueline", "Samson", "Simone", "Zacharias", "Axel",
         "Mechtild", "Max", "Moritz", "Nina", "Tim", "Tina", "Agathe", "Ricarda", "Lea", "Louise", "Elisabeth", "Olaf", "Hendrik", "Helmut",
         "Ulrike", "Jenny", "Bettina", "Bert", "Matthias", "Ingrid", "Ludwig", "Gert", "Gerhard", "Gesine", "Mohammed", "Friedrich", "Felix", "Aylin", "Helene",
         "Katerina", "Jonas", "Michael", "Thomas", "Dietmar", "Ingmar", "Jochen", "Joachim", "Lukas", "Johanna", "Franziska", "Inga", "Ina",
         "Hans", "Jakob", "Jasmin", "Sebastian", "Benjamin", "Christian", "Svenja", "Sven"}

def show_instructions(ant_key, nonant_key, ispause=True):
    p = "Kleine Pause. Zur Erinnerung:\n\n" if ispause else ' '
    inst = u"""
{}Wenn das gezeigte Wort der Name einer Person ist, drücke {}. Sonst drücke {}.""".format(p, ant_key.upper(), nonant_key.upper())
    visual.TextStim(win, inst).draw()
    win.flip()
    event.waitKeys()
    win.flip()
    core.wait(.5)


def trial(ii, w, ant_key, nonant_key, t=.5):
    correct_key = ant_key if w in names else nonant_key
    res = False
    iscorrect = True
    visual.TextStim(win, w).draw()
    event.clearEvents()
    win.callOnFlip(clock.reset)
    event.clearEvents()
    win.flip()
    core.wait(t)
    res = event.getKeys(timeStamped=clock)
    win.flip()
    core.wait(t, hogCPUperiod=t)
    if not res:
        res = event.getKeys(timeStamped=clock)
    core.wait(t, hogCPUperiod=t)
    try:
        button, rt = res[0]
    except:
        button, rt = 'miss', 999
    if button != correct_key:
        iscorrect = False
        bad_feedback()
    with open(fname, 'a') as f:
        fb = [ii, fix_umlaut(word), correct_key, button, rt]
        line = ",".join([str(x) for x in fb])
        print(line, file=f)


shuffle(keys)
show_instructions(*keys, ispause=False)
ii = 0

while len(words) > 0 and len(words2) > 0:
    was_target = False
    if (len(words) + len(words2) < 0) or randint(0, 4) == 0:
        word = choice(list(names))
    elif len(words) > 0 and choice((True, False)):
        word = words.pop()
    else:
        word = words2.pop()
    trial(ii, word, *keys)
    if (ii % 20) == 0:
        show_instructions(*keys)
    ii += 1

visual.TextStim(win, "Das war's! Vielen Dank.").draw()
win.flip()
event.waitKeys()
