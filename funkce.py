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
    kat_int = [('C',0,1000,'rakovina'),
                ('I',0,52,'selhani organu'),
                ('I',60,69,'ostatni paliativni'),
                ('J',40,47,'selhani organu'),
                ('K',70,77,'selhani organu'),
                ('B',20,24,'ostatni paliativni')]
    for (kod, od, do, kat) in kat_int:
        if mkn[0] == kod and od <= int(mkn[1:]) <= do:
            return kat

    kat_mkn = [(['J96','N17','N18','N28'],'selhani organu'),
                (['F01','F03','G30','R54'],'demence'),
                (['G10','G12','G20','G35'],'ostatni paliativni')]
    for (kody, kat) in kat_mkn:
        if mkn in kody:
            return kat

    return 'bez paliativni pece'
    