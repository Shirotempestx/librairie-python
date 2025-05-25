from Partie2classDocument import Document , Auteur , Livre 
import datetime
# Document (abstract)
# ├── Livre   (abstract)
# │   ├── LivreFiction  (abstract)
# │   │   ├── Roman
# │   │   ├── Nouvelle
# │   │   └── BD
# │   └── LivreReference (abstract)
# │       ├── LivreScientifique         ******
# │       └── Encyclopedie              ******
# ├── Ebook   (abstract)
# │   ├── EbookTexte
# │   └── EbookSpecifique
# ├── ManuelScolaire
# ├── Revue
# └── Dictionnaire



class LivreReference(Livre):
    def __init__(self , titre = "" , nomAuteur = [] , prix = 0.0 , quantite_en_stock = None , nbpages = 0 , domaine = ""):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, nbpages)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, nbpages)
        self._domaine = domaine
        
    
    @property
    def domaine(self):
        return self._domaine
    @domaine.setter
    def domaine(self,new_domaine):
        self._domaine = new_domaine
        
class LivreScientifique(LivreReference):
    def __init__(self, titre="", nomAuteur=[], prix=0, quantite_en_stock=None, nbpages=0, domaine="", champ_etude=""):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, nbpages, domaine)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, nbpages, domaine)
        self._champ_etude = champ_etude
        
    @property
    def champ_etude(self):
        return self._champ_etude
    @champ_etude.setter
    def champ_etude(self,new_champ_etude):
        self._champ_etude = new_champ_etude
        
    def getprix(self):
        return super().prix * 0.65 # réduction  de 35%
    
    def __eq__(self, objet):
        return isinstance(objet,LivreScientifique) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._champ_etude == objet.champ_etude

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])


        string = f"LivreScientifique: « {super().titre}  de {auteurs} nomber de pages est {super().nbpages} , domaine: {super().domaine} , champ d'étude: {self._champ_etude}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string
    
class Encyclopedie(LivreReference):
    def __init__(self, titre="", nomAuteur=[], prix=0, quantite_en_stock=None, nbpages=0, domaine="", nb_tome=0):
        if not isinstance(nomAuteur,Auteur):
            super().__init__(titre, nomAuteur, prix, quantite_en_stock, nbpages, domaine)
        else :
            super().__init__(titre, [nomAuteur], prix, quantite_en_stock, nbpages, domaine)
        self._nb_tome = nb_tome
        
    @property
    def nb_tome(self):
        return self._nb_tome
    @nb_tome.setter
    def nb_tome(self,new_nb_tome):
        self._nb_tome = new_nb_tome
        
    def getprix(self):
        return super().prix * 0.6 # réduction  de 40%
    
    def __eq__(self, objet):
        return isinstance(objet,LivreScientifique) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._nb_tome == objet.nb_tome

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])


        string = f"Encyclopedie: « {super().titre}  de {auteurs} nomber de pages est {super().nbpages} , domaine: {super().domaine} , nomber du tomes: {self._nb_tome}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string
# *************************************************************************************
