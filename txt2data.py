#!/usr/bin/python3
import sys
import json
import csv
import re

def addxyz(key, value, store):
  r = -1
  for row in store:
    r = r+1
    if key not in row:
      row[key]=value
      return r

state = 0
d = {'reperes':[]} # données du site
re_lonlat = re.compile(r"^ *(\d+)° *(\d+)' ([0-9\.]+)'' ([EO]) *(\d+)° (\d+)' ([0-9\.]*)'' ([NS]) *([\-0-9\.]*)$")
re_lat = re.compile(r"^ *(\d+)° (\d+)' ([0-9\.]*)'' ([NS]) *([\-0-9\.]*)$")
re_lon = re.compile(r"^ *(\d+)° *(\d+)' ([0-9\.]+)'' ([EO])")
re_alti = re.compile(r" +([\-0-9\.]+)$")
re_date= re.compile(r"^(\d\d)/(\d\d)/(\d\d\d\d)")

# format de sortie json ou csv
sortie = 'json'
try:
    sortie = sys.argv[2]
except:
    pass

if sortie=='csv':
    fieldnames = ['numero','indice','id','nivellement','date_fiche','reseau','site_nom','site_num','commune','ld','departement','description','gps','vu','lat','lon','ele','x','y','z','precision_plani_max','precision_alti_max','ref_latlon','ref_proj','ref_proj_epsg','ref_proj_alti']
    csvout = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    #csvout.writeheader()

