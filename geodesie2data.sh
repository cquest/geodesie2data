# récupération données via WFS
ogr2ogr -f geojson rbf.json WFS:http://geodesie.ign.fr/cgi-bin/mapserv?map=/var/webapp/lib/visugeod/mapfile_bdg.map sit_rbfType

# récupération des PDF
mkdir -p rbf
jq -r '.features[].properties|[.url, .nom]|@csv' rbf.json | sed 's/"//g' | parallel --colsep ',' wget -q {1} -O rbf/{2}.pdf

# extraction texte contenu dans les PDF
for f in rbf/*.pdf; do pdf2txt.py $f > $f.txt; done
# conversion en json
: > rbf.sjson ;for f in rbf/*.pdf.txt; do echo $f; python3 txt2data.py $f >> rbf.sjson; done
jq -s '.' rbf.sjson > rbf-all.json

exit

ogr2ogr -f geojson rdf.json WFS:http://geodesie.ign.fr/cgi-bin/mapserv?map=/var/webapp/lib/visugeod/mapfile_bdg.map sit_rdfType
mkdir -p rdf
jq -r '.features[].properties|[.url, .nom]|@csv' rdf.json | sed 's/"//g' | parallel --colsep ',' echo {2} \; wget -q {1} -O rdf/{2}.pdf

# extraction texte contenu dans les PDF
for f in rdf/*.pdf; do pdf2txt.py $f > $f.txt ; done
# conversion en json
: > rdf.sjson ; for f in rdf/*.pdf.txt; do echo $f; python3 txt2data.py $f >> rdf.sjson; done
jq -s '.' rdf.sjson > rdf-all.json


ogr2ogr -f geojson rn.json WFS:http://geodesie.ign.fr/cgi-bin/mapserv?map=/var/webapp/lib/visugeod/mapfile_bdg.map sit_rnType
mkdir -p rn
jq -r '.features[].properties|[.url, .nom]|@csv' rn.json | sed 's/"//g' | parallel --colsep ',' wget -q {1} -O rn/{2}.pdf
