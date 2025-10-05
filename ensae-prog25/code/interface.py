import pygame
import random
from grid import Grid

import sys
sys.path.append("code/")

class interface_jeu_solo:
    def __init__(self,solver):
        pygame.init()
        self.grid = None
        self.etat = "accueil"
        self.largeur_case = 50
        self.hauteur_case = 50
        pygame.display.set_caption("Jeu solo")
        self.fenetre = pygame.display.set_mode((800, 600))
        self.score = 0
        self.grille_jamais_vus = [5]
        self.selection = []
        self.paires = []
        self.cases_vus = []
        self.texte_saisi = ""  # Pour numéro de grille
        self.saisie_active = True
        self.erreur_message = None
        self.erreur_timestamp = None
        self.logo = pygame.image.load("logo.png")  # Remplace par ton chemin si nécessaire
        self.logo = pygame.transform.scale(self.logo, (150, 150))  # Redimensionne proprement
        self.Solver = solver
        self.score_optimal = None
        self.matching_optimal = []
        self.afficher_solution = False

    def generer_grille_aleatoire(self):
        i = random.randint(0, len(self.grille_jamais_vus) - 1)
        numero_grille = self.grille_jamais_vus[i]
        if numero_grille < 10:
            self.grid = Grid.grid_from_file(f"input/grid0{numero_grille}.in", read_values=True)
        else:
            self.grid = Grid.grid_from_file(f"input/grid{numero_grille}.in", read_values=True)
        self.grille_jamais_vus.pop(i)
        self.fenetre = pygame.display.set_mode((self.grid.m * self.largeur_case, self.grid.n * self.hauteur_case))
        self.selection = []
        self.paires = []
        self.cases_vus = [[False] * self.grid.m for _ in range(self.grid.n)]

    def charger_grille_depuis_numero(self, numero):
        try:
            numero = int(numero)
            if numero < 10:
                path = f"input/grid0{numero}.in"
            else:
                path = f"input/grid{numero}.in"
            self.grid = Grid.grid_from_file(path, read_values=True)
            self.fenetre = pygame.display.set_mode((self.grid.m * self.largeur_case, self.grid.n * self.hauteur_case))
            self.selection = []
            self.paires = []
            self.cases_vus = [[False] * self.grid.m for _ in range(self.grid.n)]
            return True
        except:
            self.erreur_message = "Grille introuvable"
            self.erreur_timestamp = pygame.time.get_ticks()
            return False


    def dessiner_grille(self):
        self.fenetre.fill((255, 255, 255))
        pygame.display.set_caption("Appuyer sur Entrée une fois fini")
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                couleur = self.grid.color[i][j]
                couleur_correspondante = [(255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0)][couleur]
                if self.cases_vus[i][j]:
                    facteur_gris = 0.7
                    new_couleur = tuple(int(c * (1 - facteur_gris) + 150 * facteur_gris) for c in couleur_correspondante)
                else:
                    new_couleur = couleur_correspondante

                rect = pygame.Rect(j * self.largeur_case, i * self.hauteur_case, self.largeur_case, self.hauteur_case)
                pygame.draw.rect(self.fenetre, new_couleur, rect)
                pygame.draw.rect(self.fenetre, (0, 0, 0), rect, 2)

                if (i, j) in self.selection:
                    pygame.draw.rect(self.fenetre, (255, 165, 0), rect, 3)

                if couleur < 4:
                    font = pygame.font.Font(None, 30)
                    texte = font.render(str(self.grid.value[i][j]), True, (0, 0, 0))
                    self.fenetre.blit(texte, (j * self.largeur_case + self.largeur_case // 2, i * self.hauteur_case + self.hauteur_case // 2))
        pygame.display.flip()

    def case_clique(self, position):
        x, y = position
        j = x // self.largeur_case
        i = y // self.hauteur_case
        if 0 <= i < self.grid.n and 0 <= j < self.grid.m:
            return i, j
        return None

    def gerer_clic(self, position):
        case = self.case_clique(position)
        if case is None:
            return
        if self.cases_vus[case[0]][case[1]]:
            if len(self.selection) == 0:
                i, j = case
                index = 0
                r = True
                while r:
                    (i1, j1), (i2, j2) = self.paires[index]
                    if (i1, j1) == (i, j) or (i2, j2) == (i, j):
                        for (ii, jj) in [(i1, j1), (i2, j2)]:
                            couleur = self.grid.color[ii][jj]
                            couleur_corr = [(255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0)][couleur]
                            rect = pygame.Rect(jj * self.largeur_case, ii * self.hauteur_case, self.largeur_case, self.hauteur_case)
                            pygame.draw.rect(self.fenetre, couleur_corr, rect)
                            pygame.draw.rect(self.fenetre, (0, 0, 0), rect, 2)
                        self.cases_vus[i1][j1] = False
                        self.cases_vus[i2][j2] = False
                        pygame.display.flip()
                        r = False
                    index += 1
            else:
                self.selection = []
                return

        if case in self.selection:
            self.selection.pop(0)
        else:
            self.selection.append(case)
        if len(self.selection) == 2:
            (i1, j1), (i2, j2) = self.selection
            if self.grid.pair_color((i1, j1), (i2, j2)) and (abs(i1 - i2) + abs(j1 - j2)) == 1:
                self.paires.append(((i1, j1), (i2, j2)))
                self.cases_vus[i1][j1] = True
                self.cases_vus[i2][j2] = True
            self.selection = []

    def calculer_score_final(self):
        s = 0
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if not self.cases_vus[i][j] and self.grid.color[i][j] != 4:
                    s += self.grid.value[i][j]
        for x in self.paires:
            s += self.grid.cost(x)
        self.score = s

    def dessiner_accueil(self):
        self.fenetre = pygame.display.set_mode((800, 600))
        self.fenetre.fill((0, 0, 0))  # Fond noir
        pygame.display.set_caption("ColorMatch")

        # Polices
        font = pygame.font.Font(None, 40)
        small_font = pygame.font.Font(None, 30)

        # Afficher le logo avec une marge en haut
        logo_rect = self.logo.get_rect(center=(400, 100))  # Position Y ajustée ici
        self.fenetre.blit(self.logo, logo_rect)

        # Titre du jeu
        titre = font.render("Bienvenue dans ColorMatch !", True, (255, 255, 255))
        titre_rect = titre.get_rect(center=(400, 190))  # En dessous du logo
        self.fenetre.blit(titre, titre_rect)

        # Instruction 1 : jouer aléatoirement
        texte_alea = small_font.render("Appuyez sur ESPACE pour une grille aléatoire", True, (255, 255, 255))
        texte_alea_rect = texte_alea.get_rect(center=(400, 250))
        self.fenetre.blit(texte_alea, texte_alea_rect)

        # Instruction 2 : saisir un numéro
        texte_saisie = small_font.render("Ou entrez un numéro de grille et appuyez sur Entrée :", True, (255, 255, 255))
        texte_saisie_rect = texte_saisie.get_rect(center=(400, 290))
        self.fenetre.blit(texte_saisie, texte_saisie_rect)

        # Champ de saisie
        input_box = pygame.Rect(350, 320, 100, 50)
        pygame.draw.rect(self.fenetre, (255, 255, 255), input_box)
        texte_saisi_render = font.render(self.texte_saisi, True, (0, 0, 0))
        self.fenetre.blit(texte_saisi_render, (input_box.x + 10, input_box.y + 10))

        # Message d'erreur si besoin
        if self.erreur_message and self.erreur_timestamp:
            if pygame.time.get_ticks() - self.erreur_timestamp < 3000:
                erreur_font = pygame.font.Font(None, 28)
                texte_erreur = erreur_font.render(self.erreur_message, True, (255, 0, 0))
                self.fenetre.blit(texte_erreur, texte_erreur.get_rect(center=(400, 390)))
            else:
                self.erreur_message = None  # On efface après 3s

        pygame.display.flip()



    def dessiner_fin(self):
        self.fenetre = pygame.display.set_mode((800, 600))
        self.fenetre.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        small_font = pygame.font.Font(None, 30)
        pygame.display.set_caption("Partie terminée")

        # Score du joueur
        score_texte = font.render(f"Score final : {self.score}", True, (255, 255, 255))
        self.fenetre.blit(score_texte, (200, 150))

        # Score optimal si disponible
        result=self.Solver(self.grid)
        result.run()
        self.score_optimal = result.score()
        self.matching_optimal = result.pairs
        optimal_texte = small_font.render(f"Score optimal : {self.score_optimal}", True, (0, 255, 0))
        self.fenetre.blit(optimal_texte, (200, 210))

        # Instructions
        self.fenetre.blit(small_font.render("Appuyez sur R pour rejouer", True, (255, 255, 255)), (200, 300))
        self.fenetre.blit(small_font.render("Appuyez sur Q pour quitter", True, (255, 255, 255)), (200, 340))
        self.fenetre.blit(small_font.render("Appuyez sur O pour voir la solution optimale", True, (255, 255, 255)), (200, 380))

        pygame.display.flip()


    def ajuster_taille_case(self):
        max_largeur = self.fenetre.get_width() // self.grid.m
        max_hauteur = self.fenetre.get_height() // self.grid.n
        taille_max = min(max_largeur, max_hauteur, 80)  # Limite pour éviter texte illisible
        self.largeur_case = taille_max
        self.hauteur_case = taille_max


    def dessiner_solution_optimale(self):
        self.ajuster_taille_case()  # Adapter la taille selon la grille
        offset_x = (self.fenetre.get_width() - self.grid.m * self.largeur_case) // 2
        offset_y = (self.fenetre.get_height() - self.grid.n * self.hauteur_case) // 2
        self.fenetre.fill((255, 255, 255))
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                couleur = self.grid.color[i][j]
                couleur_correspondante = [(255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0)][couleur]
                rect = pygame.Rect(offset_x +j * self.largeur_case, offset_y+i * self.hauteur_case, self.largeur_case, self.hauteur_case)
                pygame.draw.rect(self.fenetre, couleur_correspondante, rect)
                pygame.draw.rect(self.fenetre, (0, 0, 0), rect, 2)

                if couleur < 4:
                    font = pygame.font.Font(None, 30)
                    texte = font.render(str(self.grid.value[i][j]), True, (0, 0, 0))
                    self.fenetre.blit(texte, (offset_x +j * self.largeur_case + self.largeur_case // 2, offset_y+i * self.hauteur_case + self.hauteur_case // 2))

        # Dessin des flèches pour chaque paire optimale
        for (i1, j1), (i2, j2) in self.matching_optimal:
            x1 = offset_x+j1 * self.largeur_case + self.largeur_case // 2
            y1 = offset_y+i1 * self.hauteur_case + self.hauteur_case // 2
            x2 = offset_x+j2 * self.largeur_case + self.largeur_case // 2
            y2 = offset_y+i2 * self.hauteur_case + self.hauteur_case // 2

            pygame.draw.line(self.fenetre, (0, 0, 0), (x1, y1), (x2, y2), 3)

            # Flèche finale
            dx, dy = x2 - x1, y2 - y1
            norm = max((dx**2 + dy**2)**0.5, 1)
            ux, uy = dx / norm, dy / norm
            pygame.draw.line(self.fenetre, (0, 0, 0), (x2, y2), (x2 - 10 * ux - 5 * uy, y2 - 10 * uy + 5 * ux), 2)
            pygame.draw.line(self.fenetre, (0, 0, 0), (x2, y2), (x2 - 10 * ux + 5 * uy, y2 - 10 * uy - 5 * ux), 2)

        pygame.display.set_caption("Solution optimale (R pour rejouer, Q pour quitter)")
        pygame.display.flip()







    def run(self):
        running = True
        dernier_etat_affiche = None  # Pour éviter de redessiner en boucle

        while running:
            besoin_redessiner = False  # On redessine seulement si besoin

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # === ÉTAT ACCUEIL ===
                    if self.etat == "accueil":
                        if event.key == pygame.K_SPACE:
                            self.generer_grille_aleatoire()
                            self.etat = "jeu"
                        elif event.key == pygame.K_RETURN and self.texte_saisi.isdigit():
                            if self.charger_grille_depuis_numero(self.texte_saisi):
                                self.etat = "jeu"
                            else:
                                besoin_redessiner = True  # Afficher le message d'erreur
                        elif event.key == pygame.K_BACKSPACE:
                            self.texte_saisi = self.texte_saisi[:-1]
                            besoin_redessiner = True
                        elif event.unicode.isdigit():
                            self.texte_saisi += event.unicode
                            besoin_redessiner = True

                    # === ÉTAT JEU ===
                    elif self.etat == "jeu" and event.key == pygame.K_RETURN:
                        self.etat = "fin"
                        self.calculer_score_final()

                    # === ÉTAT FIN ===
                    elif self.etat == "fin":
                        if event.key == pygame.K_r:
                            self.texte_saisi = ""
                            self.etat = "accueil"
                        elif event.key == pygame.K_q:
                            running = False
                        elif event.key == pygame.K_o:
                            self.etat = "solution"
                    #==Etat Solution==
                    elif self.etat == "solution":
                        if event.key == pygame.K_r:
                            self.texte_saisi = ""
                            self.etat = "accueil"
                        elif event.key == pygame.K_q:
                            running = False            

                elif event.type == pygame.MOUSEBUTTONDOWN and self.etat == "jeu":
                    self.gerer_clic(event.pos)
                    self.dessiner_grille()

            # On redessine l'accueil uniquement si l'état change ou s'il y a une erreur / saisie
            if self.etat == "accueil":
                if self.etat != dernier_etat_affiche or besoin_redessiner:
                    self.dessiner_accueil()
            elif self.etat == "jeu":
                if self.etat != dernier_etat_affiche:
                    self.dessiner_grille()
            elif self.etat == "fin":
                if self.etat != dernier_etat_affiche:
                    self.dessiner_fin()
            elif self.etat == "solution":
                if self.etat != dernier_etat_affiche:
                    self.dessiner_solution_optimale()        

            dernier_etat_affiche = self.etat