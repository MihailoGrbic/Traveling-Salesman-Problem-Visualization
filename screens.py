import numpy as np
import pygame

from common import window, colors, Object, Button, Text, TextBlock, quitProgram
from NNSim import NNSim
from AntOptSim import AntOptSim
from AntColOptSim import AntColOptSim


state_object = ["MainMenu"]


def updateScreen(state):
    window.fill(colors['White'])
    for obj in list(screens[state]['ObjectDict'].values()):
        obj.draw(force=True)
        pygame.display.update()


def changeState(new_state):
    state_object[0] = new_state
    updateScreen(new_state)


screens = {
    'MainMenu': {},
    'Intro': {},
    'Intro2': {},
    'ExactAlg': {},
    'ApproxAlg': {},
    'NNExplanation': {},
    'NNSim': {},
    'AntOptExplanation': {},
    'AntOptSim': {},
    'AntColOptExplanation': {},
    'AntColOptSim': {},
}

window_dim = np.array(window.get_size())

# Permanent Objects
perma_obj = {'QuitButton': Button(window_dim * [1, 0] + [-85, 50],
                                  size=(150, 80), text="Ugasi", text_size=40, action=quitProgram), }
for screen in screens:
    screens[screen]['ObjectDict'] = perma_obj.copy()

# ----------------------------------------------------------------------------------------------------------------------
# Main Menu
screens['MainMenu']['ObjectDict'].update({
    'IntroductionButton': Button(window_dim / 2 + [-400, +200], (300, 100), color=colors['Yellow'], clicked_color=colors['DarkYellow'],
                                 text="Uvod", action=changeState, action_arg="Intro"),
    'ExactButton': Button(window_dim / 2 + [0, +200], (300, 100), color=colors['Orange'], clicked_color=colors['DarkOrange'],
                          text="Egzaktni algoritmi", action=changeState, action_arg="ExactAlg"),
    'ApproximativeButton': Button(window_dim / 2 + [+400, +200], (300, 100), color=colors['Cyan'], clicked_color=colors['DarkCyan'],
                                  text="Aproksimativni algoritmi", action=changeState, action_arg="ApproxAlg"),

    'MainText1': Text("Problem putujućeg trgovca", window_dim / 2 + [0, -100], 80),
    'MainText2': Text("uvod u problem i najpopularnija rešenja", window_dim / 2 + [0, -30], 50),
    'MainText3': Text("napravio Mihailo Grbić", window_dim / 2 + [0, 20], 30),
    'ContactText': Text("Ako pronađete neki bug obavestite me na mihailogrbic99@gmail.com", window_dim - [410, 30], 30),
})


# ----------------------------------------------------------------------------------------------------------------------
# Intro

screens['Intro']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="MainMenu"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="Intro2"),

    'HeaderText': Text("Uvod", window_dim / 2 + [0, -380], 80),
    'TextBlock': TextBlock("""
Problem pujućeg trgovca (skraćeno PPT) već vekovima predstavlja jedan od \n
najintentzivnije proučavanih problema u optimizaciji.\n
Nije poznato ko je i kada prvi put formulisao ovaj problem ali su aluzije \n
na njega postojale još početkom 1800-tih godina. \n
Postavka problema je prosta: putujući trgovac ima mapu gradova koje mora \n
da poseti, mapa je predstavljena kao graf a gradovi kao čvorovi tog grafa. \n
Putujući trgovac započinje u jednom od gradova i želi da pronađe najkraći \n
put koji obilazi sve gradove i vraća ga u grad u kom je započeo.
                            """, window_dim / 2 + [0, 50], 35),
})

