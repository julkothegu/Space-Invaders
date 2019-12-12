import pygame
import random

pygame.init()

class projectile(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class enemies(object):
    enemies = []
    enemy_bullets = []
    def __init__(self, enemy_num, diff, enemy_size, width, height, alien_sprite1, alien_sprite1_1, alien_sprite2):
        self.enemy_num = enemy_num
        self.diff = diff
        self.enemy_s = enemy_size
        self.width = width
        self.height = height
        self.dirnx = 1
        self.enemy_speed = 0.25
        self.timer = 0
        self.bullet_color = (95, 53, 203)
        self.score = 0
        self.alien_sprite1 = alien_sprite1
        self.alien_sprite1_1 = alien_sprite1_1
        self.alien_sprite2 = alien_sprite2
        self.anim_timer = 0
        self.remainder = 0

    def add_enemies(self):
        if len(self.enemies) < self.enemy_num:
            for enemy in range(0, self.enemy_num):
                self.enemies.append([self.alien_sprite1, self.alien_sprite1_1, enemy * (self.enemy_s*2), 200])
                self.enemies.append([self.alien_sprite1, self.alien_sprite1_1, enemy * (self.enemy_s*2), 250])
                self.enemies.append([self.alien_sprite1, self.alien_sprite1_1, enemy * (self.enemy_s*2), 300])

    def e_timer(self):
        self.anim_timer += 1
        if self.anim_timer % 30 == 0:
            self.remainder = 0
        elif self.anim_timer % 15 == 0:
            self.remainder = 1

    def draw(self, surface):
        for enemy in self.enemies:
            surface.blit(enemy[self.remainder], (enemy[2], (enemy[3])))

    def check_pos(self):
        for enemy in self.enemies:
            if enemy[2] > self.width - self.enemy_s:
                self.dirnx = -self.enemy_speed
                self.move_down()
            elif enemy[2] < 0:
                self.dirnx = self.enemy_speed
                self.move_down()

    def move_down(self):
        for enemy in self.enemies:
            enemy[3] += 10

    def update_pos(self):
        for enemy in self.enemies:
            enemy[2] += self.dirnx

    def remove_enemy(self, index):
        del self.enemies[index]

    def next_level(self):
        if len(self.enemies) == 0:
            self.increase_diff()
            self.add_enemies()

    def increase_diff(self):
        self.enemy_speed += 0.10

    def get_bullet(self, posl):
        return projectile(posl[2], posl[3], (95, 53, 203))

    def random_bullet(self, surface):
        self.enemy_timer()
        if self.timer == 0:
            if len(self.enemy_bullets) < 5:
                pos = random.randint(0, (self.enemy_num * 3) - 1)
                try:
                    posl = self.enemies[pos]
                    bullet = self.get_bullet(posl)
                    self.enemy_bullets.append(bullet)
                except IndexError:
                    pass

    def enemy_timer(self):
        if self.timer > 0:
            self.timer += 1
        if self.timer > 45:
            self.timer = 0

    def draw_bullet(self, surface):
        for bullet in self.enemy_bullets:
            pygame.draw.circle(surface, bullet.color, (int(bullet.x), int(bullet.y)), 5, 5)

        self.timer += 1

    def update_bullets(self):
        for idx, bullet in enumerate(self.enemy_bullets):
            bullet.y += 20
            if bullet.y > self.height + 10:
                self.enemy_bullets.pop(idx)

    def collision(self, playerx, playery, enemy_s):
        for idx, bullet in enumerate(self.enemy_bullets):

                p_x = int(bullet.x)
                p_y = int(bullet.y)

                e_x = playerx
                e_y = playery

                if e_x >= p_x and e_x < (p_x + 10) or p_x >= e_x and p_x < (e_x + enemy_s):
                    if e_y >= p_y and e_y < (p_y + 10) or p_y >= e_y and p_y < (e_y + enemy_s):
                        return True
        return False

    def reset(self, lives):
        self.enemies = []
        self.enemy_bullets = []

    def draw_score(self, surface, score):
        pygame.font.init()
        font = pygame.font.SysFont('Verdana', 20, bold=True)
        label = font.render('Score: ' + str(score), 1, (184, 178, 20))

        surface.blit(label, (800 - 130, 1000 - 50))

    def increase_score(self):
        if ship.collision(ship, self.enemies, self.enemy_s):
            self.score += 1

    def gameOver(self):
        pass

class ship():
    bullets = []
    def __init__(self, x, y, color, enemy_s, surface, lives, enemies, width, height, player_sprite):
        self.x = x
        self.y = y
        self.color = color
        self.dirny = 0
        self.shoot_loop = 0
        self.enemy_s = enemy_s
        self.surface = surface
        self.lives = lives
        self.score = enemies.score
        self.width = width
        self.height = height
        self.player = player_sprite

    def draw_all(self, surface, ship_size):
        surface.blit(self.player, (self.x, self.y))

    def he_liva(self, score):
        x = int(self.x)
        y = int(self.y)
        if enemies.collision(enemies, x, y, self.enemy_s):
            self.lives -= 1
            enemies.reset(enemies, self.lives)
            self.x = self.width / 2
            self.y = self.height - 100
        enemies.draw_score(enemies, self.surface, score)

    def move(self):
        keys = pygame.key.get_pressed()

        for key in keys:
            if keys[pygame.K_LEFT]:
                self.x -= 0.15
            if keys[pygame.K_RIGHT]:
                self.x += 0.15
            if keys[pygame.K_UP]:
                self.y -= 0.15
            if keys[pygame.K_DOWN]:
                self.y += 0.15
            if keys[pygame.K_SPACE] and self.shoot_loop == 0 and len(self.bullets) < 10:
                bullet = self.get_bullet()
                self.bullets.append(bullet)
                self.shoot_loop += 1

    def get_bullet(self):
        return projectile(self.x, self.y, (181, 53, 14))

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            pygame.draw.circle(surface, bullet.color, (int(bullet.x), int(bullet.y)), 5, 5)

    def update_bullets(self):
        for idx, bullet in enumerate(self.bullets):
            bullet.y -= 20
            if bullet.y < 0 - 10:
                self.bullets.pop(idx)

    def bullet_timer(self):
        if self.shoot_loop > 0:
            self.shoot_loop += 1
        if self.shoot_loop > 10:
            self.shoot_loop = 0

    def collision(self, henemies, enemy_s):
        for idx, bullet in enumerate(self.bullets):
            for idx2, enemy in enumerate(henemies):

                p_x = int(bullet.x)
                p_y = int(bullet.y)

                e_x = enemy[2]
                e_y = enemy[3]

                if e_x >= p_x and e_x < (p_x + 10) or p_x >= e_x and p_x < (e_x + enemy_s):
                    if e_y >= p_y and e_y < (p_y + 10) or p_y >= e_y and p_y < (e_y +   enemy_s):
                        enemies.remove_enemy(enemies, idx2)
                        self.bullets.pop(idx)
                        return True

        return False

    def reset(self):
        self.lives = 3
        self.x = self.width / 2
        self.y = self.height - 100

def main():
    lives = 3
    width = 800
    height = 1000
    ship_size = 35
    difficulty = 0
    enemy_number = 10
    enemy_size = 35
    screen = pygame.display.set_mode((width, height))
    enemy_list = 12
    run = True
    clock = pygame.time.Clock()

    player_sprite = pygame.image.load('player_sprite1.png').convert()
    player_sprite = pygame.transform.scale(player_sprite, (35, 35))
    player_sprite.set_colorkey((243,0,194))
    alien_sprite1 = pygame.image.load('alien_sprite1.png').convert()
    alien_sprite1 = pygame.transform.scale(alien_sprite1, (35, 35))
    alien_sprite1.set_colorkey((243,0,194))
    alien_sprite1_1 = pygame.image.load('alien_sprite1_1.png').convert()
    alien_sprite1_1 = pygame.transform.scale(alien_sprite1_1, (35, 35))
    alien_sprite1_1.set_colorkey((243,0,194))
    alien_sprite2 = pygame.image.load('alien_sprite2.png').convert()
    alien_sprite2 = pygame.transform.scale(alien_sprite2, (35, 35))
    alien_sprite2.set_colorkey((243,0,194))

    aliens = enemies(enemy_number, difficulty, enemy_size, width, height, alien_sprite1, alien_sprite1_1, alien_sprite2)
    player = ship(width / 2, height - 100, (255, 0, 0), enemy_size, screen, lives, aliens, width, height, player_sprite)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
        screen.fill((0, 0, 0))
        player.draw_all(screen, ship_size)
        player.move()

        score = aliens.score
        lives = player.lives

        if lives < 0:
            aliens.score = 0
            player.lives = 3
            print(lives)

        player.he_liva(score)
        player.draw_bullets(screen)
        player.update_bullets()
        player.bullet_timer()
        aliens.draw(screen)
        aliens.check_pos()
        aliens.update_pos()
        aliens.next_level()
        aliens.random_bullet(screen)
        aliens.draw_bullet(screen)
        aliens.update_bullets()
        aliens.increase_score()
        aliens.e_timer()
        clock.tick(30)
        pygame.display.update()

main()








