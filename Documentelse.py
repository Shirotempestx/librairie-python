from Partie2classDocument import Document , Auteur 
from datetime import datetime , date 
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
# │   ├── EbookTexte
# │   └── EbookSpecifique
# ├── ManuelScolaire                ******
# ├── Revue                         ******
# └── Dictionnaire                  ******


class ManuelScolaire(Document):
    def __init__(self, titre="", nomAuteur=..., prix=0, quantite_en_stock=None,niveau_filier=""):
        super().__init__(titre, nomAuteur, prix, quantite_en_stock)    
        self._niveau_filier = niveau_filier
        
    @property
    def niveau_filier(self):
        return self._niveau_filier
    @niveau_filier.setter
    def niveau_filier(self,new_niveau_filier):
        self._niveau_filier = new_niveau_filier
    
    
    def getprix(self):
        return super().prix  # reduction de 0%
    
    def __eq__(self, objet):
        return isinstance(objet,ManuelScolaire) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._nb_caracter == objet.nb_caracter

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])


        string = f"ManuelScolaire: « {super().titre}  de {auteurs}, niveau scolaire && filier : {self._niveau_filier}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string

class Revue(Document):
    def __init__(self, titre="", nomAuteur=..., prix=0, quantite_en_stock=None, date_chain=""):
        super().__init__(titre, nomAuteur, prix, quantite_en_stock)
        try:
            # Vérifier que la date est au format YYYY-MM-DD
            self._date = datetime.strptime(date_chain, "%Y-%m-%d").date()
        except ValueError as e:
            print(f"Format de date invalide pour Revue: {date_chain}. Utilisez YYYY-MM-DD.")


    @property
    def date(self):
        return self._date
    @date.setter
    def date(self,new_date):
        self._date = new_date
    
    
    def getprix(self):
        return super().prix  # reduction de 0%
    
    def __eq__(self, objet):
        return isinstance(objet,Revue) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._nb_caracter == objet.nb_caracter

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])


        string = f"Revue: « {super().titre}  de {auteurs}  , date : {self._date}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string


class Dictionnaire(Document):
    def __init__(self, titre="", nomAuteur=..., prix=0, quantite_en_stock=None, langue="eng"):
        super().__init__(titre, nomAuteur, prix, quantite_en_stock)
        self._langue = langue
        
    @property
    def langue(self):
        return self._langue
    @langue.setter
    def langue(self,new_langue):
        self._langue = new_langue
    
    
    def getprix(self):
        return super().prix *0.85  # reduction de 15%
    
    def __eq__(self, objet):
        return isinstance(objet,Dictionnaire) and super().titre == objet.titre and super().nomAuteur == objet.nomAuteur and self._nb_caracter == objet.nb_caracter

    def __str__(self):
        auteurs = ' et '.join([a.nom for a in self.nomAuteur])


        string = f"Dictionnaire: « {super().titre}  de {auteurs}  , de langue : {self._langue}, coûte {super().prix} DH "  
        string += f"avec {super().quantite_en_stock} exemplaires en stock. »" if super().quantite_en_stock is not None else None
        return string

