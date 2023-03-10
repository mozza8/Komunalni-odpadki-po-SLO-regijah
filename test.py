import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from math import pi
from bokeh.transform import cumsum
import numpy as np

df = pd.read_csv('odpadki.csv', sep = ';', encoding='windows-1250')

# pobere tabele iz spletne strani
scraper = pd.read_html('https://sl.wikipedia.org/wiki/Seznam_ob%C4%8Din_v_Sloveniji')


#   Za lociranje tabele, ki jo hočem dobiti:
'''
for index, table in enumerate(scraper):
    print('**************************************************')
    print(index)
    print(table)
'''

# Želim tabelo z indexom 1
tabela = scraper[1]

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

d = vsi.copy()

# normaliziram podatke za posamezne regije
for i in range(len(vsi)):
    d.iloc[i] = vsi.iloc[i].apply(lambda x: (x - vsi.iloc[i].min()) / (vsi.iloc[i].max() - vsi.iloc[i].min()))

data = { 'x': d.loc["Goriška"].index,
         'y1': d.loc["Goriška"],
         'y2': d.loc["Gorenjska"],
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

#source = ColumnDataSource(data=dict(x=d.loc["Goriška"].index, y=d.loc["Goriška"] ))
source = ColumnDataSource(data=data)

p1 = figure(title='Gorenjska', width=470, height=300)
p1.title.text_font_size = "20px"
p1.title.text_font_style = 'bold italic'
p1.background_fill_color = 'lightcyan'
p1.title.text_color = "red"
p1.line(x='x',y='y2', source=source,color='red', line_width=3)
p1.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p2 = figure(title='Goriška', width=470, height=300)
p2.title.text_font_size = "20px"
p2.title.text_color = "blue"
p2.line(x='x',y='y1', source=source,color='blue',line_width=3)
p2.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p3 = figure(title='Jugovzhodna', width=470, height=300)
p3.title.text_font_size = "20px"
p3.title.text_color = "gold"
p3.line(x='x',y='y3', source=source,color='gold', line_width=3)
p3.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p4 = figure(title='Koroška', width=470, height=300)
p4.title.text_font_size = "20px"
p4.title.text_color = "gray"
p4.line(x='x',y='y4', source=source,color='gray', line_width=3)
p4.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p5 = figure(title='Obalno-kraška', width=470, height=300)
p5.title.text_font_size = "20px"
p5.title.text_color = "cyan"
p5.line(x='x',y='y5', source=source,color='cyan', line_width=3)
p5.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p6 = figure(title='Osrednjeslovenska', width=470, height=300)
p6.title.text_font_size = "20px"
p6.title.text_color = "green"
p6.line(x='x',y='y6', source=source,color='green', line_width=3)
p6.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p7 = figure(title='Podravska', width=470, height=300)
p7.title.text_font_size = "20px"
p7.title.text_color = "orange"
p7.line(x='x',y='y7', source=source,color='orange', line_width=3)
p7.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p8 = figure(title='Pomurska', width=470, height=300)
p8.title.text_font_size = "20px"
p8.title.text_color = "brown"
p8.line(x='x',y='y8', source=source,color='brown', line_width=3)
p8.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p9 = figure(title='Posavska', width=470, height=300)
p9.title.text_font_size = "20px"
p9.background_fill_color = 'lightcyan'
p9.title.text_color = "hotpink"
p9.line(x='x',y='y9', source=source,color='hotpink', line_width=3)
p9.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p10 = figure(title='Primorsko-notranjska', width=470, height=300)
p10.title.text_font_size = "20px"
p10.title.text_color = "purple"
p10.line(x='x',y='y10', source=source,color='purple', line_width=3)
p10.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p11 = figure(title='Savinjska', width=470, height=300)
p11.title.text_font_size = "20px"
p11.title.text_color = "magenta"
p11.line(x='x',y='y11', source=source,color='magenta', line_width=3)
p11.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p12 = figure(title='Zasavska', width=470, height=300)
p12.title.text_font_size = "20px"
p12.title.text_color = "skyblue"
p12.line(x='x',y='y12', source=source,color='skyblue', line_width=3)
p12.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)


# TORTNI DIAGRAM - seštejem količine vseh let po regijah
slovar = {}
for i in vsi.index:
    vsota = sum(vsi.loc[i])
    slovar[i] = vsota

# preuredim dataFrame
barve = pd.Series(['red', 'blue', 'gold', 'gray','cyan','green','orange','brown','hotpink','purple','magenta','skyblue'])
data_vsi = pd.Series(slovar).reset_index(name='vsota').rename(columns={'index': 'regija'})
data_vsi['angle'] = data_vsi['vsota']/data_vsi['vsota'].sum() * 2*pi
data_vsi['color'] = barve


p = figure(height=650, width=940, title="Regije po deležih vseh odpadkov", toolbar_location=None,
           tools="hover", tooltips="@regija", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='regija', source=data_vsi)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

grid = gridplot([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12], ncols=4)

show(grid)
show(p)



