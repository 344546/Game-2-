import pygame, sys, math
from pygame.locals import *

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

scale = (1/2)
s_width = 720
s_height = 1280
tile_size = 40
h = 18
#w = 40
#screen sized divided by square sizes must be an integer
#h = int(s_width/pixelw)
w = int(s_width/tile_size)
offset = (s_height/2) - ((h*tile_size)/2)

white = 255, 255, 255
gray = 150, 150, 150
black = 0, 0, 0
blue = 25, 100, 255
green = 50, 150, 10
red = 255, 50, 50

size = (width, height) = (s_width*scale, s_height*scale)

screen = pygame.display.set_mode(size)
bg = pygame.Surface((s_width*scale, s_height*scale))
pygame.Surface.fill(bg, gray)

menu = pygame.Surface((s_width*scale, s_height*scale))

grid = pygame.Surface((s_width*scale, s_width*scale))
grid_rect = grid.get_rect()
grid_rect = pygame.Rect.move(grid_rect, 0, offset*scale)
grid.set_colorkey((255,0,255))
pygame.Surface.fill(grid, (255, 0, 255))

deletion_rect = pygame.Surface((s_width*scale, s_width*scale))
del_rect = deletion_rect.get_rect()
del_rect = pygame.Rect.move(del_rect, 0, offset*scale)
deletion_rect.set_colorkey((255,0,255))
pygame.Surface.fill(deletion_rect, (255, 0, 255))
pygame.draw.rect(deletion_rect, red, (0, 0, s_width*scale, s_width*scale), width = 10)
#ADD TRANSPARENT RECT?

grid_state = [[0] * w for _ in range(h)]
grid_surf_arr = [[] for _ in range(h)]
grid_rect_arr = [[] for _ in range(h)]

grid_surf_list = []
grid_rect_list = []
blit_list = []
k = 0
for i in range(0,h):
  for j in range(0,w):

    pygame.draw.rect(grid, black, (tile_size*j*scale, tile_size*i*scale, tile_size*scale, tile_size*scale), width > 0)
    grid_surf_list.append(pygame.Surface((tile_size*scale, tile_size*scale)))
    pygame.Surface.fill(grid_surf_list[k], white)
    grid_rect_list.append(grid_surf_list[k].get_rect(topleft=(tile_size*j*scale, (tile_size*i)*scale + offset*scale)))
    blit_list.append((grid_surf_list[k], grid_rect_list[k]))

    grid_surf_temp = grid_surf_arr[i]
    grid_surf_temp.append(grid_surf_list[k])

    grid_rect_temp = grid_rect_arr[i]
    grid_rect_temp.append(grid_rect_list[k])
 
    k += 1

towers = []
class Tower:
  def __init__(self, gridspace):
    self.gridspace = gridspace
    #gridspace_pos = (gridspace[0]*tile_size*scale, gridspace[1]*tile_size*scale)

class Wall(Tower):
  dmg = 0
  defence = 25
  cost = 5
  color = gray

class Tower1(Tower):
  dmg = 5
  defence = 5
  radius = tile_size*2*scale
  cost = 10
  color = blue
  speed = 0.5
  timer = int()

class Tower2(Tower):
  dmg = 10
  defence = 10
  radius = tile_size*2*scale
  cost = 20
  color = green
  speed = 0.25
  timer = int()

class AATower(Tower):
  dmg = 10
  defence = 5
  radius = tile_size*3*scale
  cost = 15
  color = red
  speed = 0.125
  timer = int()

enemies = []
enemies_pos = []
class Enemy:
  def __init__(self, start_loc):
    self.start_loc = start_loc
    enemies.append(self)
    temp_surf = pygame.Surface((int(tile_size*scale), int(tile_size*scale)))
    temp_surf.set_colorkey((255,0,255))
    pygame.Surface.fill(temp_surf, (255, 0, 255))
    pygame.draw.circle(temp_surf, black, ((tile_size/2)*scale, (tile_size/2)*scale), (tile_size/2)*scale)
    temp_rect = temp_surf.get_rect(center=start_loc)
    enemies_pos.append((temp_surf, temp_rect))
    
class Enemy1(Enemy):
  defence = 35
  speed = 2
  radius = tile_size*scale

class Enemy2(Enemy):
  defence = 15
  speed = 1
  radius = tile_size*scale*0.9

class Enemy3(Enemy):
  defence = 25
  speed = 2
  radius = tile_size*scale

class EnemyA1(Enemy):
  defence = 10
  speed = 2
  radius = tile_size*scale*0.85

class EnemyA2(Enemy):
  defence = 15
  speed = 3
  radius = tile_size*scale*0.75

tower_list = []
for tower in Tower.__subclasses__():
  tower_list.append(tower)

buttons = pygame.Surface((s_width*scale, offset*scale))
buttons.set_colorkey((255,0,255))
pygame.Surface.fill(buttons, (255, 0, 255))
buttons_rect = pygame.Rect((0, (1280 - offset)*scale), (s_width*scale, offset*scale))
b_rects = []
for i in range(4):
  pygame.draw.rect(buttons, red, ((((s_width/4)*i) + 30)*scale, 70*scale, (s_width/6)*scale, (s_height/10)*scale), 0)

  pygame.draw.rect(buttons, tower_list[i].color, ((((s_width/4)*i) + 60)*scale, 100*scale, (s_width/12)*scale, (s_height/20)*scale), 0)

  pygame.draw.rect(buttons, black, ((((s_width/4)*i) + 60)*scale, 100*scale, (s_width/12)*scale, (s_height/20)*scale), width > 0)

  b_rects.append(pygame.Rect((((s_width/4)*i) + 30)*scale, (s_height - 210)*scale, (s_width/6)*scale, (offset/2)*scale))

