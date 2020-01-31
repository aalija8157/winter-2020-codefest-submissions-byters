import pygame, sys
import os
from sprites import *

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1500,900)
current_path = os.path.dirname(__file__)
imgpath = os.path.join(current_path, 'img/')
SPRITE_SHEET = imgpath + "bear-polar.png"
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
spritesheet = Spritesheet(SPRITE_SHEET)
display = pygame.Surface((500,300)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
current_frame = 0
last_update = 0
last_facing = "right"
true_scroll = [0, 0]
message_blocks = []
curr_msg = []
msg_time = 0
spawn = [100, 100]

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    i = 0
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map(current_path + '/map')
standing_frames = [spritesheet.get_image(0, 7, 31, 20),
                   spritesheet.get_image(32, 7, 31, 20),
                   spritesheet.get_image(64, 7, 31, 20)]
left_standing = []
for frame in standing_frames:
    frame.set_colorkey((0, 0, 0))
    left_standing.append(pygame.transform.flip(frame, True, False))
for frame in left_standing:
    frame.set_colorkey((0, 0, 0))
walk_frames_r = [spritesheet.get_image(96, 7, 31, 20),
                 spritesheet.get_image(128, 7, 31, 20),
                 spritesheet.get_image(160, 7, 31, 20),
                 spritesheet.get_image(192, 7, 31, 20),
                 spritesheet.get_image(224, 7, 31, 20)]
for frame in walk_frames_r:
    frame.set_colorkey((0, 0, 0))
walk_frames_l = []
for frame in walk_frames_r:
    walk_frames_l.append(pygame.transform.flip(frame, True, False))

for frame in walk_frames_l:
    frame.set_colorkey((0, 0, 0))

snow_img = pygame.image.load(imgpath + 'snow.png')
plat_img = pygame.image.load(imgpath + "plat.png")
water_img = pygame.image.load(imgpath + "water.jpg")
hint_img = pygame.image.load(imgpath + "hint.png")
flag_img = pygame.image.load(imgpath + "flag.png")
water_img = pygame.transform.scale(water_img, (16, 16))
plat_img = pygame.transform.scale(plat_img, (16, 16))
snow_img = pygame.transform.scale(snow_img, (16, 16))
player_img = spritesheet.get_image(0, 7, 31, 20)
player_img.set_colorkey((0, 0, 0))
messages = [["Watch out!", "Sometimes the ice under you will break and you will fall in the water!", "Make sure you hit these blocks in the future, they give facts that you need to defeat the level!"],
            ["Did you know that glaciers are rapidly melting?", "The main cause of this is the increase of carbon dioxide", "and other greenhouse gasses"]]
player_rect = pygame.Rect(100,100,31,20)

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)

    for tile in hit_list:
        if tile[1] != '4':
            if movement[0] > 0:
                rect.right = tile[0].left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile[0].right
                collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if tile[1] != '4':
            if movement[1] > 0:
                rect.bottom = tile[0].top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile[0].bottom
                collision_types['top'] = True
        if tile[1] == '5':
            break_ice(tile[0].x//16, tile[0].y//16, tile)
        if tile[1] == '6':
            global curr_msg
            curr_msg = tile
        if tile[1] == '4':
            rect.x = spawn[0]
            rect.y = spawn[1]
        if tile[1] == '7':
            spawn[0] = rect.x
            spawn[1] = rect.y
    return rect, collision_types

def break_ice(x, y, tile):
    game_map[y][x] = '0'

def display_msg(tile):
    if len(tile) == 0:
        return
    msg = " \n"
    for r in message_blocks:
        if r[0]*16 == tile[0].x and r[1]*16 == tile[0].y:
            msg = r[2]

    font = pygame.font.Font(pygame.font.match_font('arial'), 14)
    i = 0
    for s in msg:
        text_surface = font.render(s, True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WINDOW_SIZE[0]/6.17, tile[0].y + i * 15)
        display.blit(text_surface, text_rect)
        i += 1

while True: # game loop

    display.fill((146,244,255)) # clear screen by filling it with blue
    true_scroll[0] += (player_rect.x - true_scroll[0] - 252)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 150)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    tile_rects = []
    y = 0
    msgidx = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            strn = ''
            if tile == '1':
                display.blit(snow_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '5':
                display.blit(snow_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(plat_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '4':
                display.blit(water_img, (x*16-scroll[0],y*16-scroll[1]))
            if tile == '6':
                display.blit(hint_img, (x*16-scroll[0],y*16-scroll[1]))
                message_blocks.append((x, y, messages[msgidx]))
                msgidx += 1
            if tile == '7':
                display.blit(flag_img, (x*16 - scroll[0], y*16 - scroll[1]))
            if tile != '0':
                tile_rects.append((pygame.Rect(x*16,y*16,16,16), tile))
            x += 1
        y += 1
    if len(curr_msg) != 0:
        msg_time += 1
    display_msg(curr_msg)
    if msg_time > 140:
        curr_msg = []
        msg_time = 0
    now = pygame.time.get_ticks()
    if moving_right:
        if now - last_update > 200:
            last_update = now
            current_frame = (current_frame + 1) % len(walk_frames_r)
            player_img = walk_frames_r[current_frame]
            last_facing = "right"
    if moving_left:
        if now - last_update > 200:
            last_update = now
            current_frame = (current_frame + 1) % len(walk_frames_l)
            player_img = walk_frames_l[current_frame]
            last_facing = "left"
    if not moving_right and not moving_left:
        if now - last_update > 350:
            last_update = now
            if last_facing == "right":
                current_frame = (current_frame + 1) % len(standing_frames)
                player_img = standing_frames[current_frame]
            else:
                current_frame = (current_frame + 1) % len(left_standing)
                player_img = left_standing[current_frame]

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    if collisions ['top'] == True:
        vertical_momentum = 0
    else:
        air_timer += 1

    if player_rect.y > WINDOW_SIZE[1]:
        player_rect.x = 100
        player_rect.y = 100
    display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
