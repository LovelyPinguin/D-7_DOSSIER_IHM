import matplotlib.pyplot as plt
import numpy as np

class Hydrolienne():

    materiaux = {'acier': 2.5 * (10**8), 'aluminium' : 2.4 * (10**8)}

    def __init__(self, longeur, hauteur, largeur, rendement, force_eau, divisions=100, materiel='acier'):
        self.force_eau = force_eau
        self.l = longeur
        self.h = hauteur
        self.b = largeur
        self.materiel = self.materiaux[materiel]
        self.rendement = rendement
        self.force_retour =  self.force_eau *  2 / 5
        self.flexion_maximale = self.flexmax()
        self.range = self.setRange(divisions)

        self.torseur = {
            'Fx': 0,          'Mx': 0,
            'Fy': self.fx(),  'My': 0,
            'Fz': 0,          'Mz': self.mz(),
        }

    def setRange(self, divisons):
        elements = []
        size = self.l / divisons
        for i in range(divisons):
            dist = i * size
            elements.append(dist)
        return elements

    def rendementRange(self):
        elements = []
        number = len(self.range)
        size = 100 / number
        for i in range(number):
            dist = i * size
            elements.append(dist)
        return elements

    def flexmax(self, f_eau=None):
        if f_eau == None:
            f_eau = self.force_eau
        mMax = (f_eau - f_eau * 2 / 5) * ((3 / 2) * (self.l - 1)) # N . m 
        y = self.h / 2
        It =  (self.b * self.h * self.h * self.h) / 12
        flexmax =  - (mMax * y) / It # Pa 
        return flexmax
        
    def fx(self):
        valeures = []
        for x in self.range:
            force = (self.force_eau - self.force_retour) * (x - self.l)
            valeures.append(force)
        return valeures

    def mz(self):
        valeures = []
        for x in self.range:
            force = (self.force_eau - self.force_retour) * ( (3 / 2) * self.l - x - (x*x)/2)
            valeures.append(force)
        return valeures
    
    def travail(self, f_eau=None):
        if f_eau == None:
            f_eau = self.force_eau

        f = (f_eau - (2 / 5 * f_eau)) * ( (self.l*self.l)/2 - self.l * self.l)
        g = (f_eau - (2 / 5 * f_eau)) * ( (3 / 2) * self.l * self.l - (self.l*self.l)/2 - (self.l*self.l*self.l)/6)
        return abs(f) + abs(g)
    
    def getEnergyRange(self):
        array =  np.logspace(0, 5, num=100, base=10)
        return array
    
    def rangeTravailJoules(self):
        valeures = []
        my_range = self.getEnergyRange()
        for element in my_range:
            if self.flexmax(element) * self.l * self.h * self.b >= self.materiel:
                valeures.append(0)
            e = self.travail(element)
            valeures.append(e)
        return valeures

    def rangeTravailKwh(self):
        valeures = [e / (3.6 * 10**6) for e in self.rangeTravailJoules()]
        return valeures
    
h1 = Hydrolienne(15, 3, 1, 100, 50, 100, 'acier')

def interface():
    print('Logiciel de détermination des variations de production d\'energie du système: ')
    print('Que voulez-vous faire ? ')
    choix = premier_choix()

    force_eau = demander_force_eau()
    hydro = creer_hydrolienne(force_eau)

    
    if choix == 1:
        plt.plot(hydro.getEnergyRange(), hydro.rangeTravailJoules(), label='Joules générés selon le courant')
        plt.plot(hydro.getEnergyRange(), hydro.rangeTravailKwh(), label='kwh généré par le courant')
        plt.yscale('log')
        plt.xlabel('Force des vagues')
        plt.ylabel('Energie')
        plt.legend()
        plt.show()

    if choix == 2:
        plt.plot(hydro.fx(), hydro.range, label='Force appliquée en fonction de la hauteur')
        plt.plot(hydro.mz(), hydro.range, label='Moments en fonction de la hauteur')
        plt.xlabel('Force Et Moment en N')
        plt.ylabel('Hauteur en M')
        plt.legend()
        plt.show()

    if choix == 3:
        print(f'La flexion maximale de cette hydrolienne est de +/- {abs(hydro.flexion_maximale)} Pa')

def demander_force_eau():
    force = int(input('La force de l\'eau en Pascals (Usuellement 50000): '))
    return force

def premier_choix():
    print('1- Obtenir un graphe de l\'energie générée selon la force du courant')
    print('2- Obtenir un graphe de des Forces et Moments appliquées au système')
    print('3- Obtenir la force de flexion maximale du système')
    choix = int(input('Votre choix (1, 2 ou 3): '))
    return choix

def creer_hydrolienne(force_eau):
    default = input('Ecrivez \'oui\' pour le setup par defaut: ')
    if default == 'oui':
        return h1
    
    longeur = int(input('La hauteur de votre hydrolienne: '))
    hauteur = int(input('La hauteur d\'une section: '))
    largeur = int(input('La largeur d\'une section: '))
    rendement = int(input('Le rendement du système (100 par défaut): '))
    precision = int(input('Le nombre de points sur le graph (100 par défaut): '))
    hydro = Hydrolienne(longeur, hauteur, largeur, rendement, precision, force_eau)
    return hydro

interface()