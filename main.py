#!/usr/bin/python3.1 
### -*- coding:Utf-8 -*-
###
### Dwarf & Dungeon : Rogue-like en développement.
### Copyright (C) 2010  E. Lévêque & R. Verschelde
### Contact : rverschelde@gmail.com
###
### This program is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.



### --- Imports de librairies ---
### =============================

from tkinter import *
from random import *
from math import *

from globales import *


### --- Classes ---
### ===============


class Matrice:
    """Classe modélisant une matrice, à 'larg' colonnes et 'haut' lignes.
    On accède à une case de la matrice par ses coordonnées j, i.
    Les indices vont de 0 à len(matrice)-1 et l'ordre des coordonnées est : numéro de colonne, puis numéro de ligne, contrairement aux matrices mathématiques pures.
    La matrice est initialement peuplée de obj.
    """
    def __init__(self, larg, haut, obj = 0):
        """Constructeur de la matrice.
        Les arguments sont le nombre larg de colonnes et le nombre haut de lignes.
        La matrice est une liste de listes stockée dans l'attribut _mat.
        """
        j, i = 0, 0
        self._mat = list()
        self.nblig = haut
        self.nbcol = larg
        while j<self.nbcol:                      # j est l'indice des colonnes
            self._mat.append([])
            while i<self.nblig:                  # i est l'indice des lignes
                self._mat[j].append(obj)
                i += 1
            i = 0
            j += 1
    def __getitem__(self, coord):
        """Méthode donnant accès à une case de la matrice via la syntaxe matrice[j,i].
        L'argument de coordonnées doit donc bien être passé sous forme d'un tuple de deux entiers.
        """
        j, i = coord[0], coord[1]
        return self._mat[j][i]
    def __setitem__(self, coord, valeur):
        """Méthode modifiant une case de la matrice via la syntaxe matrice[j,i] = valeur.
        L'argument de coordonnées doit donc bien etre passé sous forme d'un tuple de deux entiers.
        """
        j, i = coord[0], coord[1]
        self._mat[j][i] = valeur
    def __repr__(self):
        """Méthode modifiant l'affichage du type d'objet quand on l'entre dans l'interpréteur."""
        return "Matrice de {0} lignes et {1} colonnes.".format(self.nblig, self.nbcol)
    def __str__(self):
        """Méthode effectuant l'affichage de la matrice quand passée en argument de print."""
        i, j = 0, 0
        chaine = str()
        while i<self.nblig:
            while j<self.nbcol:
                chaine += str(self._mat[j][i])
                j += 1
            if i != self.nblig-1:
                chaine += '\n'
            j = 0
            i += 1
        return chaine

