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
})


# ----------------------------------------------------------------------------------------------------------------------
# Intro

screens['Intro']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="MainMenu"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="Intro2"),

    'HeaderText': Text("Uvod", window_dim / 2 + [0, -350], 80),
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
    'HeaderText': Text("Uvod", window_dim / 2 + [0, -350], 80),
    'TextBlock': TextBlock("""
TO BE IMPLEMENTED.
                            """, window_dim / 2 + [0, 80], 35),
})

# ----------------------------------------------------------------------------------------------------------------------
# Exact Algorithms
screens['ExactAlg']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="MainMenu"),
    'HeaderText': Text("Egzaktni algoritmi", window_dim / 2 + [0, -350], 80),
    'TextBlock': TextBlock("""
TO BE IMPLEMENTED.
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
Lorem ipsum dolor sit amet, consectetur adipiscing elit, \n
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \n
Ut enim ad minim veniam, quis nostrud exercitation ullamco \n
laboris nisi ut aliquip ex ea commodo consequat.
                            """, window_dim / 2 + [0, 50], 35),
})

screens['NNExplanation']['ObjectDict'].update({
    'BackButton': Button((85, 50), size=(150, 80), color=colors['Orange'], clicked_color=colors['DarkOrange'], text="Nazad",
                         text_size=40, action=changeState, action_arg="ApproxAlg"),
    'ForwardButton': Button(window_dim - [200, 150], size=(150, 80), color=colors['Green'], clicked_color=colors['DarkGreen'], text="Napred",
                            text_size=40, action=changeState, action_arg="NNSim"),

    'HeaderText': Text("Heuristika najbližeg suseda", window_dim / 2 + [0, -350], 80),
    'TextBlock': TextBlock("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit, \n
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \n
Ut enim ad minim veniam, quis nostrud exercitation ullamco \n
laboris nisi ut aliquip ex ea commodo consequat.
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

    'HeaderText': Text("Mravlja optimizacija", window_dim / 2 + [0, -350], 80),
    'TextBlock': TextBlock("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit, \n
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \n
Ut enim ad minim veniam, quis nostrud exercitation ullamco \n
laboris nisi ut aliquip ex ea commodo consequat.
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
    'HeaderText': Text("Optimizacija sistema mravljih kolonija", window_dim / 2 + [0, -350], 80),
    'TextBlock': TextBlock("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit, \n
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \n
Ut enim ad minim veniam, quis nostrud exercitation ullamco \n
laboris nisi ut aliquip ex ea commodo consequat.
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
