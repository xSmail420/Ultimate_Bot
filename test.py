
def filter_views(objet, seuil):
        valeur_en_nombre = convertir_en_nombre(objet["views"])
        return valeur_en_nombre < seuil
    

def convertir_en_nombre(valeur):
    multiplicateurs = {'K': 1000, 'M': 1000000}
    for suffixe, facteur in multiplicateurs.items():
        if suffixe in valeur:
            return float(valeur.replace(f'{suffixe} views', '')) * facteur
    return float(valeur.replace(' views', ''))

# Exemple d'utilisation
objet1 = {"views": "623 views"}
objet2 = {"views": "2.1M views", "dsfsd":"gdfgd"}

seuil = 1000
print(filter_views(objet1, 1000))  # True
print(filter_views(objet2, 1000))  # False
