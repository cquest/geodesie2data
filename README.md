# geodesie2data
**Scripts d'extractions des données des repères géodésiques de l'IGN**

Le but de ces scripts est d'extraire des fiches de géodésie (uniquement disponibles sous forme de fichier PDF) des données *"dans un standard ouvert, aisément réutilisable et exploitable par un système de traitement automatisé"*.

Afin d'éviter que chacun ne refasse des milliers de téléchargements et d'analyses de fichiers PDF, **les données déjà extraites sont disponibles en json :**
- fichier pour le [Réseau de Base](https://github.com/cquest/geodesie2data/raw/master/rbf-all.json) (un peu plus de 1100 bornes)
- fichier pour le [Réseau de Détail](https://github.com/cquest/geodesie2data/raw/master/rdf-all.json.zip) (plus de 64000 bornes)

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
**[ogr2ogr](http://www.gdal.org/ogr2ogr.html)** est ici utilisé pour récupérer ces données et les convertir en geojson.
Ceci permet d'obtenir les URL des fichiers PDF décrivant chaque site géodésique.

### Récupérer les PDF de chaque site
- **[jq](https://stedolan.github.io/jq/)** est utilisé pour extraire du fichier geojson l'URL du PDF et l'id de chaque site.
- **wget** sert à récupérer les fichiers PDF.
- Le tout est parallélisé avec **[GNU parallel](https://www.gnu.org/software/parallel/)**.

### Extraire le texte contenu dans les fichiers PDF
**[pdfminer](http://www.unixuser.org/~euske/python/pdfminer/)** fait cette conversion et produit des fichiers .txt reprenant le contenu textuel des fichiers PDF.

### Analyser le texte des PDF et en extraire les données utiles
Ici c'est un script **python3** qui fonctionne avec une machine à état pour s'adapter au format variable du contenu textuel extrait des PDF par pdfminer.
La sortie est en json.

### Mise en forme du json final
C'est à nouveau **jq** qui est utilisé pour transformer le stream json dans un unique tableau json.

## Exemple
```
  {
    "commune": "SAINT-LAURENT-SUR-SAONE",
    "date": "2017/02/21",
    "departement": "AIN (01)",
    "ld": "",
    "ref_latlon": "RGF93 (ETRS89) - Ellipsoïde : IAG GRS 1980",
    "ref_proj": "RGF93 (ETRS89) - Projection : LAMBERT-93 - Système altimétrique : NGF-IGN",
    "ref_proj_alti": "NGF-IGN",
    "ref_proj_epsg": "2154",
    "reperes": [
      {
        "description": "Pont : Culée S.E. : Repère hémisphérique 1994 en laiton de 18, mm de diamètre",
        "ele": 231.737,
        "id": "1814",
        "indice": "b",
        "lat": 46.30848479444444,
        "lon": 4.850522066666667,
        "nivellement": "J'.D.N3 - 144-III",
        "numero": "0137002-02",
        "precision_alti_max": 5,
        "precision_plani_max": 0.05,
        "vu": "2016",
        "x": 842401.481,
        "y": 6580400.169,
        "z": 183.084
      },
      {
        "description": "Borne IGN 2004 dans un massif de béton : repère hémisphérique, en laiton de 12mm de diamètre",
        "ele": 223.616,
        "id": "1816",
        "indice": "c",
        "lat": 46.306721575,
        "lon": 4.841772013888889,
        "nivellement": "J'.D.N3 - 144-II",
        "numero": "0137002-04",
        "precision_alti_max": 5,
        "precision_plani_max": 0.05,
        "vu": "2016",
        "x": 841732.835,
        "y": 6580188.669,
        "z": 174.92
      }
    ],
    "reseau": "Réseau de base",
    "site_nom": "SAINT-LAURENT-SUR-SAONE II",
    "site_num": "0137002"
  }
```
