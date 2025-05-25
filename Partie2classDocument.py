from abc import ABC , abstractmethod
from exeptions import *
import re

class Auteur :
    def __init__(self , nom = "" , email = "" , sexe = "" ):
        self._nom = nom 
        try:
            if re.match(r"\w+@\w+.\w+",email) :
                self._email = email 
            else :
                raise ValueError()
        except ValueError as e:
            print(e,"l'email doit etre comme ca lib@domain.com ")
        try :
            if sexe.lower() == "m" or sexe.lower() == "f" :
                self._sexe = sexe
            else :
                raise SexeExeption()
        except SexeExeption as e:
            print(e)
    
    @property
    def nom(self):
        return self._nom
    @nom.setter
    def nom(self, new_nom):
        self._nom = new_nom
        
    @property 
    def sexe(self):
        return self._sexe
    @sexe.setter
    def sexe(self, new_sexe):
        self._sexe = new_sexe
    
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self , new_email):
        self._email = new_email
    
    def __eq__(self, auteur):
        return isinstance(auteur,Auteur ) and self._email == auteur.email
    
    def __str__(self):
        return f"« {self._nom} ({self._sexe}) à {self._email} »."
    
class Document(ABC) :
    _compteur = 1
    def __init__(self , titre = "" , nomAuteur = [] , prix = 0.0 , quantite_en_stock = None):
        self._numero = Document._compteur
        self._titre = titre
        if isinstance(nomAuteur,list):
            self._nomAuteur = nomAuteur
        else :
            self._nomAuteur = [nomAuteur]
        self._prix = prix
        # if quantite_en_stock is not None :
        self._quantite_en_stock = quantite_en_stock 
        Document._compteur = Document._compteur + 1
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def titre(self):
        return self._titre
    
    @property
    def nomAuteur(self):
        return self._nomAuteur
    
    @property
    def prix(self):
        return self._prix
    @prix.setter
    def prix(self,new_prix):
        self._prix = new_prix
    
    @property
    def quantite_en_stock(self):
        return self._quantite_en_stock 
    @quantite_en_stock.setter
    def quantite_en_stock(self,new_quantite_en_stock):
        self._quantite_en_stock = new_quantite_en_stock
    
    @abstractmethod
    def __eq__(self, value):
        pass
    
    @abstractmethod
    def __str__(self):
        
        pass
        
    @abstractmethod
    def getprix(self):
        pass
    
class Livre(Document) :
    def __init__(self , titre = "" , nomAuteur = [] , prix = 0.0 , quantite_en_stock = None , nbpages = 0):
        super().__init__(titre,nomAuteur,prix,quantite_en_stock)
        self._nbpages = nbpages
    
    @property
    def nbpages(self):
        return self._nbpages
    @nbpages.setter
    def nbpages(self,new_nbpages):
        self._nbpages = new_nbpages
        
    # return isinstance(livre,Livre) and self._titre == livre.titre and self._nomAuteur == livre._nomAuteur
        
class Ebook(Document):
    def __init__(self , titre = "" , nomAuteur = [] , prix = 0.0 , quantite_en_stock = None , taille_octets = 0):
        super().__init__(titre,nomAuteur,prix,quantite_en_stock)
        self._taille_octets = taille_octets
    
    @property
    def taille_octets(self):
        return self._taille_octets
    @taille_octets.setter
    def taille_octets(self,new_taille_octets):
        self._taille_octets = new_taille_octets
        


    