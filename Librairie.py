from Partie2classDocument import Document , Auteur , Ebook , Livre
from LivreFiction import LivreFiction , Roman , BD , Nouvelle
from LivreReference import LivreReference , LivreScientifique , Encyclopedie
from Ebook import EbookSpecifique , EbookTexte 
from Documentelse import ManuelScolaire , Revue , Dictionnaire
from datetime import datetime , date 
import re
from exeptions import *
from ListeAuteurs import *
from ListeDocuments import *


class  Librairie:
    def __init__(self, listeAuteurs=ListeAuteurs(), listeDocuments=ListeDocuments()):
        try :
            if isinstance(listeAuteurs,ListeAuteurs) :
                self._listeAuteurs = listeAuteurs 
                self._listeDocuments = listeDocuments
            else :
                raise TypeError("la 1er propriete doit etre un objet 'ListeAuteurs'")
        except ListeObjetsExeption as e :
            print(e)
            
        try :
            if isinstance(listeDocuments,ListeDocuments) :
                self._listeDocuments = listeDocuments
            else :
                raise TypeError("la 2em propriete doit etre un objet 'ListeDocuments'")
        except TypeError as e :
            print(e)
        
    @property
    def listeAuteurs(self):
        return self._listeAuteurs
    @listeAuteurs.setter
    def listeAuteurs(self, new_listeAuteurs):
        try :
            if isinstance(new_listeAuteurs,ListeAuteurs)  :
                self._listeAuteurs = new_listeAuteurs 
            else :
                raise TypeError("la propriete listeAuteurs doit etre un objet 'ListeDocuments'")
        except TypeError as e :
            print(e) 
        
    @property
    def listeDocuments(self):
        return self._listeDocuments
    @listeDocuments.setter
    def listeDocuments(self, new_listeDocuments):
        try :
            if isinstance(new_listeDocuments,list)  :
                self._listeAuteurs = new_listeDocuments 
            else :
                raise TypeError("la propriete listeDocuments doit etre un objet 'ListeDocuments'")
        except TypeError as e :
            print(e)         
            
    def AjouterEntree(self,document,auteur):
        try :
            if isinstance(document,Document) :
                self._listeDocuments.AjouterDocument(document) 
            else :
                raise TypeError("Le paramètre document doit être une objet Document")
        except TypeError as e :
            print(e)
        
        try :
            if isinstance(auteur,Auteur) :
                if self._listeAuteurs.RechercherAuteur(auteur.nom)[0] != -1 : 
                    # la method RechercherAuteur() returne un tuple (indice,auteur)
                    self._listeAuteurs.ajouterAuteur(auteur) 
                    print("l'ajout d'un auteur est confirmer ")
                else :
                    print("l'auteur exist deja!!")
            else :
                    raise TypeError("Le paramètre Auteurs doit être une objet Auteur")
        except TypeError as e :
            print(e)
            
    def AjouterEntrees(self,documents,auteurs):
        try :
            if isinstance(documents, ListeDocuments):
                self._listeDocuments += documents 
                # la class listeDocuments ayon la methode __add__
            else :
                raise TypeError("Le paramètre liste documents doit être une objet de type 'ListeDocuments'")
        except TypeError as e:
            print(e)
        
        # for document in documents:
        #     try :
        #         if not isinstance(document, Document):
        #             raise TypeError(f"Élément invalide dans 'documents': {str(document)} " )
        #         self._listeDocuments.append(document)
        #     except TypeError as e :
        #         print(e)

        try :
            if isinstance(auteurs, ListeAuteurs):
                self._listeAuteurs += auteurs.auteurs
                # la class listeAuteurs ayan une acceceur getter 
            else :
                raise TypeError("Le paramètre liste auteurs doit être une objet de type 'ListeAuteurs'")
        except TypeError as e:
            print(e)

        # for auteur in auteurs:
        #     try :
        #         if not isinstance(auteur, Auteur):
        #             raise TypeError(f"Élément invalide dans 'auteurs': {str(auteur)}"  )
        #         if auteur not in self._listeAuteurs:
        #             self._listeAuteurs.append(auteur)
        #     except TypeError as e :
        #         print(e)

        print("Entrées ajoutées avec succès !")

        # try :
        #     if isinstance(documents,list) :
        #         any( self._listeDocuments.append(document) 
        #             for document in documents 
        #                 if isinstance(document,Document) )
        #     else :
        #         raise ListeObjetsExeption("Le paramètre documents doit être une liste des Documents")
        # except ListeObjetsExeption as e :
        #     print(e)
        

        # try :
        #     if isinstance(auteurs,list) :
        #         any( self._listeAuteurs.append(auteur) 
        #             for auteur in auteurs
        #                 if isinstance(auteur,Auteur) and auteur not in self._listeAuteurs  )
        #     else :
        #         raise ListeObjetsExeption("Le paramètre auteurs doit être une liste des objets Auteur")
        # except ListeObjetsExeption as e :
        #     print(e)
    
    def SupprimerAuteur(self,nom):
        self._listeAuteurs.SupprimerAuteur(nom)
        
    def DocumentsParAuteurs(self):
        return [(auteur,len(self._listeDocuments.rechercherParAuteur(auteur.nom))) for auteur in self._listeAuteurs.auteurs]
    
    def TrierAuteursParDocuments(self):
        try:
            self._listeAuteurs.auteurs.sort(
                key=lambda auteur: len(self._listeDocuments.rechercherParAuteur(auteur.nom)),
                reverse=True
            )
        except Exception as e:
            print(f"Erreur trier auteurs par documents: {e}")

    
