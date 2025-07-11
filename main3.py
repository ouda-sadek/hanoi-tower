import pygame, sys, time

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Chargement du son d'applaudissements (optionnel)
try:
    applause_sound = pygame.mixer.Sound("assets/applause.wav")
except:
    applause_sound = None

# game vars:
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

# auto mode vars
auto_mode = False
auto_moves = []
auto_timer = 0
auto_delay = 300
auto_started_at = 0
auto_start_delay = 1000
auto_ending = False
auto_end_time = 0
auto_end_delay = 2000

# animation
blink = False
blink_timer = 0
blink_interval = 300

# colors:
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

def menu_screen():
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:
        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (323,122), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Towers of Hanoi', (320,120), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=blue)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks = min(n_disks+1, 6)
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks = max(n_disks-1, 1)
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()
        clock.tick(60)

def game_over():
    global screen, steps
    screen.fill(white)
    min_steps = 2**n_disks-1
    blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'Your Steps: '+str(steps), (320, 360), font_name='mono', size=30, color=black)
    blit_text(screen, 'Minimum Steps: '+str(min_steps), (320, 390), font_name='mono', size=30, color=red)
    if min_steps==steps:
        blit_text(screen, 'You finished in minimum steps!', (320, 300), font_name='mono', size=26, color=green)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def draw_towers():
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160 , 20))
        pygame.draw.rect(screen, grey, pygame.Rect(xpos+75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)

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
        disk['rect'].midtop = (120, ypos)
        disks.append(disk)
        ypos -= height + 3
        width -= 23

def draw_disks():
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)

def check_won():
    if all(disk['tower'] == 2 for disk in disks):
        time.sleep(0.2)
        game_over()

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
    make_disks()

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

menu_screen()
make_disks()

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
                auto_mode = True
                auto_started_at = pygame.time.get_ticks()
                auto_moves.clear()
                solve_hanoi(n_disks, 0, 2, 1)
                if applause_sound:
                    applause_sound.play()
            elif not auto_mode:
                if event.key == pygame.K_RIGHT:
                    pointing_at = (pointing_at + 1) % 3
                    if floating:
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                        disks[floater]['tower'] = pointing_at
                elif event.key == pygame.K_LEFT:
                    pointing_at = (pointing_at - 1) % 3
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
                    for disk in reversed(disks):
                        if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                            if disk['val'] > disks[floater]['val']:
                                floating = False
                                disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                                steps += 1
                            break
                    else:
                        floating = False
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400 - 23)
                        steps += 1

    screen.fill(white)
    draw_towers()

    now = pygame.time.get_ticks()

    if auto_ending:
        # Message et clignotement
        blit_text(screen, 'Résolution terminée', (320, 150), font_name='mono', size=40, color=gold)
        if now - blink_timer > blink_interval:
            blink = not blink
            blink_timer = now
        for disk in disks:
            color = gold if blink else blue
            pygame.draw.rect(screen, color, disk['rect'])
    else:
        draw_disks()

    draw_ptr()
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    blit_text(screen, 'Press A for auto-solve', (320, 50), font_name='mono', size=20, color=red)
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