next_stage_surf = pygame.Surface((360*scale, 120*scale))
pygame.Surface.fill(next_stage_surf, green)
pygame.draw.rect(next_stage_surf, black, (1, 1, 360*scale - 2, 120*scale - 2), width = 3)
next_stage_rect = next_stage_surf.get_rect(center=(s_width/2*scale, 120*scale))
font_temp = pygame.font.SysFont('Arial', 35, True)
next_text = font_temp.render('Next', False, (0, 0, 0))
next_text_rect = next_text.get_rect(center=next_stage_rect.center)
next_button = ((next_stage_surf, next_stage_rect), (next_text, next_text_rect))

def centRotate(image, pos, originPos, angle):

    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    print(offset_center_to_pivot)
    
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    print(rotated_offset)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    print(rotated_image_center)

    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    return rotated_image, rotated_image_rect

def circleCollision(pos1, pos2, rad1, rad2):
  dist = math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
  if (dist < (rad1 + rad2)):
    return True

text = []
font_temp = pygame.font.SysFont('Arial', 15, True)
for b in range(len(b_rects)):
  if (b == 0):
    t = 'Wall'
    c = str(Wall.cost)
  elif (b == 1):
    t = 'Tower 1'
    c = str(Tower1.cost)
  elif (b == 2):
    t = 'Tower 2'
    c = str(Tower2.cost)
  elif (b == 3):
    t = 'A-A Tower'
    c = str(AATower.cost)
  text_temp = font_temp.render(t, False, (0, 0, 0))

  text_rect = text_temp.get_rect(center=(b_rects[b].centerx, b_rects[b].centery - (s_height/13)*scale))

  text.append((text_temp, text_rect))

  text_temp = font_temp.render(c, False, (0, 0, 0))

  text_rect = text_temp.get_rect(center=(b_rects[b].centerx, b_rects[b].centery + (s_height/16)*scale))

  text.append((text_temp, text_rect))

def main():
  y = 0
  #state = "menu"
  state = 'game'
  selection = None
  money = w*Wall.cost
  enemy_interval = 1/scale
  enemy_interval_counter = 0
  float(enemy_interval_counter)
  #health = 100
  while 1:
    for event in pygame.event.get():
      if event.type == MOUSEBUTTONDOWN:
        if event.button == BUTTON_LEFT:
          pos = pygame.mouse.get_pos()
          if (state == 'game'):
            if (buttons_rect.collidepoint(pos) == True):
              for i in range(len(b_rects)):
                if (b_rects[i].collidepoint(pos) == True):
                  selection = i

            elif (selection in range(len(tower_list))):
              for i in range(len(grid_rect_arr)):
                for j in range(len(grid_rect_arr[0])):
                  if (grid_rect_arr[i][j].collidepoint(pos) and (grid_state[i].count(0) > 1) and (grid_state[i][j] == 0) and (money - tower_list[selection].cost > -1)):
                    pygame.Surface.fill(grid_surf_arr[i][j], tower_list[selection].color)
                    grid_state[i][j] = tower_list[selection]((i, j))
                    towers.append(grid_state[i][j])
                    money = money - tower_list[selection].cost

            elif (selection == 4):
              for i in range(len(grid_rect_arr)):
                for j in range(len(grid_rect_arr[0])):
                  if (grid_rect_arr[i][j].collidepoint(pos) and (grid_state[i][j] != 0)):
                    pygame.Surface.fill(grid_surf_arr[i][j], white)
                    money = money + grid_state[i][j].cost
                    towers.remove(grid_state[i][j])
                    grid_state[i][j] = 0

            elif (len(enemies) == 0 and next_stage_rect.collidepoint(pos)):
              pass

        elif event.button == BUTTON_RIGHT:
          if (selection != 4):
            selection = 4
          else:
            selection = None

      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()
        if event.key == K_0:
          Enemy1((360*scale, 0))
        if event.key == K_9:
          print(grid_state)
    for tower in towers:
      i = 0
      for enemy in enemies:
        if (tower.dmg != 0):
          pos1 = grid_rect_arr[tower.gridspace[0]][tower.gridspace[1]].center
          pos2 = enemies_pos[i][1].center
          rad1 = tower.radius
          rad2 = enemy.radius
          if (circleCollision(pos1, pos2, rad1, rad2)):
            if (pygame.time.get_ticks() >= tower.timer + tower.speed*1000):
              tower.timer = pygame.time.get_ticks()
              print(y)
              y += 1
              enemy.defence = enemy.defence - tower.dmg
              if (enemy.defence <= 0):
                enemies.remove(enemy)
                del enemy
                enemies_pos.pop(i)
        i += 1
    for e in range(len(enemies)):
      if (len(enemies_pos) != 0 and enemies_pos[e][1].colliderect(buttons_rect)):
        pass

      if (enemy_interval_counter == enemy_interval):
        if (len(enemies_pos) != 0):
          enemies_pos[e][1].move_ip(-2, 2)
    
    screen.fill(white)
    screen.blit(bg, (0, 0))
    if (state == "game"):
      screen.blits(blit_list)
      screen.blit(grid, grid_rect)
      screen.blit(buttons, buttons_rect)
      screen.blits(text)
      screen.blits(enemies_pos)
      if (len(enemies) == 0):
        screen.blits(next_button)
      if (selection == 4):
        screen.blit(deletion_rect, del_rect)
    elif (state == "menu"):
      pass
    
    if (enemy_interval_counter == enemy_interval):
      enemy_interval_counter = 0
    enemy_interval_counter = enemy_interval_counter + 1.0
    pygame.display.flip()
    clock.tick(60)
    

main()