class Niveau:
    """Classe modélisant un niveau de Dwarf & Dungeon.
    L'accès direct à l'objet est une matrice indiquant le type de case (praticable ou non, escalier...).
    L'objet possède aussi en attributs une matrice indiquant les cases ayant été vues, et une matrice stockant le profil du labyrinthe.
    """
    def __init__(self, larg, haut):
        """Constructeur du niveau.
        Construction du labyrinthe dans l'attribut principal _main.
        Construction de la matrice indiquant les cases vues ou non (brouillard).
        Une case vue est représentée par un 1, une case non vue par un 0.
        Construction de la matrice stockant le profil du labyrinthe.
        Le profil d'une case est indiquée par les points cardinaux des murs.
        """
        ### Création du labyrinthe
        self.lvl = len(niv)
        self.larg = larg
        self.haut = haut
        self._main = Matrice(self.larg, self.haut, 0)  # Création de la matrice principale peuplée de 0
        self.creuserNiveau()                           # Creusage du niveau
        ### Matrice des vues
        self.vues = Matrice(self.larg, self.haut, 0)
        ### Matrice de profil
        self.profil = Matrice(self.larg, self.haut, '')
        self.tracerProfil()
        ### Liste des monstres
        self.monstres = list()
        self.monstrescoord = list()
        j, i = 0, 0         # Création d'un premier monstre minotaure, première étape vers la population des niveaux et le pathfinding
        while self[j,i] == 0:       
            j, i = randrange(self.larg), randrange(self.haut)
        self.monstres.append(Monstre(self.lvl, j, i, 'minotaure'))
        self.monstrescoord.append([j, i])     # Peut devenir problématique si cette commande recopie la valeur au lieu de lier les variables.
            
    def __getitem__(self, coord):
        """Méthode donnant accès à une case de la matrice principale via la syntaxe niveau[j,i].
        L'argument de coordonnées doit donc bien être passé sous forme d'un tuple de deux entiers.
        """
        j, i = coord[0], coord[1]
        return self._main[j,i]
        
    def __setitem__(self, coord, valeur):
        """Méthode modifiant une case de la matrice principale via la syntaxe niveau[j,i] = valeur.
        L'argument de coordonnées doit donc bien etre passé sous forme d'un tuple de deux entiers.
        """
        j, i = coord[0], coord[1]
        self._main[j,i] = valeur
        
    def __repr__(self):
        """Méthode modifiant l'affichage du type d'objet quand on l'entre dans l'interpréteur."""
        return "Niveau de {0} lignes et {1} colonnes.".format(self.haut, self.larg)
        
    def __str__(self):
        """Méthode effectuant l'affichage de la matrice quand passée en argument de print."""
        j, i = 0, 0
        chaine = str()
        while i<self.haut:
            while j<self.larg:
                chaine += str(self._main[j,i])
                j += 1
            if i != self.haut-1:
                chaine += '\n'
            j = 0
            i += 1
        return chaine
        
    def creuserNiveau(self):
        """Fonction "creusant" la matrice pour réaliser un labyrinthe. Un escalier descendant est placé sur la dernière case creusée, un escalier montant est placé sous l'emplacement (aléatoire au niveau 0, défini aux autres niveaux) du héros.
        """
        ### Insertion du premier chemin, en évitant la bordure
        if self.lvl == 0:
            j, i = randrange(self.larg-2)+1, randrange(self.haut-2)+1
        else:
            j, i = player.j, player.i
        self[j,i] = 1

        ### Creusage de la matrice jusqu'à un certain stade (TODO: Explication sur l'instanciation de compteur ?)
        compteur = (randrange(self.larg)+3*self.larg)*(randrange(self.haut)+3*self.haut)
        while compteur > 0:
            j, i = self.creuser(j, i)
            compteur -= 1
        self[j,i] = 2       # Placement de l'escalier descendant sur la dernière case creusée

        ### Placement de l'escalier descendant sous le joueur (lvl >= 1) ou du joueur aléatoire puis de l'escalier.
        if self.lvl == 0:
            while player.i == -1 and player.j == -1:      
                j, i = randrange(self.larg), randrange(self.haut)
                if self[j,i] == 1 and self[j,i-1] == 0 and self[j,i-1] == 0:
                    player.i, player.j = i, j
            self[j,i] = 3                     # Placement de l'escalier montant sous le joueur
        else:
            self[player.j,player.i] = 3

    def creuser(self, j, i):
        """Fonction ouvrant une nouvelle case vide adjacente à la case entrée en paramètre.
        Prends en arguments la colonne et la ligne.
        Renvoie les nouvelles positions j et i sous forme d'un tuple (j, i).
        """
        card = [ 'n', 'e', 's', 'w' ]      # 0 = nord, 1 = est, 2 = sud, 3 = ouest
        dir = card[randrange(4)]
        k, l = i, j
        if dir == 'n':
            k -= 1
        elif dir == 'e':
            l += 1
        elif dir == 's':
            k += 1
        elif dir == 'w':
            l -= 1
        if (k != 0 and l != 0 and k != self.haut-1 and l != self.larg-1):
            if (self[l,k] == 0 and self.compterVoisins(l, k) == 1) or self[l,k] == 1:
                self[l,k] = 1
                return (l,k)
            else:
                return (j,i)
        else:
            return (j,i)
            
    def compterVoisins(self, j, i):
        """Fonction comptant le nombre de cases vides directement adjacentes à une case j, i de la matrice principale.
        Prends en arguments la colonne et la ligne.
        Renvoie le nombre.
        """
        nb = 0
        try:
            if self[j,i+1] != 0:
                nb += 1
            if self[j,i-1] != 0:
                nb += 1
            if self[j+1,i] != 0:
                nb += 1
            if self[j-1,i] != 0:
                nb += 1
        except IndexError:
            nb = 2
        return nb

    def tracerProfil(self):
        """Fonction établissant le profil de la matrice principale, c'est à dire spécifiant pour chaque case lesquels de ses cases adjacentes sont des murs (les autres étant donc des chemins).
        """
        j, i = 0, 0
        while j<self.larg:
            while i<self.haut:
                try:
                    if self[j,i-1] == 0:        # La case nord est elle un mur ?
                        self.profil[j,i] += 'n-'
                except IndexError:
                    self.profil[j,i] += ''
                try:
                    if self[j+1,i] == 0:        # La case est est elle un mur ?
                        self.profil[j,i] += 'e-'
                except IndexError:
                    self.profil[j,i] += ''
                try:
                    if self[j,i+1] == 0:        # La case sud est elle un mur ?
                        self.profil[j,i] += 's-'
                except IndexError:
                    self.profil[j,i] += ''
                try:
                    if self[j-1,i] == 0:        # La case ouest est elle un mur ?
                        self.profil[j,i] += 'w-'
                except IndexError:
                    self.profil[j,i] += ''
                if len(self.profil[j,i]) != 0:
                    self.profil[j,i] = self.profil[j,i].rstrip('-')     # On supprime le '-' en trop
                else:
                    self.profil[j,i] += 'c'
                i += 1
            i = 0
            j += 1
            
    def afficher(self):
        """Fonction réalisant l'affichage du donjon avec les tiles Dark, c'est à dire hors du champ de vision du joueur mais déjà parcouru, et avec les tiles Brume pour les zones non explorées.
        Prend en arguments le niveau.
        """
        j, i, = 0, 0
        while j<self.larg:    # Affichage initial du donjon avec les tiles Dark (hors du champ de vision)
            while i<self.haut:
                if self.vues[j,i] == 1:
                    if self[j,i] == 0:
                        can.create_image((j+0.5)*case, (i+0.5)*case, image = imgMurDark[self.profil[j,i]])
                    elif self[j,i] != 0:
                        can.create_image((j+0.5)*case, (i+0.5)*case, image = imgCheminDark)
                    else:
                        print("Erreur dans l'affichage du donjon initial.")                        
                elif self.vues[j,i] == 0:
                    can.create_image((j+0.5)*case, (i+0.5)*case, image = imgBrume)
                else:
                    print("Erreur dans l'affichage du donjon initial.")
                i += 1
            i = 0
            j += 1

