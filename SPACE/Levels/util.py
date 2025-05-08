import pygame as pg
import random
aliens = []

def load_level(level_file, alien_h, alien_w, n, t, hit):
    #last level attempt = 9A
    if level_file == "Space-Shooter/Levels/level7.txt":        
        y = -alien_h
        x = (400-(10*(alien_w)))/2-13
        for c in range(10):
            alien = {'x': x , 'y': y, 'hp': n, 'type': t, 'hit': hit}
            rando = random.randint(1,100)
            if rando > 90:
                t = "coin"
            if rando < 90:
                t = "alien"
                aliens.append(alien)
            x += alien_w+3
        y -= alien_h+10
        
    
    #all other levels
    else:
        with open(level_file, 'r') as f:
            y = -alien_h
            for line in f:
                    
                    x = (400-(len(line)*(alien_w+10)))/2+28
                    for c in line.strip(): # Remove line ending    

                        if c == "A":
                            alien = {'x': x , 'y': y, 'hp': n, 'type': t}
                            rando = random.randint(1,100)
                            if rando > 90:
                                t = "coin"
                            if rando < 90:
                                t = "alien"
                            aliens.append(alien)
                            x += alien_w+10
                        if c == "-":
                            x += alien_w+10
                    y -= alien_h+10
    
    return aliens

# https://stackoverflow.com/questions/56209634/is-it-possible-to-change-sprite-colours-in-pygame
def change_color(image, color):
    colouredImage = pg.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pg.BLEND_MULT)
    return finalImage