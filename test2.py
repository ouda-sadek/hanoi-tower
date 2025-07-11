import pygame, sys, time

pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Paramètres
n_disks = 3
n_towers = 3
towers_midx = []

# État du jeu
steps = 0
disks = []
pointing_at = 0
floating = False
floater = 0

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78,162,196)
grey = (170, 170, 170)
green = (77, 206, 145)

def blit_text(screen, text, midtop, aa=True, font=None, font_name=None, size=None, color=(255,0,0)):
    if font is None:
        font = pygame.font.SysFont(font_name, size)
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def draw_towers():
    global towers_midx
    spacing = 640 // (n_towers + 1)
    towers_midx = []
    for i in range(n_towers):
        midx = spacing * (i + 1)
        towers_midx.append(midx)
        pygame.draw.rect(screen, green, pygame.Rect(midx - 80, 400, 160, 20))
        pygame.draw.rect(screen, grey, pygame.Rect(midx - 5, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[-1], 403), font_name='mono', size=14, color=black)

def draw_disks():
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])

def draw_ptr():
    if pointing_at < len(towers_midx):
        midx = towers_midx[pointing_at]
        points = [(midx - 7, 440), (midx + 7, 440), (midx, 433)]
        pygame.draw.polygon(screen, red, points)

def make_disks():
    global disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {
            'rect': pygame.Rect(0, 0, width, height),
            'val': n_disks - i,
            'tower': 0
        }
        disk['rect'].midtop = (towers_midx[0], ypos)
        disks.append(disk)
        ypos -= height + 3
        width -= 23

def check_won():
    if all(d['tower'] == n_towers - 1 for d in disks):
        screen.fill(white)
        draw_towers()
        draw_disks()
        blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
        blit_text(screen, 'Steps: ' + str(steps), (320, 350), font_name='mono', size=30, color=black)
        pygame.display.flip()
        time.sleep(2)
        reset()

def reset():
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    draw_towers()  # ← ESSENTIEL pour éviter crash ENTER
    make_disks()

def menu_screen():
    global n_disks, n_towers
    menu = True
    while menu:
        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (320, 100), font_name='sans serif', size=72, color=gold)
        blit_text(screen, 'Disks: ' + str(n_disks), (320, 200), font_name='mono', size=30, color=black)
        blit_text(screen, 'Use ←/→ to change disks (1-6)', (320, 230), font_name='mono', size=20, color=black)
        blit_text(screen, 'Towers: ' + str(n_towers), (320, 280), font_name='mono', size=30, color=black)
        blit_text(screen, 'Use Z/S to change towers (3-6)', (320, 310), font_name='mono', size=20, color=black)
        blit_text(screen, 'Press ENTER to start', (320, 370), font_name='mono', size=24, color=red)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                elif event.key == pygame.K_LEFT:
                    n_disks = max(1, n_disks - 1)
                elif event.key == pygame.K_RIGHT:
                    n_disks = min(6, n_disks + 1)
                elif event.key == pygame.K_z:
                    n_towers = min(6, n_towers + 1)
                elif event.key == pygame.K_s:
                    n_towers = max(3, n_towers - 1)
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
        pygame.display.flip()
        clock.tick(30)

# === Lancement ===
reset()

# === Boucle de jeu ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            elif event.key == pygame.K_q:
                pygame.quit(); sys.exit()
            elif event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at + 1) % n_towers
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            elif event.key == pygame.K_LEFT:
                pointing_at = (pointing_at - 1) % n_towers
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            elif event.key == pygame.K_UP and not floating:
                for disk in reversed(disks):
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            elif event.key == pygame.K_DOWN and floating:
                target_disks = [d for d in disks if d['tower'] == pointing_at and disks.index(d) != floater]
                if not target_disks:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400 - 23)
                    disks[floater]['tower'] = pointing_at
                    floating = False
                    steps += 1
                else:
                    top = target_disks[-1]
                    if disks[floater]['val'] < top['val']:
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], top['rect'].top - 23)
                        disks[floater]['tower'] = pointing_at
                        floating = False
                        steps += 1

    screen.fill(white)
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, 'Steps: ' + str(steps), (320, 20), font_name='mono', size=30, color=black)
    pygame.display.flip()

    if not floating:
        check_won()
    clock.tick(60)