class Animate:
    """Classe modélisant quelque chose d'animé, pouvant notamment se déplacer.
    """
    type = 'animate'     # valeur par défaut
    
    def __init__(self, lvl, j, i):
        self.lvl = lvl
        self.j = j
        self.i = i
        self.image = ''
        self.race = ''
        
    def deplacer(self, dir, nb = 1):
        """Fonction déplaçant l'objet de nb cases dans la direction dir.
        """
        # TODO: Attaque ou redirection si destination est un animate
        if dir == 'n':
            if niv[self.lvl][self.j,self.i-1] != 0 and [self.j, self.i-1] not in (niv[self.lvl].monstrescoord or [player.j, player.i]):
                self.i -= 1
        if dir == 'e':
            if niv[self.lvl][self.j+1,self.i] != 0 and [self.j+1, self.i] not in (niv[self.lvl].monstrescoord or [player.j, player.i]):
                self.j += 1
        if dir == 's':
            if niv[self.lvl][self.j,self.i+1] != 0 and [self.j, self.i+1] not in (niv[self.lvl].monstrescoord or [player.j, player.i]):
                self.i += 1
        if dir == 'w':
            if niv[self.lvl][self.j-1,self.i] != 0 and [self.j-1, self.i] not in (niv[self.lvl].monstrescoord or [player.j, player.i]):
                self.j -= 1
    
    def distance(self, objet):
        return sqrt((objet.i-self.i)**2+(objet.j-self.j)**2)
    