f = open(sys.argv[1])
for l in f:
  l=l[:-1]
  if sortie == 'debug':
      print(state,l)

  if state==0 and l=='Réseau Géodésique Français': # première page, entête
    state=2
  elif state==2 and l[:10]=='No du Site':
    d['site_num']=l[12:]
  elif state==2 and l[:13]=='Département :':
    d['departement']=l[15:]
  elif state==2 and l[:9]=='Commune :':
    d['commune']=l[11:]
  elif state==2 and l[:10]=='Lieu-dit :':
    if l[12:] != '':
        d['ld']=l[12:]
  elif state==2 and l[:7]=='Site du':
    d['reseau']=l[9:]
  elif state==2 and l=='IGN/SGN': # page suivante, détail
    state=3
  elif state==2 and l!='' and 'site_nom' not in d:
    d['site_nom'] = l
  elif (state==3 or state==7) and re_date.match(l) is not None:
    date = re_date.match(l)
    d['date_fiche']=date.group(3)+'/'+date.group(2)+'/'+date.group(1)
  elif (state==2 or state==3 or state==6 or state==7) and l[:13]=='Identifiant :':
    num = l.find('NO :')
    if num>0:
        d['reperes'].append({})
        d['reperes'][len(d['reperes'])-1]['id']=l[14:num-3]
        d['reperes'][len(d['reperes'])-1]['numero']=l[num+5:]
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
  elif state==6 and l[:23]=='Support en mauvais état':
    d['reperes'][len(d['reperes'])-1]['vu']=l[-4:]
    state = 7
  elif state==6 and l[:9]=='Point non':
    state = 7
  elif state==6 and l=="© 2009 IGN - INSTITUT NATIONAL DE L'INFORMATION GÉOGRAPHIQUE ET FORESTIÈRE":
    state=7
  elif (state==7 or state==6) and l[:27]=='Azimut de la prise de vue :':
    state=7
  elif (state==7 or state==6) and l[:23]=='Compte-tenu des risques':
    state=7
  elif (state==7 or state==6) and l[:23]=='Repère de nivellement :':
    d['reperes'][len(d['reperes'])-1]['nivellement']=l[24:]
  elif (state==7 or state==6) and l=='Exploitable directement par GPS':
    d['reperes'][len(d['reperes'])-1]['gps']='ok'
  elif state==6 and l!='':
    d['reperes'][len(d['reperes'])-1]['description']=d['reperes'][len(d['reperes'])-1]['description']+' '+l
  elif (state==6 or state==7) and l[:9]=='Système :': # début coordonnées
    # on récupère le SRS
    d['ref_latlon']=l[10:]
    state = 8
    repere = 0 # on repart sur le premier repère du tableau d['reperes']

  elif state==8:
    c = re_lonlat.match(l)
    if c is not None:
      lon=int(c.group(1))+int(c.group(2))/60+float(c.group(3))/3600
      if c.group(4)=='O':
        lon=-lon
      cur = addxyz('lon',lon,d['reperes'])
      lat=int(c.group(5))+int(c.group(6))/60+float(c.group(7))/3600
      if c.group(8)=='S':
        lat=-lat
      d['reperes'][cur]['lat']=lat
      if c.group(9)!='':
        d['reperes'][cur]['ele']=float(c.group(9))
    else:
        c = re_lat.match(l)
        if c is not None:
          lat=int(c.group(1))+int(c.group(2))/60+float(c.group(3))/3600
          if c.group(4)=='S':
            lat=-lat
          cur = addxyz('lat',lat,d['reperes'])
          if c.group(5)!='':
            d['reperes'][cur]['ele']=float(c.group(5))

        c = re_lon.match(l)
        if c is not None:
          lon=int(c.group(1))+int(c.group(2))/60+float(c.group(3))/3600
          if c.group(4)=='O':
            lon=-lon
          addxyz('lon',lon,d['reperes'])

        c = re_alti.match(l)
        if c is not None:
          addxyz('ele',float(c.group(1)),d['reperes'])

    if l=='' and 'lat' in d['reperes'][len(d['reperes'])-1] and 'lon' in d['reperes'][len(d['reperes'])-1]:
      state=10
      repere=0

  elif (state==10) and l.find('Projection')>=0:
    d['ref_proj']=l[10:]
    if l.find('RGF93')>=0:
      d['ref_proj_epsg']='2154'
    if l.find('RGAF09')>=0:
      d['ref_proj_epsg']='5490'
    if l.find('RGR92_07')>=0:
      d['ref_proj_epsg']='2975'
    if l.find('RGFG95')>=0:
      d['ref_proj_epsg']='2972'
    if l.find('RGM04')>=0:
      d['ref_proj_epsg']='4471'
    if l.find('RGSPM06')>=0:
      d['ref_proj_epsg']='4467'
    if l.find('UTM NORD FUSEAU 20')>=0:
      d['ref_proj_epsg']='4559'

    alti = l.find("Système altimétrique :")
    if alti>=0:
      d['ref_proj_alti']=l[alti+23:]

  elif state==10 and l=='(NGG) 1977':
    d['ref_proj_alti'] = 'NGG 1977'

  elif state==10 and l=='e (m)':
    state=11
    repere = 0

  elif state==11 and l.find('.')>0:
    d['reperes'][repere]['x']=float(l)
    if repere==len(d['reperes'])-1:
      state=12
    else:
      repere = repere+1

  elif state==12 and l=='n (m)':
    state=13
    repere = 0
  elif state==13 and l!='':
    d['reperes'][repere]['y']=float(l)
    if repere==len(d['reperes'])-1:
      state=14
      repere=0
    else:
      repere = repere+1

  elif state==14 and l=='Précision plani Altitude (m)':
    state=15
  elif state==15:
    if l.find('m')>0:
      p = re.match(r".* (\d+)( |)(m|cm|mm)(| local)$",l)
      pr = int(p.group(1))
      if p.group(3)=='cm':
        pr = pr/100
      if p.group(3)=='mm':
        pr = pr/1000
      d['reperes'][repere]['precision_plani_max']=pr
      if repere==len(d['reperes'])-1:
        state=16
        repere=0
      else:
        repere = repere+1

  elif state==16 and l!='' and l.find('m')==-1:
    try: # au cas où il n'y a pas d'altitude pour le repère (exemple: 1905801.pdf)
      d['reperes'][repere]['z']=float(l)
    except:
      pass
    if repere==len(d['reperes'])-1:
      state=17
      repere=0
    else:
      repere = repere+1

  elif (state==16 or state==17) and l=='Précision alti':
    state=18
  elif state==18:
    if l.find('m')>0:
      p = re.match(r".* (\d+)( |)(m|cm|mm)(| local)$",l)
      pr = int(p.group(1))
      if p.group(3)=='cm':
        pr = pr/100
      if p.group(3)=='mm':
        pr = pr/1000
      d['reperes'][repere]['precision_alti_max']=pr
    if repere==len(d['reperes'])-1:
      state=19
    else:
      repere = repere+1

if sortie=='json':
    print(json.dumps(d,sort_keys=True))
elif sortie == 'csv':
    r = d['reperes']
    del d['reperes']

    for rep in r:
        rep.update(d)
        csvout.writerow(rep)
