from Partie2classDocument import Document , Auteur , Ebook
import datetime
# Document (abstract)
# ├── Livre   (abstract)
# │   ├── LivreFiction  (abstract)
# │   │   ├── Roman
# │   │   ├── Nouvelle
# │   │   └── BD
# │   └── LivreReference (abstract)
# │       ├── LivreScientifique
# │       └── Encyclopedie
# ├── Ebook   (abstract)
# │   ├── EbookTexte                ******
# │   └── EbookSpecifique           ******
# ├── ManuelScolaire
# ├── Revue
# └── Dictionnaire


class EbookTexte(Ebook):
    def __init__(self, titre="", nomAuteur=..., prix=0, quantite_en_stock=None, taille_octets=0):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, taille_octets)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, taille_octets)
        self._nb_caracter = taille_octets/8
        
    @property
    def nb_caracter(self):
        return self._nb_caracter
    @nb_caracter.setter
    def nb_caracter(self,new_taille_octets=None):
        self.taille_octets = int(input("modifier taille octets premierment")) if new_taille_octets is None else  self.new_taille_octets == new_taille_octets
        self._nb_caracter = self.taille_octets/8
        
    def getprix(self):
        return super().prix * 0.5 # reduction de 50%
    
    def __eq__(self, objet):
        return isinstance(objet,EbookTexte) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._nb_caracter == objet.nb_caracter

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])
        
        string = f"bookTexte: « {super().titre}  de {auteurs} taille octets est {super().taille_octets}  , nomber de caractères: {self._nb_caracter}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string

class EbookSpecifique(Ebook):
    def __init__(self, titre="", nomAuteur=..., prix=0, quantite_en_stock=None, taille_octets=0, format="", logiciel=""):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, taille_octets)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, taille_octets)
        self._format = format
        self._logiciel = logiciel
    
    @property
    def format(self):
        return self._format
    @format.setter
    def format(self,new_format):
        self._format = new_format
    
    @property
    def logiciel(self):
        return self._logiciel
    @logiciel.setter
    def logiciel(self,new_logiciel):
        self._logiciel = new_logiciel
    
    
    def getprix(self):
        return super().prix  # reduction de 0%
    
    def __eq__(self, objet):
        return isinstance(objet,EbookSpecifique) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._nb_caracter == objet.nb_caracter

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])


        string = f"EbookSpecifique: « {super().titre}  de {auteurs} taille octets est {super().taille_octets} , de format : {self._format} qui affiche par : {self._logiciel}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string

# *************************************************************************************