class Joueur(Animate):
    """Classe modélisant un joueur.
    Comprend ses caractéristiques, son capacités, son inventaire/équipement,
    ainsi que différents modules rattachés au joueur.
    """
    type = 'joueur'

    def __init__(self):
        ### Position
        self.lvl = 0
        self.nivmax = 0
        self.j = -1
        self.i = -1
        self.vision = 3

        ### Identité
        self.race = 'nain'
        self.image = ''
        self.disp = 0       # Variant servant à stocker le retour de can.create_image pour déplacer l'image
        self.nom = 'Daedalus'
        
        ### Variables
        self.nbaff = 0

    def deplacer(self, dir, nb = 1):
        """Fonction déplaçant le joueur de nb cases dans la direction dir.
        """
        
        self.effacerVision()

        Animate.deplacer(self, dir, nb)
        self.image = PhotoImage(file = 'image/' + str(case) + '/' + self.type + '/' + self.race + '-' + dir +'.gif')
        
        if self.nbaff == maxaff:
            self.nbaff = 0
            can.delete(ALL)
            niv[self.lvl].afficher()
        self.afficherVision()
        self.nbaff += 1

        fintour()

    def deplacerN(self, event):
        self.deplacer('n')
    def deplacerE(self, event):
        self.deplacer('e')
    def deplacerS(self, event):
        self.deplacer('s')
    def deplacerW(self, event):
        self.deplacer('w')

    def doFov(self, x, y):
        """Fonction effectuant l'affichage du champ de vision du joueur.
        Adaptation du code proposé ici : http://roguebasin.roguelikedevelopment.org/index.php?title=Eligloscode
        """
        d = 0
        ox, oy = self.i+0.5, self.j+0.5
        
        while d<self.vision:
            j, i = int(oy), int(ox)
            niv[self.lvl].vues[j,i] = 1
            if niv[self.lvl][j,i] == 0:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgMur[niv[self.lvl].profil[j,i]])
            elif niv[self.lvl][j,i] == 1:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgChemin)
            elif niv[self.lvl][j,i] == 2:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgEscapeDown)
            elif niv[self.lvl][j,i] == 3:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgEscapeUp)
            if niv[self.lvl][j,i] == 0:
                return
            ## Si un monstre est présent sur cette case, on l'affiche, et on l'ajoute à la liste ennemis
            #if [j, i] in niv[self.lvl].monstrescoord:
                #can.create_image((j+0.5)*case, (i+0.5)*case, image = niv[self.lvl].monstres[niv[self.lvl].monstrescoord.index([j, i])].image)
            oy += y
            ox += x
            d += 1
    
    def undoFov(self, x, y):
        """Fonction effaçant le champ de vision précédant du joueur, avant un mouvement.
        Adapté à partir de la fonction doFov.
        """
        d = 0
        ox, oy = self.i+0.5, self.j+0.5
        while d<self.vision:
            j, i = int(oy), int(ox)
            if niv[self.lvl][j,i] == 0:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgMurDark[niv[self.lvl].profil[j,i]])
            elif niv[self.lvl][j,i] == 1:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgCheminDark)
            elif niv[self.lvl][j,i] == 2:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgCheminDark)
            elif niv[self.lvl][j,i] == 3:
                can.create_image((j+0.5)*case, (i+0.5)*case, image = imgCheminDark)
            if niv[self.lvl][j,i] == 0:
                return
            oy += y
            ox += x
            d += 1
            
    def effacerVision(self):
        ### On "efface" autour du joueur, sur son champ de vision
        x, y = 0, 0
        c = 0
        while c < 360:
            x = cos(c*0.01745)
            y = sin(c*0.01745)
            self.undoFov(x, y)
            c += 18     # L'incrément doit être assez petit pour parcourir toute la zone mais assez grand pour gagner de la vitesse de calcul. A optimiser en fonction de champ de vision du joueur.
    
    def afficherVision(self):
        """Fonction affichant le nouveau champ de vision, le précédent ayant été effacé dans la méthode self.deplacer.
        Prend en arguments la colonne j, la liste i, et le numéro du niveau où se trouve le joueur.
        """
                
        ### On affiche en lumineux ce qu'il peut voir
        
        x, y = 0, 0
        c = 0
        while c < 360:
            x = cos(c*0.01745)
            y = sin(c*0.01745)
            self.doFov(x, y)
            c += 18
    
        ### Affichage de la tile sous le joueur.
    
        if niv[self.lvl][self.j,self.i] == 1:
            can.create_image((self.j+0.5)*case, (self.i+0.5)*case, image = imgChemin)
        elif niv[self.lvl][self.j,self.i] == 2:
            can.create_image((self.j+0.5)*case, (self.i+0.5)*case, image = imgEscapeDown)
        elif niv[self.lvl][self.j,self.i] == 3:
            can.create_image((self.j+0.5)*case, (self.i+0.5)*case, image = imgEscapeUp)
        else:
            print("Erreur dans l'affichage de la tile sous le joueur.")
        
        ### Affichage du héros
        can.create_image((self.j+0.5)*case, (self.i+0.5)*case, image = self.image)

    def changerRace(self, race = 'Null'):
        """Change la race du joueur en lui donnant pour valeur soit l'argument 'race', soit l'élément suivant de la liste 'races'.
        """
        if race == 'Null':
            ind = races.index(self.race)
            if ind == len(races)-1:
                self.race = races[0]
                self.image = PhotoImage(file = 'image/' + str(case) + '/joueur/' + self.race + '-s.gif')
            else:
                self.race = races[ind + 1]
                self.image = PhotoImage(file = 'image/' + str(case) + '/joueur/' + self.race + '-s.gif')
        elif race in races:
            self.race = race
            self.image = PhotoImage(file = 'image/' + str(case) + '/joueur/' + self.race + '-s.gif')
        else:
            print("Erreur, cette race n'existe pas.")
        self.afficherVision()

    def actionEnter(self, event):
        if niv[self.lvl][self.j,self.i] == 2:
            self.niveauSuiv()
        elif niv[self.lvl][self.j,self.i] == 3:
            self.niveauPrec()

    def niveauPrec(self):
        """Réalise le passage au niveau précédent (supérieur) du donjon.
        """
        if self.lvl == 0:
            print("Vous quittez le donjon.")
            fen1.quit()
        else:
            self.lvl -= 1
            can.delete(ALL)
            niv[self.lvl].afficher()
            self.afficherVision()
    
    def niveauSuiv(self):
        """Réalise le passage au niveau suivant (inférieur) du donjon.
        """
        self.lvl += 1
        can.delete(ALL)
        if self.lvl > self.nivmax:
            self.nivmax += 1
            creerNiveau()
        else:
            niv[self.lvl].afficher()
            self.afficherVision()

