import pygame as pg


def load_level(level_file, alien_h, alien_w, n):
    aliens = []
    with open(level_file, 'r') as f:
        y = -alien_h
        for line in f:
            x = (400-(len(line)*(alien_w+10)))/2+28
            for c in line.strip(): # Remove line ending    
                print(len(line))
                

                if c == "A":
                    alien = {'x': x , 'y': y, 'hp': n }
                    aliens.append(alien)
                    x += alien_w+10
                if c == "-":
                    x += alien_w+10
                
                

                
            y -= alien_h+10
    print()
    return aliens

# https://stackoverflow.com/questions/56209634/is-it-possible-to-change-sprite-colours-in-pygame
def change_color(image, color):
    colouredImage = pg.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pg.BLEND_MULT)
    return finalImage