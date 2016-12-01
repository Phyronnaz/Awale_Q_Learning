def evaluation(total_prise, total_perte):
    return total_prise - total_perte


plateau = [1, 1, 3, 4, 1, 1, 1, 5, 4, 4, 0, 0]


def creer_arbre_elag(h: int) -> list:
    l = []
    for i in range(0, h + 1):
        l.append([])
    return l


def jouer_score_elag(plat, trou, joueur, jlocal, prise, perte, pere, hole):
    rep = []
    for k in range(len(plat)):
        rep.append(plat[k])

    graine = rep[trou]

    if jlocal == 0:
        zone_adverse = [6, 7, 8, 9, 10, 11]
    else:
        zone_adverse = [0, 1, 2, 3, 4, 5]

    good = [2, 3]
    correction = graine // 12
    for k in range(1, graine + 1 + correction):  # modifie le plateau
        rep[(trou + k) % 12] += 1
    rep[trou] = 0
    arrivee = (trou + graine + correction) % 12

    score = 0
    h = 0
    while ((arrivee - h) in zone_adverse) and (rep[arrivee - h] in good):
        score += rep[arrivee - h]  # compte et enleve du plateau les nouvelles prises
        rep[arrivee - h] = 0
        h += 1
    if jlocal == joueur:
        prise_rep = prise + score
        perte_rep = perte
    else:
        perte_rep = perte + score
        prise_rep = prise

    res = [rep, joueur, jlocal, prise_rep, perte_rep]  # retourne le plateau, les prise totales et les pertes totales
    return res


def descente_elag(plateau, h, joueur):
    rep = creer_arbre_elag(h)
    prise0 = 0
    perte0 = 0
    rep[0].append([plateau, joueur, 1 - joueur, prise0, perte0, 0,0])
    tree = creer_arbre_elag(h)
    for i in range(0, h):
        for j in range(0, len(rep[i])):
            plat = rep[i][j][0]
            player = 1 - rep[i][j][2]
            prise = rep[i][j][3]
            perte = rep[i][j][4]
            trou = []
            for k in range(6 * player, 6 * (player + 1)):
                if plat[k] != 0:
                    trou.append(k)
            for l in trou:
                config = jouer_score_elag(plat, l, joueur, player, prise, perte, j, l)
                rep[i + 1].append(config)
                if i + 1 != h:
                    tree[i + 1].append([0,j, l])
                else:
                    tree[i + 1].append([prise-perte,j,l])
    return rep, tree


a, b = descente_elag(plateau, 1, 1)

def remonter(arb):
    n =len(arb)
    for i in range (n-1,0,-1):
        j=0
        pere = arb[i][j][1]
        m = arb[i][j][0]
        while j<2**i:
            j+=1
            if pere==arb[i][j][1]:
                if i%2 ==1:
                    m=max(m,arb[i][j][0])
                else:
                    m=min(m,arb[i][j][0])
            else:
                arb[i-1][pere][0]=m
                pere=arb[i][j][1]
    return(arb[1])

print(remonter(b))