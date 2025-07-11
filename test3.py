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

# Auto mode
auto_mode = False
auto_moves = []
auto_timer = 0
auto_delay = 300
auto_started_at = 0
auto_start_delay = 1000
auto_ending = False
auto_end_time = 0
auto_end_delay = 2000
blink = False
blink_timer = 0
blink_interval = 300

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

def solve_hanoi(n, source, target, auxiliary):
    if n == 1:
        auto_moves.append((source, target))
    else:
        solve_hanoi(n-1, source, auxiliary, target)
        auto_moves.append((source, target))
        solve_hanoi(n-1, auxiliary, target, source)

def execute_auto_move():
    global steps
    if not auto_moves:
        return
    from_tower, to_tower = auto_moves.pop(0)
    for disk in reversed(disks):
        if disk['tower'] == from_tower:
            moving = disk
            break
    new_top = 400 - 23
    for disk in reversed(disks):
        if disk['tower'] == to_tower and disk != moving:
            new_top = disk['rect'].top - 23
            break
    moving['rect'].midtop = (towers_midx[to_tower], new_top)
    moving['tower'] = to_tower
    steps += 1

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
    global auto_mode, auto_moves, auto_ending
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    auto_mode = False
    auto_ending = False
    auto_moves.clear()
    menu_screen()
    draw_towers()
    make_disks()

def menu_screen():
    global n_disks, n_towers
    menu = True
    while menu:
        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (320, 100), font_name='sans serif', size=72, color=gold)
        blit_text(screen, 'Disks: ' + str(n_disks), (320, 200), font_name='mono', size=30, color=black)
        blit_text(screen, '←/→ Disks (1-6)', (320, 230), font_name='mono', size=20, color=black)
        blit_text(screen, 'Towers: ' + str(n_towers), (320, 280), font_name='mono', size=30, color=black)
        blit_text(screen, 'Z/S Towers (3-6)', (320, 310), font_name='mono', size=20, color=black)
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
            elif event.key == pygame.K_a and not auto_mode:
                if n_towers == 3:
                    auto_mode = True
                    auto_started_at = pygame.time.get_ticks()
                    auto_moves.clear()
                    solve_hanoi(n_disks, 0, 2, 1)
            elif not auto_mode:
                if event.key == pygame.K_RIGHT:
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

    now = pygame.time.get_ticks()
    if auto_ending:
        blit_text(screen, 'Résolution terminée', (320, 150), font_name='mono', size=40, color=gold)
        if now - blink_timer > blink_interval:
            blink = not blink
            blink_timer = now
        for disk in disks:
            pygame.draw.rect(screen, gold if blink else blue, disk['rect'])
    else:
        draw_disks()

    draw_ptr()
    blit_text(screen, 'Steps: ' + str(steps), (320, 20), font_name='mono', size=30, color=black)
    if n_towers == 3:
        blit_text(screen, 'Press A for auto-solve', (320, 50), font_name='mono', size=20, color=red)
    else:
        blit_text(screen, 'Auto-mode ', (320, 50), font_name='mono', size=20, color=grey)

    pygame.display.flip()

    if not floating and auto_mode:
        if now - auto_started_at > auto_start_delay:
            if auto_moves and now - auto_timer > auto_delay:
                execute_auto_move()
                auto_timer = now
            elif not auto_moves and not auto_ending:
                auto_ending = True
                auto_end_time = now
            elif auto_ending and now - auto_end_time > auto_end_delay:
                auto_mode = False
                auto_ending = False
                check_won()

    if not floating and not auto_mode and not auto_ending:
        check_won()

    clock.tick(60)