class Monstre(Animate):
    """Classe modélisant un monstre.
    """
    type = 'monstre'
    
    def __init__(self, lvl, j, i, race = 'erreur'):
        self.lvl = lvl
        self.j = j
        self.i = i
        self.vision = 3
        self.race = race
        self.image = PhotoImage(file = 'image/' + str(case) + '/monstre/' + self.race + '.gif')
        self.disp = 0       # Variant servant à stocker le retour de can.create_image pour déplacer l'image


### --- Fonctions ---
### =================

### Création et gestion des Niveaux

def creerNiveau(larg = larg, haut = haut):
    """Fonction créant et affichant un niveau.
    """
    niv.append(Niveau(larg, haut))
    niv[player.lvl].afficher()
    player.afficherVision()

def fintour():
    for ind, monstre in enumerate(niv[player.lvl].monstres):
        hyp = monstre.distance(player)
        if hyp < monstre.vision:
            if player.i <= monstre.i:
                alpha = acos((player.j-monstre.j)/hyp)
                if alpha <= pi/4:                           # cadran E-NE
                    if niv[monstre.lvl][monstre.j+1, monstre.i] == 1:
                        monstre.j += 1
                    elif niv[monstre.lvl][monstre.j, monstre.i-1] == 1:
                        monstre.i -= 1
                elif alpha > pi/4 and alpha <= pi/2:        # cadran N-NE
                    if niv[monstre.lvl][monstre.j, monstre.i-1] == 1:
                        monstre.i -= 1
                    elif niv[monstre.lvl][monstre.j+1, monstre.i] == 1:
                        monstre.j += 1
                elif alpha > pi/2 and alpha <= 3*pi/4:      # cadran N-NW
                    if niv[monstre.lvl][monstre.j, monstre.i-1] == 1:
                        monstre.i -= 1
                    elif niv[monstre.lvl][monstre.j-1, monstre.i] == 1:
                        monstre.j -= 1
                elif alpha > 3*pi/4 and alpha <= pi:        # cadran W-NW
                    if niv[monstre.lvl][monstre.j-1, monstre.i] == 1:
                        monstre.j -= 1
                    elif niv[monstre.lvl][monstre.j, monstre.i-1] == 1:
                        monstre.i -= 1
                else:
                    print('Erreur dans le déplacement du monstre.')
            else:
                alpha = -acos((player.j-monstre.j)/hyp)
                if alpha >= -pi/4:                          # cadran E-SE
                    if niv[monstre.lvl][monstre.j+1, monstre.i] == 1:
                        monstre.j += 1
                    elif niv[monstre.lvl][monstre.j, monstre.i+1] == 1:
                        monstre.i += 1
                elif alpha < -pi/4 and alpha >= -pi/2:      # cadran S-SE
                    if niv[monstre.lvl][monstre.j, monstre.i+1] == 1:
                        monstre.i += 1
                    elif niv[monstre.lvl][monstre.j+1, monstre.i] == 1:
                        monstre.j += 1
                elif alpha < -pi/2 and alpha >= -3*pi/4:    # cadran S-SW
                    if niv[monstre.lvl][monstre.j, monstre.i+1] == 1:
                        monstre.i += 1
                    elif niv[monstre.lvl][monstre.j-1, monstre.i] == 1:
                        monstre.j -= 1
                elif alpha < -3*pi/4 and alpha >= -pi:      # cadran W-SW
                    if niv[monstre.lvl][monstre.j-1, monstre.i] == 1:
                        monstre.j -= 1
                    elif niv[monstre.lvl][monstre.j, monstre.i+1] == 1:
                        monstre.i += 1
                else:
                    print('Erreur dans le déplacement du monstre.')
            niv[player.lvl].monstrescoord[ind] = [monstre.j, monstre.i]
            can.create_image((monstre.j+0.5)*case, (monstre.i+0.5)*case, image = niv[player.lvl].monstres[ind].image)
        print(monstre.j, monstre.i, player.j, player.i)
        
            

