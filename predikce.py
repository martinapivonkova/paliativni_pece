import pandas
import sys
from funkce import paliativni_kat, koeficienty, geom_prumer
pandas.set_option("display.max_rows", 1000)

vstup_zemreli = sys.argv[1]             #'vstupy/zemreli2011-2017.csv'
vstup_obyvatele = sys.argv[2]           #'vstupy/obyvatele2011-2017.csv'
vstup_predikce_obyvatele = sys.argv[3]  #'vstupy/predikce_stredni.csv'
vystup_predikce_zemreli = sys.argv[4]   #'vystupy/predikce_dle_vyvoje_gp_stredni.csv'

zemreli = pandas.read_csv(vstup_zemreli, encoding='utf-8')
zemreli['rok'] = zemreli['rok'].apply(str)
#v tabulce zemrelych jsou jednotlive roky pod sebou, presuneme je z radek do sloupecku
tabulka = zemreli.pivot_table(index=['MKN','pohlavi','vekova_kategorie'],values = 'pocet_umrti', columns='rok').reset_index()
tabulka = tabulka.fillna(0)
#funkce paliativni_kat priradi kazde nemoci dle MKN paliativni kategorii
kategorie = tabulka['MKN'].apply(paliativni_kat)
#pridame do tabulky sloupecek s paliativni kategorii
tabulka['pal_kat'] = kategorie
#seskupime nemoci do paliativnich kategorii
zemreli = tabulka.groupby(['pal_kat','pohlavi','vekova_kategorie'])[['2011','2012','2013','2014','2015','2016','2017']].sum()
zemreli = zemreli.reset_index()

demence = zemreli[zemreli['pal_kat']=='demence'].reset_index().iloc[:,1:]
rakovina = zemreli[zemreli['pal_kat']=='rakovina'].reset_index().iloc[:,1:]
selhani_organu = zemreli[zemreli['pal_kat']=='selhani organu'].reset_index().iloc[:,1:]
ostatni_paliativni = zemreli[zemreli['pal_kat']=='ostatni paliativni'].reset_index().iloc[:,1:]
bez_paliativni_pece = zemreli[zemreli['pal_kat']=='bez paliativni pece'].reset_index().iloc[:,1:]

obyvatele = pandas.read_csv(vstup_obyvatele, index_col=0, encoding='utf-8')

predikce_dle_vyvoje_p = pandas.DataFrame()
seznam_df = [demence, rakovina, selhani_organu, ostatni_paliativni,bez_paliativni_pece]
for df in seznam_df:
    #prevedeme absolutni cisla zemrelych na procenta z poctu obyvatel
    procenta = pandas.DataFrame()
    rok = 2011
    for i in range(7):
        procenta[str(rok+i)] = (df[str(rok+i)] / obyvatele[str(rok+i)] * 1000).round(6)
    
    #funkce koeficienty vypocita koeficienty mezirocniho rustu
    koeficienty_p = procenta.apply(koeficienty, axis=1, result_type='expand')
    
    #funkce koeficienty_gp vypocita GEOMETRICKY prumer koeficientu a prida do noveho sloupecku
    koeficienty_gp = koeficienty_p.apply(geom_prumer, axis=1, result_type='expand')
    prumer = koeficienty_gp.iloc[:,6]

    #pro predikci vezmeme procenta zemrelych v roce 2017 a budeme nasobit prumerem koeficientu
    rok = 2017
    predikce_p = procenta.loc[:,['2017']]
    for i in range(13):
        predikce_p[str(rok+i+1)] = predikce_p.iloc[:,i]*prumer
    rok = 2018
    for i in range(13):
        predikce_p.loc[predikce_p[str(rok+i)] < 0, str(rok+i)] = 0

    #predikci procent zemrelych napasujeme na predikci poctu obyvatel z CSU
    predikce_obyvatel = pandas.read_csv(vstup_predikce_obyvatele, index_col=0, encoding='utf-8')
    predikce_zemreli_p = pandas.DataFrame()
    rok = 2018
    for i in range(13):
        predikce_zemreli_p[str(rok+i)] = ((predikce_p[str(rok+i)] * predikce_obyvatel[str(rok+i)]) / 1000).round()

    predikce_zemreli_p['pohlavi'] = predikce_obyvatel['pohlavi']
    predikce_zemreli_p['vek_kat'] = predikce_obyvatel['vekova_kategorie']
    predikce_zemreli_p['pal_kat'] = df['pal_kat']

    predikce_dle_vyvoje_p = pandas.concat([predikce_dle_vyvoje_p,predikce_zemreli_p])
        
#print(predikce_dle_vyvoje_p)
predikce_dle_vyvoje_p.to_csv(vystup_predikce_zemreli)
