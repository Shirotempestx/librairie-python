from Partie2classDocument import Document , Auteur , Ebook , Livre
from LivreFiction import LivreFiction , Roman , BD , Nouvelle
from LivreReference import LivreReference , LivreScientifique , Encyclopedie
from Ebook import EbookSpecifique , EbookTexte 
from Documentelse import ManuelScolaire , Revue , Dictionnaire
from datetime import datetime , date 
import re



class ListeAuteurs:
    def __init__(self):
        self._auteurs = []
        
    @property
    def auteurs(self):  
        return self._auteurs
    
    def ajouterAuteur(self, auteur):
        if not any(a.email == auteur.email for a in self._auteurs):
            self._auteurs.append(auteur)

    def ajouterAuteurs(self, auteurs):
        try:
            if isinstance(auteurs, list):
                auteurs_centent = all(isinstance(a, Auteur) for a in auteurs)
                if auteurs_centent :
                    self._auteurs += auteurs
                    print("l'etat d'ajout les auteurs: succes !!")
                else :
                    raise Exception("Le content d'objet passé n'est pas des Auteurs")
            else :
                raise Exception("L'objet passé n'est pas un Liste")
        except Exception as e:
            print(f"Erreur ajouter auteurs: {e}")
        
    def RechercherAuteur(self, nom):
        indice = -1
        for auteur in self._auteurs:
            if auteur.nom == nom :
                indice = self._auteurs.index(auteur)
                return (indice , auteur)
        return (indice,"n'exist pas")

    def RechercherAuteurs(self, nom):
        
            result =  [(self._auteurs.index(auteur),auteur) for auteur in self.auteurs if auteur.nom == nom ]
            print("Done!!")
            return result

    
    def AuteursFemmes(self):
        return  [(self._auteurs.index(auteur),auteur) for auteur in self.auteurs if auteur.sexe.lower() == "f"]

    def PourcentageAuteursFemmes(self):
        return (len(self.AuteursFemmes()*100))/len(self._auteurs) if len(self._auteurs)!=0 else 0
    
    def ModifierAuteur(self, auteur):
        cherche_result = self.RechercherAuteur(auteur.nom)
        if cherche_result[0] == -1 :
            return "l'auteur n'exist pas"
        while True:
            choix = int(input("menu modifier un auteure:\n 1. modifie nom.\n 2. modifier email.\n 3. modifie sexe.\n 4. quite la menu."))
            if choix == 1: 
                auteur.nom = input("saisir la Nouveau nom ")
            elif choix  == 2 :
                auteur.nom = input("saisir la Nouveau email ")            
            elif choix  == 3 :
                auteur.nom = input("saisir la Nouveau sexe ")
            elif choix  == 4:
                break
            else :
                print("1<=x<=4")
        return "done!!"

    def TrierAuteurs(self):
        self._auteurs.sort(key=lambda a: a.nom)
        
    def InverserTriAuteurs(self):
        self._auteurs.sort(key=lambda a: a.nom , reverse=True)
    
    def SupprimerAuteur(self, nom):
        result = self.RechercherAuteurs(nom)
        # i = 0
        # for tuple in result :
        #     self._auteurs.pop(tuple[0]-i)
        #     i += 1
        for tuple in result :
            self._auteurs.remove(tuple[1]) if tuple[0] != -1 else None
        
    def getNombreAuteurs(self):
        return len(self._auteurs)
    
    def __str__(self):
        return '\n'.join(str(auteur) for auteur in self._auteurs)
                
        
        
        
        
        
        