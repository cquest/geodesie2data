# geodesie2data
**Scripts d'extractions des données des repères géodésiques de l'IGN**

Le but de ces scripts est d'extraire des fiches de géodésie (uniquement disponibles sous forme de fichier PDF) des données *"dans un standard ouvert, aisément réutilisable et exploitable par un système de traitement automatisé"*.

Afin d'éviter que chacun ne refasse des milliers de téléchargements et d'analyses de fichiers PDF, **les données déjà extraites sont disponibles en json :**
- fichier pour le [Réseau de Base](https://github.com/cquest/geodesie2data/raw/master/rbf-all.json) (un peu plus de 1100 bornes)
- fichier pour le [Réseau de Détail](https://github.com/cquest/geodesie2data/raw/master/rdf-all.json.zip) (plus de 64000 bornes)

## Licence des données

L'IGN a par ailleurs confirmé que ces données étaient sous [**Licence Ouverte**](https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Licence_Ouverte.pdf). Si vous les réutilisez n'oublier pas d'indiquer "source IGN/geodesie.ign.fr" ainsi que la date d'extraction car ce sont des données qui évoluent avec le temps.

## Qualité

La récupération des données contenues dans les PDF n'étant pas triviale, des erreurs sont possibles. Merci de les signaler afin d'améliorer le script d'extraction (txt2data.py). Reportez vous toujours aux fiches officielles (PDF) en cas de doute.

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

## Exemple (JSON)
```
{
  "commune": "SAINT-LEU-LA-FORET",
  "date_fiche": "2017/01/26",
  "departement": "VAL-D'OISE (95)",
  "ref_latlon": "RGF93 (ETRS89) - Ellipsoïde : IAG GRS 1980",
  "ref_proj": "RGF93 (ETRS89) - Projection : LAMBERT-93 - Système altimétrique : NGF-IGN",
  "ref_proj_alti": "NGF-IGN",
  "ref_proj_epsg": "2154",
  "reperes": [
    {
      "description": "Borne 1995 en béton : Repère hémisphérique en laiton de 18 mm de diamètre",
      "ele": 106.563,
      "gps": "ok",
      "id": "206818",
      "indice": "a",
      "lat": 49.005742552777775,
      "lon": 2.2484194333333334,
      "nivellement": "G.C.T3 - 344-I",
      "numero": "9556301-01",
      "precision_alti_max": 0.005,
      "precision_plani_max": 0.01,
      "vu": "2015",
      "x": 645012.411,
      "y": 6878687.024,
      "z": 62.84
    },
    {
      "description": "Borne 1995 en Polyester-béton : Repère hémisphérique de 25 mm de diamètre",
      "ele": 114.722,
      "gps": "ok",
      "id": "206819",
      "indice": "b",
      "lat": 49.009885402777776,
      "lon": 2.2395948194444446,
      "numero": "9556301-02",
      "precision_alti_max": 0.1,
      "precision_plani_max": 0.05,
      "vu": "2014",
      "x": 644371.236,
      "y": 6879153.912,
      "z": 71.01
    }
  ],
  "reseau": "Réseau de base",
  "site_nom": "SAINT-LEU-LA-FORET I",
  "site_num": "9556301"
}
```