screens['Intro2']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="Intro"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="MainMenu"),
    'HeaderText': Text("Uvod", window_dim / 2 + [0, -380], 80),
    'TextBlock': TextBlock("""
Postoje značajan broj različitih verzija PPT-a. \n
Graf po kom se trgovac kreće može biti usmeren ili neusmeren, gusto ili retko povezan.\n
Putevi između dva grada mogu biti jednaki ili različiti (simetričan / asimetričan PPT),\n
a u nekim verzijama mogu biti i negativni. U nekim verzijama trgovac ne mora da se vrati \n
u svoj početni grad dok u nekim drugim trgovac ne pokušava da minimizuje dužinu celokupnog \n
puta već dužinu najduže grane (Bottleneck PPT). \n
Mi ćemo se fokusirati na osnovnu verziju PPT-a u kojoj je graf gust, neusmeren i simetričan, \n
trgovac mora da se vrati u svoj početni grad i cilja da minimizuje ukupan pređeni put. \n
Težina grane između dva čvora biće jednaka udaljenosti ta dva čvora na ekranu.
                            """, window_dim / 2 + [0, 80], 35),
})

# ----------------------------------------------------------------------------------------------------------------------
# Exact Algorithms
screens['ExactAlg']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="MainMenu"),
    'HeaderText': Text("Egzaktni algoritmi", window_dim / 2 + [0, -380], 80),
    'TextBlock': TextBlock("""
Egzaktni algoritmi za rešavanje PPT-a pronalaze sigurnu najkraću putanju za trgovca. \n
Nakon izvršavanja ovih algoritama možemo biti sigurni da ne postoji nijedan kraći put od pronađenog. \n
Međutim velika mana ovih algoritama jeste njihovo jako dugo vreme izvršavanja. Najintuitivniji egzaktni \n
algoritam PPT-a jeste da prosto probamo sve moguće puteve u grafu i zapamtimo najkraći. Ovaj postupak se \n
svodi na generisanje svih permutacija skupa gradova i računanja dužine puta za svaku permutaciju. \n
Pošto za n gradova postoji n! permutacija, složenost ovog algoritma je O(n!). Čak i za 20 gradova vreme \n
izvršavanja ovog algoritma postaje preveliko za praktičnu primenu. Dok postoje drugi brži, \n
egzaktni algoritmi PPT-a još uvek nije dokazano da se problem može rešiti u složenosti manjoj od O(2^n) što je idalje \n
nepraktično za veliki broj gradova. Iz tog razloga se za rešavanje PPT-a najčešće koriste aproksimativni algoritmi. \n
    (U daljim verzijama treba dodati simulaciju egzaktnih algoritama)
                            """, window_dim / 2 + [0, 80], 35),
})

# ----------------------------------------------------------------------------------------------------------------------
# Approximative Algorithms
screens['ApproxAlg']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="MainMenu"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="NNExplanation"),

    'HeaderText': Text("Aproksimativni algoritmi", window_dim / 2 + [0, -350], 80),
    'TextBlock': TextBlock("""
Za razliku od egzaktnih algoritama, aproksimativni algoritmi ciljaju da pronađu približno rešenje PPT-a, \n
uz značajno kraće vreme izvršavanja. Dok je u nekim situacijama rezultujući put aproksimativnih algoritama nekoliko \n
puta duži od najkraćeg mogućeg puta, u proseku čak i najnaivniji aproksimativni algortimi generišu put koji je za \n
samo 25% duži od najkraćeg, dok najbolji od ovih algoritama generišu put koji je samo 2-3% duži od najkraćeg.\n
Pošto se u većini realnih situacija možemo zadovoljiti približno najkraćim putem, \n
ovi algoritmi su videli mnogo širu primenu od egzaktnih algoritama. \n
U sledećim stranicama ćemo proći kroz algoritme najbližeg suseda, mravlje optimizacije i optimizacije mravljih kolonija.
                            """, window_dim / 2 + [0, 50], 35),
})

screens['NNExplanation']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="ApproxAlg"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="NNSim"),

    'HeaderText': Text("Heuristika najbližeg suseda", window_dim / 2 + [0, -350], 80),
    'TextBlock': TextBlock("""
Najprostiji, najbrži ali ujedno i najneprezicniji aproksimativni algoritam, heuristika najbližeg suseda u svakom \n
koraku pronalazi najbliži neposećeni grad i odlazi do njega. Ovo se ponavlja dok se ne posete svi gradovi. \n
Složenost ovog algoritma je O(n^2) i u proseku generiše put koji je 25% duži od najkraćeg.
                            """, window_dim / 2 + [0, 50], 35),
})

