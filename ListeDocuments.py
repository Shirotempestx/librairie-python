from Partie2classDocument import Document , Auteur , Ebook , Livre
from LivreFiction import LivreFiction , Roman , BD , Nouvelle
from LivreReference import LivreReference , LivreScientifique , Encyclopedie
from Ebook import EbookSpecifique , EbookTexte 
from Documentelse import ManuelScolaire , Revue , Dictionnaire
from datetime import datetime , date 
import re

class ListeDocuments:
    def __init__(self):
        self._documents = []
        
    def AjouterDocument(self, document):
        self._documents.append(document)
    
    def AjouterDocuments(self,documents):
        try:
            if isinstance(documents, list):
                    self._documents += documents
                    print("l'etat d'ajout les documents: succes !!")
            else :
                raise Exception("L'objet passé n'est pas un Liste")
        except Exception as e:
            print(f"Erreur ajouter documents: {e}")
            
    @property
    def documents(self):
        return self._documents
    
    def RechercherParNumero(self,numero):
        indice = -1
        for document in self._documents:
            if document.numero == numero :
                indice = self._documents.index(document)
                return (indice , document)
        return (indice,None)

    def rechercherParTitre(self, titre):
        indice = -1
        for document in self._documents:
            if document.titre == titre :
                indice = self._documents.index(document)
                return (indice , document)
        return (indice,"")
    
    def rechercherParAuteur(self, nom):
            result =  [(self._documents.index(document) ,document) for document in self._documents 
                       if any(auteur.nom == nom 
                              for auteur in document.nomAuteur
                              )]
            print("Done!!" if result!=[] else "no document fund!!")
            return result
        
    def SupprimerParNumero(self,numero):
        document = self.RechercherParNumero(numero)
        self._documents.remove(document[1]) if document[0] != -1 else None
        
    def SupprimerParTitre(self,titre):
        while True:
            document = self.rechercherParTitre(titre)
            if document[0] == -1 :
                break
            self._documents.remove(document[1]) 
        
    def SupprimerParAuteur(self,nom):
        documents = self.rechercherParAuteur(nom)
        # i = 0
        # for document in documents :
        #     self._documents.pop(document[0]-i) if document[0] != -1 else None
        #     i += 1
        for document in documents :
            self._documents.remove(document[1]) if document[0] != -1 else None
        
    def getNombreDocuments(self):
        return len(self._documents)
    
    # les 10 methodes
    
    def EbooksTexte(self):
        return [str(document) for document in self._documents if isinstance(document,EbookTexte)]

    def EbooksSpecifiques(self):
        return [str(document) for document in self._documents if isinstance(document,EbookSpecifique)]

    def Romans(self):
        return [str(document) for document in self._documents if isinstance(document,Roman)]

    def Nouvelles(self):
        return [str(document) for document in self._documents if isinstance(document,Nouvelle)]

    def BDs(self):
        return [str(document) for document in self._documents if isinstance(document,BD)]

    def LivresScientifiques(self):
        return [str(document) for document in self._documents if isinstance(document,LivreScientifique)]

    def Encyclopedies(self):
        return [str(document) for document in self._documents if isinstance(document,Encyclopedie)]

    def ManuelsScolaires(self):
        return [str(document) for document in self._documents if isinstance(document,ManuelScolaire)]

    def Revues(self):
        return [str(document) for document in self._documents if isinstance(document,Revue)]

    def Dictionnaires(self):
        return [str(document) for document in self._documents if isinstance(document,Dictionnaire)]
            
    #  FIN
    
    def RuptureStock(self):
        return [document for document in self._documents if document.quantite_en_stock == 0]
    
    def TrierParTitre(self):
        self._documents.sort(key=lambda d: d.titre)
    
    def InverserTrierParTitre(self):
        self._documents.sort(key=lambda d: d.titre , reverse=True)
    
    def TrierParQuantite(self):
        self._documents.sort(key=lambda d: d.quantite_en_stock )
    
    def TrierParPrix(self):
        self._documents.sort(key=lambda d: d.prix , reverse=True )
        
    def __str__(self):
        return "Liste des documents : \n"+'\n'.join(str(d) for d in self._documents)
    
    def __add__(self,listeDocuments):
        try:
            if isinstance(listeDocuments, ListeDocuments):
                    self._documents += listeDocuments.documents
                    print("l'etat d'ajout les documents: succes !!")
            else :
                raise TypeError("L'objet passé n'est pas un objet de type ListeDocuments")
        except TypeError as e:
            print(f"Erreur ajouter documents: {e}")