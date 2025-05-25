class SexeExeption(Exception):

    def __str__(self):
        return f"{super().__str__()} , le sexe doit etre M ou F !!!"
    
    
class ListeObjetsExeption(Exception):
    
    def __str__(self):
        return super().__str__() + " la variable doit etre un liste des objets"
    