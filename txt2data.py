import sys
import json
import re

state = 0
d = {'reperes':[]} # données du site
re_lonlat = re.compile(r"^ *(\d+)° *(\d+)' ([0-9\.]+)'' ([EO]) *(\d+)° (\d+)' ([0-9\.]*)'' ([NS]) *([\-0-9\.]*)$")
re_lat = re.compile(r"^ *(\d+)° (\d+)' ([0-9\.]*)'' ([NS]) *([\-0-9\.]*)$")
re_lon = re.compile(r"^ *(\d+)° *(\d+)' ([0-9\.]+)'' ([EO])$")

f = open(sys.argv[1])
for l in f:
  l=l[:-1]
  if state==0 and l=='Réseau Géodésique Français': # première page, entête
    state=1
  elif state==1 and l!='':
    d['nom'] = l
    state=2
  elif state==2 and l[:10]=='No du Site':
    d['numero']=l[14:]
  elif state==2 and l[:13]=='Département :':
    d['departement']=l[15:]
  elif state==2 and l[:9]=='Commune :':
    d['commune']=l[11:]
  elif state==2 and l[:10]=='Lieu-dit :':
    d['ld']=l[12:]
  elif state==2 and l[:7]=='Site du':
    d['reseau']=l[9:]
  elif state==2 and l=='IGN/SGN': # page suivante, détail
    state=3
  elif (state==3 or state==6 or state==7) and l[:13]=='Identifiant :':
    d['reperes'].append({})
    d['reperes'][len(d['reperes'])-1]['id']=l[14:]
    state = 4
  elif state==4 and l[:7]=='Point :':
    d['reperes'][len(d['reperes'])-1]['indice']=l[8:]
    state = 5
  elif state==5 and l!='':
    d['reperes'][len(d['reperes'])-1]['description']=l
    state = 6
  elif state==6 and l[:20]=='Point vu en place en':
    d['reperes'][len(d['reperes'])-1]['vu']=l[21:]
    state = 7
  elif state==6 and l=="© 2009 IGN - INSTITUT NATIONAL DE L'INFORMATION GÉOGRAPHIQUE ET FORESTIÈRE":
    state=7
  elif (state==7 or state==6) and l[:27]=='Azimut de la prise de vue :':
    state=7
  elif (state==7 or state==6) and l[:23]=='Repère de nivellement :':
    d['reperes'][len(d['reperes'])-1]['nivellement']=l[24:]
  elif (state==7 or state==6) and l=='Exploitable directement par GPS':
    d['reperes'][len(d['reperes'])-1]['gps']='ok'
  elif state==6 and l!='':
    d['reperes'][len(d['reperes'])-1]['description']=d['reperes'][len(d['reperes'])-1]['description']+', '+l
  elif state==7 and l[:9]=='Système :': # début coordonnées
    # on récupère le SRS
    d['reperes'][len(d['reperes'])-1]['systeme']=l[10:]
    state=8
    repere=0 # on repart sur le premier repère du tableau d['reperes']
  elif state==8:
    c = re_lonlat.match(l)
    if c is not None:
      lon=int(c.group(1))+int(c.group(2))/60+float(c.group(3))/3600
      if c.group(4)=='O':
        lon=-lon
      lat=int(c.group(5))+int(c.group(6))/60+float(c.group(7))/3600
      if c.group(8)=='S':
        lat=-lat
      d['reperes'][repere]['lon']=lon
      d['reperes'][repere]['lat']=lat
      if c.group(9)!='':
        d['reperes'][repere]['alti']=float(c.group(9))
      repere = repere+1
    else:
      c = re_lat.match(l)
      if c is not None:
        lat=int(c.group(1))+int(c.group(2))/60+float(c.group(3))/3600
        if c.group(4)=='S':
          lat=-lat
        d['reperes'][repere]['lat']=lat
        if c.group(5)!='':
          d['reperes'][repere]['alti']=float(c.group(5))
        if 'lon' in d['reperes'][repere]:
          repere = repere+1
      else:
        c = re_lon.match(l)
        if c is not None:
          lon=int(c.group(1))+int(c.group(2))/60+float(c.group(3))/3600
          if c.group(4)=='O':
            lon=-lon
          d['reperes'][repere]['lon']=lon
          if 'lat' in d['reperes'][repere]:
            repere = repere+1
    if l=='' and repere>0:
      state=9
      repere=0
  elif state==9:
    d['reperes'][repere]['precision_plani_max']=l[5:]
    if repere==len(d['reperes'])-1:
      state=10
    else:
      repere = repere+1
  elif state==10 and l=='Précision alti':
    state=11
  elif state==11:
    d['reperes'][repere]['precision_alti_max']=l[5:]
    if repere==len(d['reperes'])-1:
      state=12
    else:
      repere = repere+1
  #print(state,l)
  
print(json.dumps(d,sort_keys=True))