### Gestion des combats

def rollDice(val = '1d6'):
    """Effectue le lancer de P dés à Q faces, les variables P et Q étant définies dans le string 'val',
    sous la forme PdQ. 'd' est le séparateur et est donc essentiel (type AD&D).
    Renvoie la somme des faces des P dés.
    """
    val.lower()
    try:
        [ nb, faces ] = val.split('d')
        nb, faces = int(nb), int(faces)
    except ValueError:
        print('La variable val doit être du type PdQ.')
        return 0
    i = 0
    res = 0
    while i<nb:
        res += randrange(faces)+1
        i += 1
    return res


### --- Corps principal ---
### =======================

print("Dwarf & Dungeon   Copyright (C) 2010  E. Lévêque & R. Verschelde")

### Création du GUI

### Choix (pour l'instant aléatoire) du type de terrain.
terrain = terrains[0]
player = Joueur()

fen1 = Tk()
fen1.title('Dwarf & Dungeon')
can = Canvas(fen1, width = case*larg, height = case*haut, bg='white')
can.bind_all("<Key-Up>", player.deplacerN)
can.bind_all("<Key-Right>", player.deplacerE)
can.bind_all("<Key-Down>", player.deplacerS)
can.bind_all("<Key-Left>", player.deplacerW)
can.bind_all("<Return>", player.actionEnter)
can.pack(side = TOP)

but1 = Button(text='Quitter', command = fen1.quit)
but1.pack(side = RIGHT)
but2 = Button(text='Changer de race', command = player.changerRace)
but2.pack(side = LEFT)

player.image = PhotoImage(file = 'image/' + str(case) + '/' + player.type + '/' + player.race + '-s.gif')

imgMur = {
    'n': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n.gif'),
    'n-e': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n-e.gif'),
    'n-s': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n-s.gif'),
    'n-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n-w.gif'),
    'n-e-s': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n-e-s.gif'),
    'n-e-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n-e-w.gif'),
    'n-s-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n-s-w.gif'),
    'n-e-s-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/n-e-s-w.gif'),
    'e': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/e.gif'),
    'e-s': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/e-s.gif'),
    'e-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/e-w.gif'),
    'e-s-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/e-s-w.gif'),
    's': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/s.gif'),
    's-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/s-w.gif'),
    'w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/w.gif'),
    'c': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/mur/c.gif'),
    }
imgMurDark = {
    'n': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n.gif'),
    'n-e': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n-e.gif'),
    'n-s': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n-s.gif'),
    'n-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n-w.gif'),
    'n-e-s': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n-e-s.gif'),
    'n-e-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n-e-w.gif'),
    'n-s-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n-s-w.gif'),
    'n-e-s-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/n-e-s-w.gif'),
    'e': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/e.gif'),
    'e-s': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/e-s.gif'),
    'e-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/e-w.gif'),
    'e-s-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/e-s-w.gif'),
    's': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/s.gif'),
    's-w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/s-w.gif'),
    'w': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/w.gif'),
    'c': PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/murDark/c.gif'),
    }
imgChemin = PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/chemin.gif')
imgCheminDark = PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/chemin-dark.gif')
imgEscapeDown = PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/escalier-desc.gif')
imgEscapeUp = PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/escalier-mont.gif')
imgBrume = PhotoImage(file = 'image/'+ str(case) +'/terrain/'+ terrain +'/brouillard.gif')

### Lancement du jeu au niveau 0
creerNiveau()


fen1.mainloop()
fen1.destroy()
