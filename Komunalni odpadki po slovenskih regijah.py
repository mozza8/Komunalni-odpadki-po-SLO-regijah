import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, Axis
from bokeh.models import BasicTickFormatter
from bokeh.transform import transform
from bokeh.layouts import gridplot
from math import pi
from bokeh.transform import cumsum
import numpy as np

df = pd.read_csv('odpadki.csv', sep = ';', encoding='windows-1250')

'''
# pobere tabele iz spletne strani in shrani csv
scraper = pd.read_html('https://sl.wikipedia.org/wiki/Seznam_ob%C4%8Din_v_Sloveniji')
scraper[1].to_csv('regije.csv', encoding='windows-1250')
'''

# odpre datoteko
tabela = pd.read_csv('regije.csv', encoding='windows-1250')

# Združitev serij Občina in Statistična regija v nov dataframe
regija = pd.DataFrame(tabela['Statistična regija'])
regija['OBČINE'] = tabela['Občina']

# pokaže vse vrstice
pd.set_option('display.max_rows', None)
# pokaže vse stolpce
pd.set_option('display.max_columns', None)

# prvotnem dataframeu odstranim vrstico SLOVENIJA, da lahko potem združim dataframe
brez_slo = df.drop(0).reset_index(drop=True)

# sprememba imen ključev, da bo bolj pregledno
for a in brez_slo.keys():
    if len(a) > 8:
        #brez_slo = brez_slo.rename(columns={a:f'Odpadki_{a[:4]}'})
        brez_slo = brez_slo.rename(columns={a: f'{a[:4]}'})
        df = df.rename(columns={a: f'{a[:4]}'})

# združitev dataframov
skupna = pd.merge(regija, brez_slo, on=['OBČINE'])

# zamenjam podatke, kjer ni podatka, dodam 0   -->  NI podatka, ker prej še ni bila samostojna občina, tako da so količine teh občin dodane prvotnim občininam, regija pa je enaka
for x in skupna.keys():
    for i in skupna.index:
        if skupna.loc[i, x] == '-':
            skupna.loc[i, x] = 0

# vse številske podatke spremenim v integer
for x in skupna.keys():
    if x == 'Statistična regija' or x == 'OBČINE':
        continue
    skupna[x] = skupna[x].astype(int)
    #df[x] = df[x].astype(int)

# seštejem količine po regijah in ustvarim nov DataFrame
vsi = skupna.groupby(by = 'Statistična regija').sum(numeric_only=True)

# normaliziram podatke za slovenijo
slo = df.loc[0][1:]
slo = slo.astype(int)
normalized_slo = slo.apply(lambda x: (x - slo.min()) / (slo.max() - slo.min()))

# naredim kopijo dataframea da deluje naslednja funkcija
d = vsi.copy()

# normaliziram podatke za posamezne regije
for i in range(len(vsi)):
    d.iloc[i] = vsi.iloc[i].apply(lambda x: (x - vsi.iloc[i].min()) / (vsi.iloc[i].max() - vsi.iloc[i].min()))

# -------------------------------------------------------Grafi komunalnih odpadkov normalizirano---------------------------------------------------------------------------

data = { 'x': d.loc["Goriška"].index,
         'y1': d.loc["Gorenjska"],
         'y2': d.loc["Goriška"],
         'y3': d.loc["Jugovzhodna"],
         'y4': d.loc["Koroška"],
         'y5': d.loc["Obalno-kraška"],
         'y6': d.loc["Osrednjeslovenska"],
         'y7': d.loc["Podravska"],
         'y8': d.loc["Pomurska"],
         'y9': d.loc["Posavska"],
         'y10': d.loc["Primorsko-notranjska"],
         'y11': d.loc["Savinjska"],
         'y12': d.loc["Zasavska"],
         'y13': normalized_slo
}

source = ColumnDataSource(data=data)

p1 = figure(title='Gorenjska', width=500, height=340)
p1.title.text_font_size = "18px"
p1.title.text_color = "red"
p1.line(x='x',y='y1', source=source,color='red', line_width=3)
p1.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p2 = figure(title='Goriška', width=500, height=340)
p2.title.text_font_size = "18px"
p2.title.text_color = "blue"
p2.line(x='x',y='y2', source=source,color='blue',line_width=3)
p2.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p5 = figure(title='Obalno-kraška', width=500, height=340)
p5.title.text_font_size = "18px"
p5.title.text_color = "cyan"
p5.line(x='x',y='y5', source=source,color='cyan', line_width=3)
p5.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p6 = figure(title='Osrednjeslovenska', width=500, height=340)
p6.title.text_font_size = "18px"
p6.title.text_color = "green"
p6.line(x='x',y='y6', source=source,color='green', line_width=3)
p6.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p7 = figure(title='Podravska', width=500, height=340)
p7.title.text_font_size = "18px"
p7.title.text_color = "orange"
p7.line(x='x',y='y7', source=source,color='orange', line_width=3)
p7.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p11 = figure(title='Savinjska', width=500, height=340)
p11.title.text_font_size = "18px"
p11.title.text_color = "magenta"
p11.line(x='x',y='y11', source=source,color='magenta', line_width=3)
p11.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