screens['NNSim']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="NNExplanation"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="AntOptExplanation"),
    'MainText1': Text("Heuristika najbližeg suseda", window_dim / 2 + [0, -460], 60),
    'SimulationBox': NNSim(),
})

screens['AntOptExplanation']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="NNSim"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="AntOptSim"),

    'HeaderText': Text("Mravlja optimizacija", window_dim / 2 + [0, -400], 80),
    'TextBlock': TextBlock("""
Mravlja optimizacija je inspirisana biološkim procesima koji se dešavaju kod pravih mrava. Dok se mravi kreću oni \n
ostavljaju feromone i prate feromone drugih mrava. Ukoliko 2 mrava krenu različitim putevima do iste tačke interesa \n
(npr. hrane) mrav koji se kreće kraćim putem će više puta stići da ode do tačke interesa i nazad, \n
i samim tim će ostaviti više feromona na tom putu, što će ohrabriti druge mrave da idu tim putem umesto onim dužim. \n
U algoritmu mravlje optimizacije mrav poprima ulogu putujućeg trgovca. Prilikom odabira sledećeg grada koji će da poseti \n
mrav svakom putu dodeli neku vrednost na osnovu količine feromona na tom putu F i na osnovu dužine tog puta L. \n
Vrednost određenog puta jednaka je F^(1 - beta) * (1/L)^beta, gde je beta podesiv parametar. \n
Na osnovu ovih vrednosti mrav dodeljuje verovatnoću svakom putu P = vrednost[i] / sum(vrednost) i nasumično odabira jedan od puteva. \n
Nakon što je mrav obišao sve gradove on ostavlja feromone na svojoj kompletnoj putanji. Količina feromona koje ostavi je jednaka \n
1 / ukupna dužina puta. Pored toga, nakon svakog obrnutog ciklus deo feromona na svim putevima ispari. \n
Podesiv parametar alfa predstavlja udeo feromona koji ispare nakon jednog ciklusa. \n
                            """, window_dim / 2 + [0, 50], 35),
})

screens['AntOptSim']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="AntOptExplanation"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="AntColOptExplanation"),
    'MainText1': Text("Mravlja optimizacija", window_dim / 2 + [0, -460], 60),
    'SimulationBox': AntOptSim(),
})


screens['AntColOptExplanation']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="AntOptSim"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="AntColOptSim"),
    'HeaderText': Text("Optimizacija sistema mravljih kolonija", window_dim / 2 + [0, -400], 80),
    'TextBlock': TextBlock("""
Kao poboljšanje za algoritam mravlje optimizacije javio se algoritam optimizacije sistema mravljih kolonija, \n
koji mnogo bolje hvata suštinu bioloških procesa kojima se mravi organizuju. Ovaj algoritam podrazumeva kretanje više mrava \n
kroz graf, dok ponašanje jednog specifičnog mrava ostaje poprilično slično kao i u mravljoj optimizaciji. \n
Izuzetak je da sada postoji parametar Istraži koji u procentima određuje verovatnoću da mrav istražuje. \n
Prilikom svakog odabira grada mrav nasumično odabere jedan broj od 0 do 100. Ukoliko je broj manji od Istraži mrav će \n
odabrati put sa najvećom vrednošću. Ukoliko je nasumični broj manji, mrav će se ponašati isto kao i u prethodnom algoritmu. \n
Druga razlika ovog algoritma jeste da mrav sada kontinualno ostavlja feromone po putevima koje prelazi, umesto da ostavlja feromone \n
tek kada poseti sve gradove. Količinu feromona koju jedan mrav ostavlja kontrolišemo pomoću R parametra. \n
Treća razlika je da nakon što su svi mravi obišli sve gradove, mrav koji je prešao najkraći put ostavlja dodatne feromone na svom putu, \n
jednake 1 / ukupna dužina puta, kako bi pojačao najkraći put, \n
čak iako nije puno mrava prešlo preko njega.\n
                            """, window_dim / 2 + [0, 50], 35),
})

screens['AntColOptSim']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="AntColOptExplanation"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="MainMenu"),
    'MainText1': Text("Optimizacija sistema mravljih kolonija", window_dim / 2 + [0, -460], 60),
    'SimulationBox': AntColOptSim(),
})
