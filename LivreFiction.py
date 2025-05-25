from Partie2classDocument import Document , Auteur , Livre , Ebook
import datetime
# Document (abstract)
# ├── Livre   (abstract)
# │   ├── LivreFiction  (abstract)
# │   │   ├── Roman             ******
# │   │   ├── Nouvelle          ******
# │   │   └── BD                ******
# │   └── LivreReference (abstract)
# │       ├── LivreScientifique
# │       └── Encyclopedie
# ├── Ebook   (abstract)
# │   ├── EbookTexte
# │   └── EbookSpecifique
# ├── ManuelScolaire
# ├── Revue
# └── Dictionnaire

# *************************************************************************************
class LivreFiction(Livre):
    def __init__(self , titre = "" , nomAuteur = [] , prix = 0.0 , quantite_en_stock = None , nbpages = 0 , categorie = ""):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, nbpages)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, nbpages)
        # if categorie in ["enfant", "jeune", "adulte"]:
        #     self._categorie = categorie
        # else :
        #     while categorie not in ["enfant", "jeune", "adulte"]:
        #         categorie = input("categorie wrrong")
        self._categorie = categorie

    
    @property
    def categorie(self):
        return self._categorie
    @categorie.setter
    def categorie(self,new_categorie):
        # if new_categorie in ["enfant", "jeune", "adulte"]:
        #     self._categorie = new_categorie
        # else :
        #     while new_categorie not in ["enfant", "jeune", "adulte"]:
        #         new_categorie = input("categorie wrrong")
            self._categorie = new_categorie
        
class Roman(LivreFiction):
    def __init__(self, titre="", nomAuteur=[], prix=0, quantite_en_stock=None, nbpages=0, categorie="", genre=""):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, nbpages, categorie)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, nbpages, categorie)  
        self._genre = genre
    
    @property
    def genre(self):
        return self._genre
    @genre.setter
    def genre(self,new_genre):
        self._genre = new_genre
        
    def getprix(self):
        return super().prix*0.75 # réduction  de 25%
    
    def __eq__(self, objet):
        return isinstance(objet,Roman) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._genre == objet.genre

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])

        string = f"Roman « {super().titre}  de {auteurs} nomber de pages est {super().nbpages} , category: {super().categorie} , genre: {self._genre}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string

class Nouvelle(LivreFiction):
    def __init__(self, titre="", nomAuteur=[], prix=0, quantite_en_stock=None, nbpages=0, categorie="", theme=""):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, nbpages, categorie)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, nbpages, categorie)
        self._theme = theme
        
    @property
    def theme(self):
        return self._theme
    @theme.setter
    def theme(self,new_theme):
        self._theme = new_theme
        
    def getprix(self):
        return super().prix * 0.7 # réduction  de 30%
    
    def __eq__(self, objet):
        return isinstance(objet,Nouvelle) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._theme == objet.theme

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])

        string = f"Nouvelle « {super().titre}  de {auteurs} nomber de pages est {super().nbpages} , category: {super().categorie} , théme: {self._theme}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string

class BD(LivreFiction):
    def __init__(self, titre="", nomAuteur=[], prix=0, quantite_en_stock=None, nbpages=0, categorie="", editeur=""):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, nbpages, categorie)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, nbpages, categorie)
        self._editeur = editeur
        
    @property
    def editeur(self):
        return self._editeur
    @editeur.setter
    def editeur(self,new_editeur):
        self._editeur = new_editeur
        
    def getprix(self):
        return super().prix * 0.9 # réduction  de 10%
    
    def __eq__(self, objet):
        return isinstance(objet,BD) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._editeur == objet.editeur

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])


        string = f"BD: « {super().titre}  de {auteurs} nomber de pages est {super().nbpages} , category: {super().categorie} , éditeur: {self._editeur}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string
# *