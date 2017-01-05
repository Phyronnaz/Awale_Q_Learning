plateau = [3, 3, 9, 6, 3, 3, 2, 2, 2, 2, 2, 2]
prise = 0
perte = 0
joueur = 0


def eval_12(plateau, joueur):
    t = plateau[(joueur) * 6: (1 + joueur) * 6]
    somme = 0
    for k in range(6):
        if t[k] == 1 or t[k] == 2:
            somme += t[k]
    rep = somme / 12
    return (rep)


def eval_krou(plateau, joueur):
    t = plateau[(joueur) * 6: (1 + joueur) * 6]
    maxi = 0
    for k in range(6):
        if t[k] >= 11 - k and t[k] <= 33 - k:  # teste si c'est un krou
            maxi = t[k]
    if maxi == 0:
        return (0)
    else:
        return (1)


def evaluation(plateau, joueur, prise, perte):
    alpha = -0.4
    beta = 0.4
    gamma = 0.1
    delta = -0.1
    entier = prise - perte
    p = plateau
    allier_12 = eval_12(plateau, joueur)  # nombre total de 1-2 chez nous (mauvais)
    adversaire_12 = eval_12(plateau, 1 - joueur)  # nombre total de 1-2 chez l'autre (bon)
    allier_krou = eval_krou(plateau, joueur)  # présence d'un krou sur notre terrain (bon)
    adversaire_krou = eval_krou(plateau, 1 - joueur)  # présence d'un krou chez l'aversaire (mauvais)
    rep = entier + 0.5 + (alpha * allier_12) + (beta * adversaire_12) + (gamma * allier_krou) + (
    delta * adversaire_krou)
    rep = ((1000 * rep) // 1) / 1000
    return (rep)