# ----------------------------------------------------------------TORTNI DIAGRAM - seštejem količine vseh let po regijah-------------------------------------------------------------------------

# vsota količine smeti za vsa leta
slovar = {}
for i in vsi.index:
    vsota = sum(vsi.loc[i])
    slovar[i] = vsota

# preuredim dataFrame
barve = pd.Series(['red', 'blue', 'gold', 'gray','cyan','green','orange','brown','hotpink','purple','magenta','skyblue'])
data_vsi = pd.Series(slovar).reset_index(name='vsota').rename(columns={'index': 'regija'})
data_vsi['angle'] = data_vsi['vsota']/data_vsi['vsota'].sum() * 2*pi
data_vsi['color'] = barve

# sortiranje vsot po velikosti
data_vsi = data_vsi.sort_values(by=['vsota'], ascending=False)

# računanje procentnega deleža
vsota_vsi = data_vsi['vsota'].sum()
data_vsi['procent'] = round((data_vsi['vsota'] / vsota_vsi) * 100,2)

hover = HoverTool(tooltips=[('language','@regije'),('percentage', '@procent')])


p = figure(height=550, width=740, title="Regije po deležih vseh odpadkov", toolbar_location=None,
           tooltips=str('@procent %'),tools="click", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color',fill_alpha = 0.8, legend_field='regija', source=data_vsi)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

# ---------------------------------------------------------------------uvozim datoteko s prebivalci-------------------------------------------------------------------

datoteka = pd.read_csv('prebivalci.csv', encoding='windows-1250')

# odstranim nepotrebne vrstice
prebivalci = datoteka.drop(0).reset_index(drop=True)
prebivalci = prebivalci.drop(212).reset_index(drop=True)

# imena občin spremenim v obliko, da bo enaka ostalim dataframom
prebivalci['OBČINE'] = brez_slo['OBČINE']

# združim dataframe s statističnimi regijami
prebivalstvo = pd.merge(regija, prebivalci, on=['OBČINE'])
prebivalstvo = prebivalstvo.drop(['Unnamed: 0'], axis=1)

f = prebivalstvo.copy()

# zamenjam podatke, kjer ni podatka, dodam 0   -->  NI podatka, ker prej še ni bila samostojna občina, tako da so količine teh občin dodane prvotnim občininam, regija pa je enaka
for x in prebivalstvo.keys():
    if x == 'Statistična regija' or x == 'OBČINE':
        continue
    f[x] = prebivalstvo[x].str.replace('.', '')
    for i in prebivalstvo.index:
        if f.loc[i, x] == '-':
            f.loc[i, x] = 0

# vse številske podatke spremenim v float
for x in prebivalstvo.keys():
    if x == 'Statistična regija' or x == 'OBČINE':
        continue
    f[x] = f[x].astype(int)

# seštejem količine po regijah in ustvarim nov DataFrame
po_regijah = f.groupby(by = 'Statistična regija').sum(numeric_only=True)

# ustvarim slovar
dict = {}
for i in po_regijah.index:
    vsota = int(round(sum(po_regijah.loc[i]) / 15))
    dict[i] = vsota

# preuredim dataFrame
barve = pd.Series(['red', 'blue', 'gold', 'gray','cyan','green','orange','brown','hotpink','purple','magenta','skyblue'])
data_preb = pd.Series(dict).reset_index(name='vsota').rename(columns={'index': 'regija'})
data_preb['angle'] = data_preb['vsota']/data_preb['vsota'].sum() * 2*pi
data_preb['color'] = barve

# sortiranje vsot po velikosti
data_preb = data_preb.sort_values(by=['vsota'], ascending=False)

# računam deleže usake regije
vsota_vseh = data_preb['vsota'].sum()
data_preb['procent'] = round((data_preb['vsota'] / vsota_vseh) * 100,2)

# ------------------------------------------------------------------------TORTNI DIAGRAM Prebivalci---------------------------------------------------------------------------------------

pre = figure(height=550, width=740, title="Regije po številu prebivalcev", toolbar_location=None,
           tools="click", tooltips=str('@procent %'), x_range=(-0.5, 1.0))

pre.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_alpha=0.8, fill_color='color', legend_field='regija', source=data_preb)

