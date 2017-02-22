# geodesie2data
**Scripts d'extractions des données des repères géodésiques de l'IGN**

Le but de ces scripts est d'extraire des fiches de géodésie (uniquement disponibles sous forme de fichier PDF) des données facilement réutilisables dans un format ouvert.

L'IGN a par ailleurs confirmé que ces données étaient sous **Licence Ouverte**. Si vous les réutilisez n'oublier pas d'indiquer "source IGN/geodesie.ign.fr" ainsi que la date d'extraction.

## Dépendances

Pour installer les dépendances (sur GNU/Linux):
```
apt-get install jq parallel wget python3
pip install pdfminer
```
## Les différentes étapes

### Récupérer la liste des sites
http://geodesie.ign.fr s'appuie sur un service WFS conforme au standard OGC.
Il suffit de l'appeler pour obtenir la liste des sites où sont situés des repères géodésiques.
**[ogr2ogr](http://www.gdal.org/ogr2ogr.html)** est utilisé pour récupérer les données et les convertir en geojson.

### Récupérer les PDF de chaque site
- **[jq](https://stedolan.github.io/jq/)** est utilisé pour extraire du fichier geojson l'URL du PDF et l'id de chaque site.
- **wget** est ensuite utilisé pour récupérer les fichiers PDF.
- Le tout est parallélisé avec **[GNU parallel](https://www.gnu.org/software/parallel/)**.

### Extraire le texte contenu dans les fichiers PDF
**[pdfminer](http://www.unixuser.org/~euske/python/pdfminer/)** est utilisé pour faire cette conversion

### Analyser le texte des PDF et en extraire les données utiles
Ici c'est un script **python3** qui fonctionne avec une machine à état pour s'adapter au format variable du contenu textuel des PDF.
La sortie est en json.

### Mise en forme du json final
C'est à nouveau **jq** qui est utilisé pour remettre chaque fichier json dans un unique json global.

## Exemple
```
  {
    "commune": "BENONCES",
    "departement": "AIN (01)",
    "ld": "CALVAIRE DE PORTES",
    "nom": "BENONCES I",
    "numero": "03701",
    "reperes": [
      {
        "alti": 1073.973,
        "description": "Borne 1946 en granit gravée IGN : Repère hémisphérique 1994, en laiton de 12 mm de diamètre",
        "gps": "ok",
        "id": "183 - NO : 0103701-01",
        "indice": "a",
        "lat": 45.857334847222226,
        "lon": 5.491579569444444,
        "nivellement": "R'.B.P3 - 108-II",
        "precision_plani_max": "1 cm",
        "vu": "2012"
      },
      {
        "alti": 1067.645,
        "description": "Regard en béton : Repère hémisphérique 1994 en laiton de 12, mm de diamètre",
        "gps": "ok",
        "id": "184 - NO : 0103701-02",
        "indice": "b",
        "lat": 45.858032550000004,
        "lon": 5.491103238888889,
        "nivellement": "R'.B.P3 - 108-I",
        "precision_plani_max": "5 cm",
        "vu": "2012"
      },
      
