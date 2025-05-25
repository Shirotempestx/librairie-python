import tkinter as tk
from tkinter import ttk, messagebox
from Librairie import *
from ListeAuteurs import *
from ListeDocuments import *
from Partie2classDocument import Document, Auteur
from LivreFiction import Roman, Nouvelle, BD
from LivreReference import LivreScientifique, Encyclopedie
from Ebook import EbookTexte, EbookSpecifique
from Documentelse import ManuelScolaire, Revue, Dictionnaire
import csv
import os
import re

class LibrairieGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Bibliothèque")
        self.root.geometry("1500x750")
        
        self.session_saved = False
        self.librairie = Librairie()
        self.notebook = ttk.Notebook(root) # Création du notebook pour les onglets
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        self.create_auteurs_tab()
        self.create_documents_tab()
        self.create_search_tab()
        self.create_statistics_tab()
        
        session_frame = ttk.Frame(self.root)
        session_frame.pack(side='bottom', pady=15)
        ttk.Button(session_frame, text="Enregistrer la session (CSV)", command=self.save_session_csv).pack(side='left', padx=20)
        ttk.Button(session_frame, text="Restaurer la session (CSV)", command=self.load_session_csv).pack(side='left', padx=20)
        
        self.root.after(500, self.session_restore_reminder)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_auteurs_tab(self):
        auteurs_frame = ttk.Frame(self.notebook)
        self.notebook.add(auteurs_frame, text="Gestion des Auteurs")
        
        add_frame = ttk.LabelFrame(auteurs_frame, text="Ajouter un Auteur")
        add_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(add_frame, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        self.nom_entry = ttk.Entry(add_frame)
        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(add_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Genre:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_var = tk.StringVar(value='m')
        ttk.Radiobutton(add_frame, text="Homme", variable=self.genre_var, value='m').grid(row=2, column=1)
        ttk.Radiobutton(add_frame, text="Femme", variable=self.genre_var, value='f').grid(row=2, column=2)
        
        ttk.Button(add_frame, text="Ajouter Auteur", command=self.add_auteur).grid(row=3, column=0, columnspan=3, pady=10)
        
        list_frame = ttk.LabelFrame(auteurs_frame, text="Liste des Auteurs")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.auteurs_tree = ttk.Treeview(list_frame, columns=('nom', 'email', 'genre'), show='headings')
        self.auteurs_tree.heading('nom', text='Nom')
        self.auteurs_tree.heading('email', text='Email')
        self.auteurs_tree.heading('genre', text='Genre')
        self.auteurs_tree.pack(fill='both', expand=True)
        
        control_frame = ttk.Frame(auteurs_frame)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(control_frame, text="Actualiser", command=self.refresh_auteurs).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Supprimer", command=self.delete_auteur).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Trier ↑", command=self.sort_auteurs_asc).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Trier ↓", command=self.sort_auteurs_desc).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Auteurs Femmes", command=self.show_female_authors).pack(side='left', padx=5)
        
    def create_documents_tab(self):
        documents_frame = ttk.Frame(self.notebook)
        self.notebook.add(documents_frame, text="Gestion des Documents")
        
        add_frame = ttk.LabelFrame(documents_frame, text="Ajouter un Document")
        add_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(add_frame, text="Type de Document:").grid(row=0, column=0, padx=5, pady=5)
        self.doc_type = ttk.Combobox(add_frame, values=[
            'Roman', 'Nouvelle', 'BD', 'Livre Scientifique', 
            'Encyclopédie', 'E-book Texte', 'E-book Spécifique',
            'Manuel Scolaire', 'Revue', 'Dictionnaire'
        ])
        self.doc_type.grid(row=0, column=1, padx=5, pady=5)
        self.doc_type.bind('<<ComboboxSelected>>', self.update_document_fields)
        
        ttk.Label(add_frame, text="Auteurs:").grid(row=1, column=2, padx=5, pady=5)
        self.auteurs_listbox = tk.Listbox(add_frame, selectmode='multiple', exportselection=0, height=5)
        self.auteurs_listbox.grid(row=2, column=2, rowspan=4, padx=5, pady=5)
        self.refresh_auteurs_listbox()
        
        self.create_document_fields(add_frame)
        
        ttk.Button(add_frame, text="Ajouter Document", command=self.add_document).grid(row=10, column=0, columnspan=2, pady=10)
        
        list_frame = ttk.LabelFrame(documents_frame, text="Liste des Documents")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.documents_tree = ttk.Treeview(list_frame, columns=('numero', 'titre', 'auteurs', 'type', 'prix', 'quantite'), show='headings')
        self.documents_tree.heading('numero', text='Numéro')
        self.documents_tree.heading('titre', text='Titre')
        self.documents_tree.heading('auteurs', text='Auteurs')
        self.documents_tree.heading('type', text='Type')
        self.documents_tree.heading('prix', text='Prix')
        self.documents_tree.heading('quantite', text='Quantité')
        self.documents_tree.pack(fill='both', expand=True)
        
        control_frame = ttk.Frame(documents_frame)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(control_frame, text="Actualiser", command=self.refresh_documents).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Supprimer", command=self.delete_document).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Trier par Titre", command=self.sort_documents_title).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Trier par Prix", command=self.sort_documents_price).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Rupture Stock", command=self.show_out_of_stock).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Afficher Infos", command=self.show_selected_document_info).pack(side='left', padx=5)
        
    def create_search_tab(self):
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Recherche")
        
        search_input_frame = ttk.LabelFrame(search_frame, text="Recherche")
        search_input_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(search_input_frame, text="Mot-clé:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_input_frame)
        self.search_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        ttk.Button(search_input_frame, text="Rechercher", command=self.search).pack(side='left', padx=5)
        
        results_frame = ttk.LabelFrame(search_frame, text="Résultats")
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.search_tree = ttk.Treeview(results_frame, columns=('type', 'details'), show='headings')
        self.search_tree.heading('type', text='Type')
        self.search_tree.heading('details', text='Détails')
        self.search_tree.pack(fill='both', expand=True)
        
    def create_statistics_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistiques")
        

        auteurs_frame = ttk.LabelFrame(stats_frame, text="Statistiques des Auteurs")
        auteurs_frame.pack(fill='x', padx=5, pady=5)
        
        self.auteurs_stats = ttk.Label(auteurs_frame, text="")
        self.auteurs_stats.pack(padx=5, pady=5)
        
        ttk.Button(auteurs_frame, text="Actualiser", command=self.update_authors_stats).pack(pady=5)
        

        docs_frame = ttk.LabelFrame(stats_frame, text="Statistiques des Documents")
        docs_frame.pack(fill='x', padx=5, pady=5)
        
        self.docs_stats = ttk.Label(docs_frame, text="")
        self.docs_stats.pack(padx=5, pady=5)
        
        ttk.Button(docs_frame, text="Actualiser", command=self.update_docs_stats).pack(pady=5)
        
    def create_document_fields(self, parent):
        ttk.Label(parent, text="Titre:").grid(row=1, column=0, padx=5, pady=5)
        self.titre_entry = ttk.Entry(parent)
        self.titre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="Prix:").grid(row=2, column=0, padx=5, pady=5)
        self.prix_entry = ttk.Entry(parent)
        self.prix_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="Quantité:").grid(row=3, column=0, padx=5, pady=5)
        self.quantite_entry = ttk.Entry(parent)
        self.quantite_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.extra_fields = {}
        
    def update_document_fields(self, event=None):
        for widget in self.extra_fields.values():
            widget.destroy()
        self.extra_fields.clear()

        doc_type = self.doc_type.get()
        row = 4

        def add_field(key, label_text, widget):
            label = ttk.Label(self.doc_type.master, text=label_text)
            label.grid(row=row, column=0, padx=5, pady=5)
            widget.grid(row=row, column=1, padx=5, pady=5)
            self.extra_fields[f'label_{key}'] = label
            self.extra_fields[key] = widget

        if doc_type in ['Roman', 'Nouvelle', 'BD']:
            add_field('nb_pages', "Nombre de Pages:", ttk.Entry(self.doc_type.master))
            row += 1
            add_field('categorie', "Catégorie:", ttk.Combobox(self.doc_type.master, values=['enfant', 'jeune', 'adulte']))
            row += 1
            if doc_type == 'Roman':
                add_field('genre', "Genre:", ttk.Entry(self.doc_type.master))
            elif doc_type == 'Nouvelle':
                add_field('theme', "Thème:", ttk.Entry(self.doc_type.master))
            elif doc_type == 'BD':
                add_field('editeur', "Éditeur:", ttk.Entry(self.doc_type.master))
        elif doc_type in ['Livre Scientifique', 'Encyclopédie']:
            add_field('nb_pages', "Nombre de Pages:", ttk.Entry(self.doc_type.master))
            row += 1
            add_field('domaine', "Domaine:", ttk.Combobox(self.doc_type.master, values=['général', 'recherche', 'technologie']))
            row += 1
            if doc_type == 'Livre Scientifique':
                add_field('champ_etude', "Champ d'étude:", ttk.Entry(self.doc_type.master))
            elif doc_type == 'Encyclopédie':
                add_field('nb_tomes', "Nombre de tomes:", ttk.Entry(self.doc_type.master))
        elif doc_type in ['E-book Texte', 'E-book Spécifique']:
            add_field('taille', "Taille (octets):", ttk.Entry(self.doc_type.master))
            row += 1
            if doc_type == 'E-book Spécifique':
                add_field('format', "Format:", ttk.Entry(self.doc_type.master))
                row += 1
                add_field('logiciel', "Logiciel:", ttk.Entry(self.doc_type.master))
        elif doc_type == 'Manuel Scolaire':
            add_field('niveau', "Niveau:", ttk.Entry(self.doc_type.master))
            row += 1
            add_field('filiere', "Filière:", ttk.Entry(self.doc_type.master))
        elif doc_type == 'Revue':
            add_field('date', "Date'YYYY-MM-DD':", ttk.Entry(self.doc_type.master))
        elif doc_type == 'Dictionnaire':
            add_field('langue', "Langue:", ttk.Entry(self.doc_type.master))

    def add_auteur(self):
        try:
            nom = self.nom_entry.get()
            email = self.email_entry.get()
            genre = self.genre_var.get()
            
            if not all([nom, email]):
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return
            if not re.match(r"\w+@\w+\.\w+", email):
                messagebox.showerror("Erreur", "L'email doit être comme ça : lib@domain.com")
                return
            
            auteur = Auteur(nom, email, genre)
            self.librairie.listeAuteurs.ajouterAuteur(auteur)
            self.refresh_auteurs()
            self.refresh_auteurs_listbox()
            messagebox.showinfo("Succès", f"Auteur ajouté avec succès,{str(auteur)}")
            
            self.nom_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            
    def refresh_auteurs(self):
        for item in self.auteurs_tree.get_children():
            self.auteurs_tree.delete(item)
        for auteur in self.librairie.listeAuteurs.auteurs:
            genre = 'Homme' if auteur.sexe.lower() == 'm' else 'Femme'
            self.auteurs_tree.insert('', 'end', values=(auteur.nom, auteur.email, genre))
            
    def delete_auteur(self):
        selected = self.auteurs_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un auteur à supprimer")
            return
            
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet auteur ?"):
            nom = self.auteurs_tree.item(selected[0])['values'][0]
            self.librairie.SupprimerAuteur(nom)
            self.refresh_auteurs()
            
    def sort_auteurs_asc(self):
        self.librairie.listeAuteurs.TrierAuteurs()
        self.refresh_auteurs()
        
    def sort_auteurs_desc(self):
        self.librairie.listeAuteurs.InverserTriAuteurs()
        self.refresh_auteurs()
        
    def show_female_authors(self):
        femmes = self.librairie.listeAuteurs.AuteursFemmes()
        messagebox.showinfo("Auteurs Femmes", 
                          f"Nombre d'auteurs femmes: {len(femmes)}\n" +
                          f"Pourcentage: {self.librairie.listeAuteurs.PourcentageAuteursFemmes():.2f}%")
        
    def refresh_auteurs_listbox(self):
        self.auteurs_listbox.delete(0, tk.END)
        for auteur in self.librairie.listeAuteurs.auteurs:
            self.auteurs_listbox.insert(tk.END, auteur.nom)
        
    def add_document(self):
        try:
            doc_type = self.doc_type.get()
            titre = self.titre_entry.get()
            prix = float(self.prix_entry.get())
            quantite = int(self.quantite_entry.get())
            
            if doc_type == "" or titre == "" or self.prix_entry.get() == "" or self.quantite_entry.get() == "":
                messagebox.showerror("Erreur", "Tous les champs de base sont requis")
                return
                
            selected = self.auteurs_listbox.curselection()
            if not selected:
                messagebox.showerror("Erreur", "Veuillez sélectionner au moins un auteur")
                return
            auteurs = [self.librairie.listeAuteurs.auteurs[i] for i in selected]
            
            if doc_type == 'Roman':
                nb_pages = int(self.extra_fields['nb_pages'].get())
                categorie = self.extra_fields['categorie'].get()
                genre = self.extra_fields['genre'].get()
                doc = Roman(titre, auteurs, prix, quantite, nb_pages, categorie, genre)
            elif doc_type == 'Nouvelle':
                nb_pages = int(self.extra_fields['nb_pages'].get())
                categorie = self.extra_fields['categorie'].get()
                theme = self.extra_fields['theme'].get()
                doc = Nouvelle(titre, auteurs, prix, quantite, nb_pages, categorie, theme)
            elif doc_type == 'BD':
                nb_pages = int(self.extra_fields['nb_pages'].get())
                categorie = self.extra_fields['categorie'].get()
                editeur = self.extra_fields['editeur'].get()
                doc = BD(titre, auteurs, prix, quantite, nb_pages, categorie, editeur)
            elif doc_type == 'Livre Scientifique':
                nb_pages = int(self.extra_fields['nb_pages'].get())
                domaine = self.extra_fields['domaine'].get()
                champ_etude = self.extra_fields['champ_etude'].get()
                doc = LivreScientifique(titre, auteurs, prix, quantite, nb_pages, domaine, champ_etude)
            elif doc_type == 'Encyclopédie':
                nb_pages = int(self.extra_fields['nb_pages'].get())
                domaine = self.extra_fields['domaine'].get()
                nb_tomes = int(self.extra_fields['nb_tomes'].get())
                doc = Encyclopedie(titre, auteurs, prix, quantite, nb_pages, domaine, nb_tomes)
            elif doc_type == 'E-book Texte':
                taille = int(self.extra_fields['taille'].get())
                doc = EbookTexte(titre, auteurs, prix, quantite, taille)
            elif doc_type == 'E-book Spécifique':
                taille = int(self.extra_fields['taille'].get())
                format_doc = self.extra_fields['format'].get()
                logiciel = self.extra_fields['logiciel'].get()
                doc = EbookSpecifique(titre, auteurs, prix, quantite, taille, format_doc, logiciel)
            elif doc_type == 'Manuel Scolaire':
                niveau = self.extra_fields['niveau'].get()
                filiere = self.extra_fields['filiere'].get()
                niveau_filier = f"{niveau} {filiere}"
                doc = ManuelScolaire(titre, auteurs, prix, quantite, niveau_filier)
            elif doc_type == 'Revue':
                date = self.extra_fields['date'].get()
                doc = Revue(titre, auteurs, prix, quantite, date)
            elif doc_type == 'Dictionnaire':
                langue = self.extra_fields['langue'].get()
                doc = Dictionnaire(titre, auteurs, prix, quantite, langue)
                
            self.librairie.AjouterEntree(doc, auteurs)
            self.refresh_documents()
            messagebox.showinfo("Succès", "Document ajouté avec succès")
            
            self.clear_document_fields()
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            
    def clear_document_fields(self):
        self.titre_entry.delete(0, 'end')
        self.prix_entry.delete(0, 'end')
        self.quantite_entry.delete(0, 'end')
        for entry in self.extra_fields.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, 'end')
            elif isinstance(entry, ttk.Combobox):
                entry.set('')
                
    def refresh_documents(self):
        for item in self.documents_tree.get_children():
            self.documents_tree.delete(item)
        
        for doc in self.librairie.listeDocuments.documents:
            auteurs_str = ', '.join([a.nom for a in getattr(doc, 'nomAuteur', [])])
            self.documents_tree.insert('', 'end', values=(doc.numero, doc.titre, 
                                                        auteurs_str,
                                                        type(doc).__name__,
                                                        doc.prix,
                                                        doc.quantite_en_stock))
            
    def delete_document(self):
        selected = self.documents_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un document à supprimer")
            return
            
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce document ?"):
            numero = self.documents_tree.item(selected[0])['values'][0]
            self.librairie.listeDocuments.SupprimerParNumero(numero)
            self.refresh_documents()
            
    def sort_documents_title(self):
        self.librairie.listeDocuments.TrierParTitre()
        self.refresh_documents()
        
    def sort_documents_price(self):
        self.librairie.listeDocuments.TrierParPrix()
        self.refresh_documents()
        
    def show_out_of_stock(self):
        rupture = self.librairie.listeDocuments.RuptureStock()
        if not rupture:
            messagebox.showinfo("Rupture de Stock", "Aucun document en rupture de stock")
            return
            
        message = "Documents en rupture de stock:\n\n"
        for doc in rupture:
            message += f"- {doc.titre} ({type(doc).__name__})\n"
        messagebox.showinfo("Rupture de Stock", message)
        
    def search(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Attention", "Veuillez entrer un mot-clé de recherche")
            return
            
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        auteurs = self.librairie.listeAuteurs.RechercherAuteurs(query)
        for auteur in auteurs:
            self.search_tree.insert('', 'end', values=('Auteur', f"{auteur[1].nom} - {auteur[1].email} - {auteur[1].sexe}"))
            
        # Rechercher dans les documents
        # while True:
        doc = self.librairie.listeDocuments.rechercherParTitre(query)
        #     if doc[0] != -1 :
        #         self.search_tree.insert('', 'end', values=('Document', f"{doc[1].titre} - {type(doc[1]).__name__}"))
        #     else:
        #         break
        self.search_tree.insert('', 'end', values=('Document', f"{doc[1].titre} - {type(doc[1]).__name__}"))

            
    def update_authors_stats(self):
        total = self.librairie.listeAuteurs.getNombreAuteurs()
        femmes = len(self.librairie.listeAuteurs.AuteursFemmes())
        pourcentage = self.librairie.listeAuteurs.PourcentageAuteursFemmes()
        
        stats = f"Nombre total d'auteurs: {total}\n"
        stats += f"Nombre d'auteurs femmes: {femmes}\n"
        stats += f"Pourcentage d'auteurs femmes: {pourcentage:.2f}%"
        
        self.auteurs_stats.config(text=stats)
        
    def update_docs_stats(self):
        total = self.librairie.listeDocuments.getNombreDocuments()
        rupture = len(self.librairie.listeDocuments.RuptureStock())
        
        stats = f"Nombre total de documents: {total}\n"
        stats += f"Documents en rupture de stock: {rupture}\n\n"
        
        stats += "Répartition par type:\n"
        stats += f"Romans: {len(self.librairie.listeDocuments.Romans())}\n"
        stats += f"Nouvelles: {len(self.librairie.listeDocuments.Nouvelles())}\n"
        stats += f"BDs: {len(self.librairie.listeDocuments.BDs())}\n"
        stats += f"Livres scientifiques: {len(self.librairie.listeDocuments.LivresScientifiques())}\n"
        stats += f"Encyclopédies: {len(self.librairie.listeDocuments.Encyclopedies())}\n"
        stats += f"E-books texte: {len(self.librairie.listeDocuments.EbooksTexte())}\n"
        stats += f"E-books spécifiques: {len(self.librairie.listeDocuments.EbooksSpecifiques())}\n"
        stats += f"Manuels scolaires: {len(self.librairie.listeDocuments.ManuelsScolaires())}\n"
        stats += f"Revues: {len(self.librairie.listeDocuments.Revues())}\n"
        stats += f"Dictionnaires: {len(self.librairie.listeDocuments.Dictionnaires())}"
        
        self.docs_stats.config(text=stats)

    def show_selected_document_info(self):
        selected = self.documents_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un document dans la liste.")
            return
        numero = self.documents_tree.item(selected[0])['values'][0]
        doc = next((d for d in self.librairie.listeDocuments.documents if d.numero == numero), None)
        if doc:
            messagebox.showinfo("Informations du Document", str(doc))
        else:
            messagebox.showerror("Erreur", "Document introuvable.")

    def on_closing(self):
        if not self.session_saved:
            if not messagebox.askyesno("Attention", "Vous n'avez pas sauvegardé la session. Voulez-vous vraiment quitter sans sauvegarder ?"):
                return
        self.root.destroy()

    def session_restore_reminder(self):
        messagebox.showinfo("Rappel", "Pour restaurer une session précédente, cliquez sur 'Restaurer la session (CSV)' en bas de la fenêtre.")

    def save_session_csv(self):
        try:
            with open('auteurs.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['nom', 'email', 'genre'])  # header / keys
                for auteur in self.librairie.listeAuteurs.auteurs:
                    writer.writerow([auteur.nom, auteur.email, auteur.sexe])

            with open('documents.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['type', 'titre', 'auteurs', 'prix', 'quantite', 'attributs'])  # header / keys
                for doc in self.librairie.listeDocuments.documents:
                    doc_type = type(doc).__name__
                    
                    auteurs = ','.join([a.nom for a in doc.nomAuteur])
                    
                    attributs = {}
                    if doc_type in ['Roman', 'Nouvelle', 'BD']:
                        attributs = {
                            'nb_pages': doc.nbpages,
                            'categorie': doc.categorie,
                            'genre' if doc_type == 'Roman' else 'theme' if doc_type == 'Nouvelle' else 'editeur': 
                                getattr(doc, 'genre' if doc_type == 'Roman' else 'theme' if doc_type == 'Nouvelle' else 'editeur')
                        }
                    elif doc_type in ['LivreScientifique', 'Encyclopedie']:
                        attributs = {
                            'nb_pages': doc.nbpages,
                            'domaine': doc.domaine,
                            'champ_etude' if doc_type == 'LivreScientifique' else 'nb_tomes': 
                                getattr(doc, 'champ_etude' if doc_type == 'LivreScientifique' else 'nb_tomes')
                        }
                    elif doc_type in ['EbookTexte', 'EbookSpecifique']:
                        attributs = {
                            'taille': doc.taille_octets
                        }
                        if doc_type == 'EbookSpecifique':
                            attributs.update({
                                'format': doc.format,
                                'logiciel': doc.logiciel
                            })
                    elif doc_type == 'ManuelScolaire':
                        attributs = {'niveau_filiere': doc.niveau_filier}
                    elif doc_type == 'Revue':
                        attributs = {'date': doc.date}
                    elif doc_type == 'Dictionnaire':
                        attributs = {'langue': doc.langue}
                    
                    writer.writerow([
                        doc_type,
                        doc.titre,
                        auteurs,
                        doc.prix,
                        doc.quantite_en_stock,
                        str(attributs)
                    ])
            
            self.session_saved = True
            messagebox.showinfo("Succès", "Session sauvegardée avec succès dans les fichiers 'auteurs.csv' et 'documents.csv'")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def load_session_csv(self):
        try:
            self.librairie = Librairie()
            
            if os.path.exists('auteurs.csv'):
                with open('auteurs.csv', 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        auteur = Auteur(row['nom'], row['email'], row['genre'])
                        self.librairie.listeAuteurs.ajouterAuteur(auteur)
            
            if os.path.exists('documents.csv'):
                with open('documents.csv', 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        auteurs_noms = row['auteurs'].split(',')
                        auteurs = []
                        for nom in auteurs_noms:
                            result = self.librairie.listeAuteurs.RechercherAuteur(nom)
                            if result[0] != -1:
                                auteurs.append(result[1])
                        
                        attributs = eval(row['attributs'])
                        
                        doc_type = row['type']
                        if doc_type == 'Roman':
                            doc = Roman(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                      attributs['nb_pages'], attributs['categorie'], attributs['genre'])
                        elif doc_type == 'Nouvelle':
                            doc = Nouvelle(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                         attributs['nb_pages'], attributs['categorie'], attributs['theme'])
                        elif doc_type == 'BD':
                            doc = BD(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                   attributs['nb_pages'], attributs['categorie'], attributs['editeur'])
                        elif doc_type == 'LivreScientifique':
                            doc = LivreScientifique(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                                  attributs['nb_pages'], attributs['domaine'], attributs['champ_etude'])
                        elif doc_type == 'Encyclopedie':
                            doc = Encyclopedie(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                             attributs['nb_pages'], attributs['domaine'], attributs['nb_tomes'])
                        elif doc_type == 'EbookTexte':
                            doc = EbookTexte(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                           attributs['taille'])
                        elif doc_type == 'EbookSpecifique':
                            doc = EbookSpecifique(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                                attributs['taille'], attributs['format'], attributs['logiciel'])
                        elif doc_type == 'ManuelScolaire':
                            doc = ManuelScolaire(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                               attributs['niveau_filiere'])
                        elif doc_type == 'Revue':
                            doc = Revue(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                      attributs['date'])
                        elif doc_type == 'Dictionnaire':
                            doc = Dictionnaire(row['titre'], auteurs, float(row['prix']), int(row['quantite']),
                                             attributs['langue'])
                        
                        self.librairie.AjouterEntree(doc, auteurs)
            
            self.refresh_auteurs()
            self.refresh_auteurs_listbox()
            self.refresh_documents()
            
            messagebox.showinfo("Succès", "Session restaurée avec succès")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la restauration: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrairieGUI(root)
    root.mainloop() 
