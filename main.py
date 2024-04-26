import sys
import pgzrun
import pygame
import random
from ctypes import windll

from pgzero import clock
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.loaders import sounds


def hide_mushroom():
    mushroom.x = -200
    mushroom.y = -200


def show_mushroom():
    actor_random_location(mushroom)
    clock.schedule(hide_mushroom, 3)


def enemy_random_direction():
    enemy.dx = random.randint(-3, 3)
    enemy.dy = random.randint(-3, 3)


def exit_func():
    quit()


def actor_location_correct(actor):
    if actor.x < -actor.width // 2:
        actor.x = WIDTH + actor.width // 2
    if actor.x > WIDTH + actor.width // 2:
        actor.x = -actor.width // 2
    if actor.y < -actor.height // 2:
        actor.y = HEIGHT + actor.height // 2
    if actor.y > HEIGHT + actor.height // 2:
        actor.y = -actor.height // 2


def on_key_down():
    global status, timer
    if keyboard.SPACE and status == "home":
        status = "play"
        clock.schedule_interval(enemy_random_direction, 10)
        clock.schedule_interval(show_mushroom, 10)
    if keyboard.ESCAPE:
        status = "end"
        clock.schedule(exit_func, 5)
    if keyboard.f:
        mod.screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    if keyboard.n:
        mod.screen.surface = pygame.display.set_mode((WIDTH, HEIGHT))

    if keyboard.r:
        status = "play"
        mario.score = 0
        luigi.score = 0
        timer = 100
        actor_location_correct(mario)
        actor_location_correct(luigi)
        actor_location_correct(enemy)


def draw():
    if status == "home":
        mod.screen.blit("home", (0, 0))
        box = pygame.Rect((0, 0), (600, 70))
        box.center = (WIDTH // 2, HEIGHT * 0.9)
        mod.screen.draw.filled_rect(box, (255, 255, 0))
        mod.screen.draw.text("press the space bar...", center=(WIDTH // 2, HEIGHT * 0.9), color="blue", fontsize=70,
                             shadow=(1, 1))
        box1 = pygame.Rect((0, 0), (600, 50))
        box1.center = (WIDTH // 2, HEIGHT * 0.98)
        mod.screen.draw.filled_rect(box1, (0, 255, 0))
        mod.screen.draw.text("F : Fullscreen  N: NormalMod  Esc : Exit  R : Restart",
                             center=(WIDTH // 2, HEIGHT * 0.98), color="black", fontsize=33)

    elif status == "play":
        background.draw()
        mario.draw()
        luigi.draw()
        coin.draw()
        enemy.draw()
        mushroom.draw()
        gold.draw()
        mod.screen.draw.text("Luigi Score:  " + str(luigi.score), (10, 10), color="green", fontsize=30)
        mod.screen.draw.text("Mario Score:  " + str(mario.score), (1110, 10), color="red", fontsize=30)
        mod.screen.draw.text("Timer: " + str(round(timer)), (WIDTH // 2 - 100, 10), color="black", fontsize=30)
    elif status == "end":
        mod.screen.blit("end", (0, 0))
    elif status == "luigi_win":
        mod.screen.blit("luigi_win", (0, 0))
    elif status == "mario_win":
        mod.screen.blit("mario_win", (0, 0))
    elif status == "time_over":
        mod.screen.blit((0, 255, 0))
        mod.screen.blit("Time Over!!", center=(WIDTH // 2, HEIGHT // 2), color="black", fontesize=180)


def update():
    global status, timer
    if status == "play":
        timer -= 1 / 60
        # enemy section
        enemy.x += enemy.dx
        enemy.y -= enemy.dy
        actor_location_correct(enemy)
        if enemy.colliderect(luigi):
            actor_random_location(luigi)
            luigi.score = 0
            sounds.lose.play()
        if enemy.colliderect(mario):
            actor_random_location(mario)
            mario.score = 0
            sounds.lose.play()

        if enemy.colliderect(luigi):
            luigi.score = 0
            actor_random_location(luigi)

        # luigi section
        if keyboard.right:
            luigi.x += luigi.speed
            luigi.image = "luigi_right"
        if keyboard.left:
            luigi.x -= luigi.speed
            luigi.image = "luigi_left"
        if keyboard.up:
            luigi.y -= luigi.speed
        if keyboard.down:
            luigi.y += luigi.speed
        if luigi.colliderect(coin):
            actor_random_location(coin)
            sounds.jiring.play()
            luigi.score += coin.point
        if luigi.colliderect(gold):
            actor_random_location(gold)
            sounds.jiring.play()
            luigi.score += gold.point
        if luigi.colliderect(mushroom):
            actor_random_location(mushroom)
            sounds.jiring.play()
            luigi.score += mushroom.score
        if luigi.score >= 100:
            status = "luigi_win"

        actor_location_correct(luigi)

        # mario section
        if keyboard.d:
            mario.x += mario.speed
            mario.image = "mario_right"
        if keyboard.a:
            mario.x -= mario.speed
            mario.image = "mario_left"
        if keyboard.w:
            mario.y -= mario.speed
        if keyboard.s:
            mario.y += mario.speed
        if mario.colliderect(coin):
            actor_random_location(coin)
            sounds.jiring.play()
            mario.score += coin.point
        if mario.colliderect(gold):
            actor_random_location(gold)
            sounds.jiring.play()
            mario.score += gold.point
        if mario.colliderect(mushroom):
            actor_random_location(mushroom)
            sounds.jiring.play()
            mario.score += mushroom.score
        if mario.score >= 100:
            status = "mario_win"

        actor_location_correct(mario)


def actor_random_location(actor_name):
    actor_name.x = random.randint(actor_name.width // 2, WIDTH - actor_name.width // 2)
    actor_name.y = random.randint(actor_name.height // 2, HEIGHT - actor_name.height // 2)


WIDTH = 1280
HEIGHT = 720
status = "home"
timer = 100
hwnd = pygame.display.get_wm_info()['window']
windll.user32.MoveWindow(hwnd, 115, 20, WIDTH, HEIGHT, False)
mod = sys.modules["__main__"]
sounds.supermario.play(-1)
background = Actor("back")
luigi = Actor("luigi_right")
actor_random_location(luigi)
luigi.score = 0
luigi.speed = 5

mario = Actor("mario_right")
actor_random_location(mario)
mario.score = 0
mario.speed = 5

coin = Actor("coin")
actor_random_location(coin)
coin.point = 10

gold = Actor("coin2")
actor_random_location(gold)
gold.point = 20

mushroom = Actor("mushroom")
hide_mushroom()
mushroom.score = 50

enemy = Actor("enemy_right")
enemy.dx = 2
enemy.dy = 2
actor_random_location(enemy)

pgzrun.go()
