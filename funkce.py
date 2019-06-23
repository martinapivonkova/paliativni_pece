#funkce dostane seznam cisel a spocita koeficienty rustu/poklesu
#pokud seznam obsahuje 0, koeficient rustu je 1 (neklesa, neroste)
def koeficienty(seznam):
    seznam = [float(i) for i in seznam]
    koeficienty = []
    if 0 in seznam:
        for i in range(len(seznam)):
            seznam[i] = 1
    for i in range(len(seznam)-1):
        koeficienty.append(round(seznam[i+1]/seznam[i],6))
    return koeficienty

#funkce dostane seznam cisel a spocita geometricky prumer
def geom_prumer(seznam):
    soucin = 1
    for i in seznam:
        soucin = soucin*i
    gprumer = soucin**(1/len(seznam))
    seznam = [float(i) for i in seznam]
    seznam.append(gprumer)
    return seznam

#funkce dostane kod MKN a priradi mu "paliativni" kategorii nemoci
def paliativni_kat(mkn):
    pal_kat = 'bez paliativni pece'
    if mkn.startswith('C'): 
        pal_kat = 'rakovina'
    if mkn.startswith('I'):
        if int(mkn[1:]) >= 0 and int(mkn[1:]) <= 52:
            pal_kat = 'selhani organu'
        if int(mkn[1:]) >= 60 and int(mkn[1:]) <= 69:
            pal_kat = 'ostatni paliativni'
    if mkn.startswith('J'):
        if int(mkn[1:]) >= 40 and int(mkn[1:]) <= 47:
            pal_kat = 'selhani organu'
    if mkn in ['J96','N17','N18','N28']:
            pal_kat = 'selhani organu'
    if mkn.startswith('K'):
        if int(mkn[1:]) >= 70 and int(mkn[1:]) <= 77:
            pal_kat = 'selhani organu'
    if mkn in ['F01','F03','G30','R54']:
            pal_kat = 'demence'
    if mkn in ['G10','G12','G20','G35']:
            pal_kat = 'ostatni paliativni'
    if mkn.startswith('B'):
        if int(mkn[1:]) >= 20 and int(mkn[1:]) <= 24:
            pal_kat = 'ostatni paliativni'
    return pal_kat