pre.axis.axis_label = None
pre.axis.visible = False
pre.grid.grid_line_color = None


# -----------------------------------------------------------------PODATKI zaposlenih------------------------------------------------------------

file = pd.read_csv('zaposleni.csv', delimiter = ';', encoding='windows-1250')
#frame = file.drop(0).reset_index(drop=True)
frame = file


zaposleni = frame.groupby(by='regije').sum(numeric_only=True)
z = zaposleni.copy()

# normalizacija števila zaposlenih po regijah
for i in range(len(zaposleni)):
    z.iloc[i] = zaposleni.iloc[i].apply(lambda x: (x - zaposleni.iloc[i].min()) / (zaposleni.iloc[i].max() - zaposleni.iloc[i].min()))


#--------------------------------------------------------------------------Grafi odpadkov v povezavi z zaposlenimi-----------------------------------------------------------------------

# podatki za nove linearne grafe - primerjava med zaposlenimi in količinami odpadkov po regijah
podatki= { 'x': normalized_slo[3:].index,
         'y1': d.loc["Gorenjska"][3:],
         'y_1': z.loc["Gorenjska"][:-1],

         'y2': d.loc["Goriška"][3:],
         'y_2': z.loc["Goriška"][:-1],

         'y3': d.loc["Jugovzhodna"][3:],
         'y_3': z.loc["Jugovzhodna"][:-1],

         'y4': d.loc["Koroška"][3:],
         'y_4': z.loc["Koroška"][:-1],

         'y5': d.loc["Obalno-kraška"][3:],
         'y_5': z.loc["Obalno-kraška"][:-1],

         'y6': d.loc["Osrednjeslovenska"][3:],
         'y_6': z.loc["Osrednjeslovenska"][:-1],

         'y7': d.loc["Podravska"][3:],
         'y_7': z.loc["Podravska"][:-1],

         'y8': d.loc["Pomurska"][3:],
         'y_8': z.loc["Pomurska"][:-1],

         'y9': d.loc["Posavska"][3:],
         'y_9': z.loc["Posavska"][:-1],

         'y10': d.loc["Primorsko-notranjska"][3:],
         'y_10': z.loc["Primorsko-notranjska"][:-1],

         'y11': d.loc["Savinjska"][3:],
         'y_11': z.loc["Savinjska"][:-1],

         'y12': d.loc["Zasavska"][3:],
         'y_12': z.loc["Zasavska"][:-1],

         'y13': normalized_slo[3:],
         'y_13': z.loc['SLOVENIJA'][:-1]
}


source2 = ColumnDataSource(data=podatki)

f1 = figure(title='Gorenjska', width=500, height=340)
f1.title.text_font_size = "20px"
f1.title.text_color = "red"
f1.line(x='x',y='y_1', source=podatki,color='red', legend_label="Zaposleni", line_width=3)
f1.line(x='x',y='y1', source=podatki,color='black',legend_label="Odpadki", line_width=3)
f1.legend.location = "top_center"

f2 = figure(title='Goriška', width=500, height=340)
f2.title.text_font_size = "20px"
f2.title.text_color = "blue"
f2.line(x='x',y='y_2', source=podatki,color='blue', legend_label="Zaposleni", line_width=3)
f2.line(x='x',y='y2', source=podatki,color='black',legend_label="Odpadki", line_width=3)
f2.legend.location = "top_center"

f5 = figure(title='Obalno-kraška', width=500, height=340)
f5.title.text_font_size = "20px"
f5.title.text_color = "cyan"
f5.line(x='x',y='y_5', source=podatki,color='cyan', legend_label="Zaposleni", line_width=3)
f5.line(x='x',y='y5', source=podatki,color='black',legend_label="Odpadki", line_width=3)
f5.legend.location = "top_center"

f6 = figure(title='Osrednjeslovenska', width=500, height=340)
f6.title.text_font_size = "20px"
f6.title.text_color = "green"
f6.line(x='x',y='y_6', source=podatki,color='green', legend_label="Zaposleni", line_width=3)
f6.line(x='x',y='y6', source=podatki,color='black',legend_label="Odpadki", line_width=3)
f6.legend.location = "top_center"

f7 = figure(title='Podravska', width=500, height=340)
f7.title.text_font_size = "20px"
f7.title.text_color = "orange"
f7.line(x='x',y='y_7', source=podatki,color='orange', legend_label="Zaposleni", line_width=3)
f7.line(x='x',y='y7', source=podatki,color='black',legend_label="Odpadki", line_width=3)
f7.legend.location = "top_center"

