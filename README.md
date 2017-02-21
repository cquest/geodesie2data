# geodesie2data
**Scripts d'extractions des données des repères géodésiques de l'IGN**

Le but de ces scripts est d'extraire des fiches de géodésie (uniquement disponibles sous forme de fichier PDF) des données facilement réutilisables dans un format ouvert.

L'IGN a par ailleurs confirmé que ces données étaient sous **Licence Ouverte**. Si vous les réutilisez n'oublier pas d'indiquer "source IGN" mains que la date d'extraction.

## Les différentes étapes

### Récupérer la liste des sites
http://geodesie.ign.fr s'appuie sur un service WFS conforme au standard OGC.
Il suffit de l'appeler pour obtenir la liste des sites où sont situés des repères géodésiques.
**ogr2ogr** est utilisé pour récupérer les données et les convertir en geojson.

### Récupérer les PDF de chaque site
**jq** est utilisé pour extraire pour chaque site l'URL du PDF et l'id du site.
**wget** est ensuite utilisé pour récupérer les fichiers PDF.
Le tout est parallélisé avec **GNU parallel**.

### Extraire le texte contenu dans les fichiers PDF
**pdfminer** est utilisé pour faire cette conversion

### Analyser le texte des PDF et en extraire les données utiles
Ici c'est un script **python** qui fonctionne avec une machine à état pour s'adapter au format variable du contenu textuel des PDF.
La sortie est en json.

### Mise en forme du json final
C'est à nouveau **jq** qui est utilisé pour remettre chaque fichier json dans un unique json global.
