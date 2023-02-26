import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
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

# naredim kopijo data Frama
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

#p = figure(title="Goriška", x_axis_label="Leta", y_axis_label="Interval", width=1750, height=900)
p1 = figure(title='Goriška')
p1.title.text_font_size = "20px"
p1.title.text_color = "blue"
p1.line(x='x',y='y1', source=source,color='blue',line_width=3)
p1.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p2 = figure(title='Gorenjska')
p2.title.text_font_size = "20px"
p2.title.text_font_style = 'bold italic'
p2.background_fill_color = 'lightcyan'
p2.title.text_color = "red"
p2.line(x='x',y='y2', source=source,color='red', line_width=3)
p2.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p3 = figure(title='Jugovzhodna')
p3.title.text_font_size = "20px"
p3.title.text_color = "gold"
p3.line(x='x',y='y3', source=source,color='gold', line_width=3)
p3.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p4 = figure(title='Koroška')
p4.title.text_font_size = "20px"
p4.title.text_color = "gray"
p4.line(x='x',y='y4', source=source,color='gray', line_width=3)
p4.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p5 = figure(title='Obalno-kraška')
p5.title.text_font_size = "20px"
p5.title.text_color = "cyan"
p5.line(x='x',y='y5', source=source,color='cyan', line_width=3)
p5.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p6 = figure(title='Osrednjeslovenska')
p6.title.text_font_size = "20px"
p6.title.text_color = "green"
p6.line(x='x',y='y6', source=source,color='green', line_width=3)
p6.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p7 = figure(title='Podravska')
p7.title.text_font_size = "20px"
p7.title.text_color = "orange"
p7.line(x='x',y='y7', source=source,color='orange', line_width=3)
p7.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p8 = figure(title='Pomurska')
p8.title.text_font_size = "20px"
p8.title.text_color = "brown"
p8.line(x='x',y='y8', source=source,color='brown', line_width=3)
p8.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p9 = figure(title='Posavska')
p9.title.text_font_size = "20px"
p9.background_fill_color = 'lightcyan'
p9.title.text_color = "hotpink"
p9.line(x='x',y='y9', source=source,color='hotpink', line_width=3)
p9.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p10 = figure(title='Primorsko-notranjska')
p10.title.text_font_size = "20px"
p10.title.text_color = "purple"
p10.line(x='x',y='y10', source=source,color='purple', line_width=3)
p10.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p11 = figure(title='Savinjska')
p11.title.text_font_size = "20px"
p11.title.text_color = "magenta"
p11.line(x='x',y='y11', source=source,color='magenta', line_width=3)
p11.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

p12 = figure(title='Zasavska')
p12.title.text_font_size = "20px"
p12.title.text_color = "skyblue"
p12.line(x='x',y='y12', source=source,color='skyblue', line_width=3)
p12.line(x='x',y='y13', source=source,color='black',legend_label="Slovenija", line_width=3)

grid = gridplot([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12], ncols=4, width=470, height=300)

show(grid)