f11 = figure(title='Savinjska', width=500, height=340)
f11.title.text_font_size = "20px"
f11.title.text_color = "magenta"
f11.line(x='x',y='y_11', source=podatki,color='magenta', legend_label="Zaposleni", line_width=3)
f11.line(x='x',y='y11', source=podatki,color='black',legend_label="Odpadki", line_width=3)
f11.legend.location = "top_center"

f13 = figure(title='Slovenija', width=1250, height=700)
f13.title.text_font_size = "20px"
f13.title.text_color = "teal"
f13.line(x='x',y='y_13', source=podatki,color='teal',legend_label="Zaposleni" ,line_width=3)
f13.line(x='x',y='y13', source=podatki,color='black',legend_label="Odpadki", line_width=3)
f13.legend.location = "top_center"

# grid grafov zaposleni v odpadki
gridF=gridplot([f1,f2,f5,f6,f7,f11], ncols=3)

# pruredim dataframe da dobim enake letnice pri obeh
vsi_brez = vsi.iloc[:,6:]                 #      Odpadki po regijah od leta 2008 do 2021
preb_brez = po_regijah.iloc[:,:-1]        #      Prebivalci brez slovenije od leta 2008 do 2021
print('----------------------------------------------------------------------------------------------------------')
print(vsi_brez)
print('----------------------------------------------------------------------------------------------------------')

# naredim dva slovarja, da lahko potem ustvarim nova dataframa , računam povprečja regij po letih
slovar_brez = {}
slovar2 = {}
for i in vsi_brez.index:
    vsota = int(sum(vsi_brez.loc[i]) / 14)
    sestevek = int(sum(preb_brez.loc[i]) / 14)
    slovar_brez[i] = vsota
    slovar2[i] = sestevek

# slovarje spremenim v dataframe in dodam stolpce
barve = pd.Series(['red', 'blue', 'gold', 'gray','cyan','green','orange','brown','hotpink','purple','magenta','skyblue'])
data_smeti = pd.Series(slovar_brez).reset_index(name='vsota_povp').rename(columns={'index': 'regija'})
data_prebivalci = pd.Series(slovar2).reset_index(name='sestevek_povp').rename(columns={'index': 'regija'})
data_smeti['color'] = barve

# dataframa združim v skupen dataframe
together = pd.merge(data_smeti, data_prebivalci, on=['regija'])

# dodam nov stolpec z razmerji
together['na_prebivalca(tone)'] = together['vsota_povp'] / together['sestevek_povp']

# sortiram po velikosti prebivalcev
together = together.sort_values(by=['vsota_povp'], ascending=False)
print(together)

# -----------------------------------------------------------------------------------BUBBLE GRAF------------------------------------------------------------------------------------

# Ustvarim podatke za Bubble graf, izbiram le prvih 6 regij
novi = {'Prebivalci': together["sestevek_povp"].head(6),
        'Odpadki': together["vsota_povp"].head(6),
        'Imena': together["regija"].head(6),
        'Razmerje': together["na_prebivalca(tone)"].head(6) * 300,
        'Na_prebivalca': together["na_prebivalca(tone)"].head(6),
        #'xrange' : list(range(42000,546000,42000)),
        'color' : together['color'].head(6)
        }
dframe = pd.DataFrame(data = novi)
source3 = ColumnDataSource(dframe)

TOOLTIPS = [
    ("Ton na prebivalca","@Na_prebivalca"),
    ("Število prebivalcev", "@Prebivalci"),
    ("Količina odpadkov(v tonah)","@Odpadki")
]

s = figure(title = 'Količina odpadkov(tone) na prebivalca v letih od 2008 do 2021', x_axis_label='Število prebivalcev', x_range=(0,650000),y_axis_label='Količina odpadkov(v tonah)',y_range=(0,250000), width=1300, tooltips=TOOLTIPS)
s.xaxis.formatter = BasicTickFormatter(use_scientific=False)
s.yaxis.formatter = BasicTickFormatter(use_scientific=False)
s.circle(x = 'Prebivalci', y = 'Odpadki', size = 'Razmerje', legend_group='Imena', fill_color = 'color', fill_alpha=0.6, line_color='black', source = source3)
s.legend.location = "top_left"
p.legend.title = "Regije"


# gridi za prikaz na html
grid = gridplot([p1,p2,p5,p6,p7,p11],ncols=3)
grid.name = "Količine odpadkov skozi leta"
grid2 = gridplot([p,pre], ncols=2)
grid3 = gridplot([grid, grid2, s, gridF, f13], ncols=1)

show(grid3)


