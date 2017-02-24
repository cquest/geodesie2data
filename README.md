# geodesie2data
**Scripts d'extractions des données des repères géodésiques de l'IGN**

Le but de ces scripts est d'extraire des fiches de géodésie (uniquement disponibles sous forme de fichier PDF) des données *"dans un standard ouvert, aisément réutilisable et exploitable par un système de traitement automatisé"*.

Afin d'éviter que chacun ne refasse des milliers de téléchargements et d'analyses de fichiers PDF, **les données déjà extraites sont disponible en json :**
- fichier pour le [Réseau de Base](https://github.com/cquest/geodesie2data/raw/master/rbf-all.json) (un peu plus de 1100 bornes)
- fichier pour le Réseau de Détail (plus de 64000 bornes, à venir, dès vérification que l'extraction est correcte pour le Réseau de Base)

L'IGN a par ailleurs confirmé que ces données étaient sous [**Licence Ouverte**](https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Licence_Ouverte.pdf). Si vous les réutilisez n'oublier pas d'indiquer "source IGN/geodesie.ign.fr" ainsi que la date d'extraction car ce sont des données qui évoluent avec le temps.

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
    "commune": "CHATILLON-SUR-CHALARONNE",
    "date": "2017/02/21",
    "departement": "AIN (01)",
    "ld": "LES PETITES MURES",
    "ref_latlon": "RGF93 (ETRS89) - Ellipsoïde : IAG GRS 1980",
    "ref_proj": "RGF93 (ETRS89) - Projection : LAMBERT-93 - Système altimétrique : NGF-IGN",
    "ref_proj_alti": "NGF-IGN",
    "ref_proj_epsg": "2154",
    "reperes": [
      {
        "description": "Borne 1948 en granit gravée IGN : Repère hémisphérique 1994, en laiton de 12 mm de diamètre",
        "ele": 311.261,
        "gps": "ok",
        "id": "441",
        "indice": "a",
        "lat": 46.107882519444445,
        "lon": 4.946572355555555,
        "nivellement": "J'.E.L3N3 - 3-II",
        "numero": "0109301-01",
        "precision_alti_max": 5,
        "precision_plani_max": 0.01,
        "vu": "2016",
        "x": 850340.407,
        "y": 6558307.449,
        "z": 262.432
      },
      {
        "description": "Muret du portail de la DDE : Repère hémisphérique 2003 en, laiton de 12 mm de diamètre",
        "ele": 292.772,
        "id": "444",
        "indice": "c",
        "lat": 46.11576530833334,
        "lon": 4.9397188000000005,
        "nivellement": "J'.E.L3 - 34-I",
        "numero": "0109301-04",
        "precision_alti_max": 5,
        "precision_plani_max": 0.05,
        "vu": "2016",
        "x": 849789.688,
        "y": 6559169.549,
        "z": 243.951
      }
    ],
    "reseau": "Réseau de base",
    "site_nom": "CHATILLON-SUR-CHALARONNE I",
    "site_num": "0109301"
  },
```
