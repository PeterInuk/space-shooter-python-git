# Arcade-style space shooter inspired by Galaga and Spacer Invaders.
# Made for the purpose of teaching git version control to beginners.

import pygame as pg
from util import *
import sqlite3
connection = sqlite3.connect("dataTest.db")
cursor = connection.cursor()


### Setup ###
pg.init()
clock = pg.time.Clock()
width = 400
height = 600
screen = pg.display.set_mode((width,height))
pg.display.set_caption("Space Shooter")
scores = []
lvln = 0
name = ""
# Spaceship character
ship_images = []
for i in range(3):
    img = pg.image.load(f"images/ship_{i}.png")
    ship_images.append(img)
    
ship_x = 200 
ship_y = 500
ship_w = ship_images[0].get_rect().size[0]
ship_h = ship_images[0].get_rect().size[1]

# Alien character
red_color = (255,0,0)
green_color = (10,200,10)
alien_images = []
red_alien_images = []
for i in range(2):
    img = pg.image.load(f"images/alien_{i}.png")
    alien_images.append(img)



aliens = []
alienspeed = 1
n = 1
# for i in range(6):
#     alien1 = {'x': 50*i + 50 , 'y': 0 , 'hp': n, 'hit': False}
#     alien2 = {'x': 50*i + 50, 'y': 50, 'hp': n, 'hit': False}
#     aliens.append(alien1)
#     aliens.append(alien2)


alien_w = alien_images[0].get_rect().size[0]
alien_h = alien_images[0].get_rect().size[1]
aliens = load_level("level0.txt", alien_h,alien_w,n)
# Projectiles 
projectile_fired = False
projectiles = []
projectile_w = 4 
projectile_h = 8

# Keypress status
left_pressed = False
right_pressed = False

# Sound: weapon / laser 
sound_laser = pg.mixer.Sound("sounds/laser.wav")

# Sound: Ship truster
sound_thruster1 = pg.mixer.Sound("sounds/thruster1.wav")
sound_thruster2 = pg.mixer.Sound("sounds/thruster2.wav")

# Sound: Alien death sound
sound_alienKill = pg.mixer.Sound("sounds/AlienKill.wav")

# Sound: Alien hit sound
sound_alienHit = pg.mixer.Sound("sounds/AlienHit.wav")




# Fonts
# https://fonts.google.com/specimen/Press+Start+2P/about
font_scoreboard = pg.font.Font("fonts/PressStart2P-Regular.ttf", 20)

font_start = pg.font.Font("fonts/PressStart2P-Regular.ttf", 20)

font_title = pg.font.Font("fonts/PressStart2P-Regular.ttf", 25)


### Game loop ###
running = True
tick = 0
score = 0
state = "START"
while running:
    #score
    
            
    if state == "START":
        events = pg.event.get()
        for event in events:

            # Close window (pressing [x], Alt+F4 etc.)
            if event.type == pg.QUIT:
                running = False

            # Keypresses
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False
                
                elif event.key == pg.K_TAB:
                    state = "PLAY"

            screen.fill((0,0,0))

            text = font_title.render(f"Space Shooter", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,100))

            text = font_title.render(f"Write your name:", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,300))

            text = font_title.render(f"Press [tab]", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,300))

            text = font_title.render(f"to play!", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,350))
    


    elif state == "RESTART":
        events = pg.event.get()
        aliens.clear()
        alien.clear()
        projectiles.clear()
        score = 0
        n = 1
        left_pressed = False
        right_pressed = False
        ship_x = 200 
        lvln = 0
        aliens = load_level(f"level{lvln}.txt",alien_h,alien_w,n)

        state = "PLAY"



    elif state == "NEXTLEVEL":
        events = pg.event.get()
        aliens.clear()
        alien.clear()
        projectiles.clear()
        
        n += 1
        left_pressed = False
        right_pressed = False
        ship_x = 200 
        if lvln == 6:
            n = 1
            state = "PLAY"
            aliens = load_level(f"level{lvln}.txt", alien_h,alien_w,n)
        aliens = load_level(f"level{lvln}.txt", alien_h,alien_w,n)

        state = "PLAY"
        
        
      
        
       
        
            
        

    elif state == "PLAY":
        
        #level clear check
        if len(aliens) == 0:
            state = "LEVELWIN"

        ## Event loop  (handle keypresses etc.) ##
        events = pg.event.get()
        for event in events:

            # Close window (pressing [x], Alt+F4 etc.)
            if event.type == pg.QUIT:
                running = False

            # Keypresses
            elif event.type == pg.KEYDOWN:
                if event.type == pg.QUIT:
                    running = False
                if event.key == pg.K_ESCAPE:
                    running = False

                elif event.key == pg.K_a:
                    left_pressed = True
                
                elif event.key == pg.K_d:
                    right_pressed = True

                elif event.key == pg.K_SPACE:
                    projectile_fired = True

            # Keyreleases
            elif event.type == pg.KEYUP:

                if event.key == pg.K_a:
                    left_pressed = False 

                if event.key == pg.K_d:
                    right_pressed = False 


        ## Updating (movement, collisions, etc.) ##

        # Spaceship
        if left_pressed:
            ship_x -= 8

        if right_pressed:
            ship_x += 8

        #Alien movement
        for a in aliens:
            a['y'] += alienspeed
        
       

    
        # Projectile movement
        # Reverse iteration needed to handle each projectile correctly
        # in cases where a projectile is removed.
        for projectile in reversed(projectiles):
            projectile['y'] -= 8 

            # Remove projectiles leaving the top of the screen
            if projectile['y'] < 0:
                projectiles.remove(projectile)

        # Alien / projectile collision 
        # Test each projectile against each alien
        for projectile in reversed(projectiles):
            for alien in aliens:

                # Horizontal (x) overlap
                if (alien['x'] < projectile['x'] + projectile_w and 
                    projectile['x'] < alien['x']+alien_w):

                    # Vertical (y) overlap 
                    if (projectile['y'] < alien['y'] + alien_h and 
                        alien['y'] < projectile['y'] + projectile_h):
                        alien['hit'] = True
                        # Alien is hit
                        alien['hp'] -= 1
                        projectiles.remove(projectile)
                        
                        if alien['hp'] < 0 or alien['hp'] == 0:
                            # Alien is hit dead
                            aliens.remove(alien)
                            sound_alienKill.play()
                            score += 10
                        else:
                            sound_alienHit.play()
                        
                        
                        # No further aliens can be hit by this projectile 
                        # so skip to the next projectile 
                        break

        # Firing (spawning new projectiles)
        if projectile_fired:
            sound_laser.play()

            projectile = {'x': ship_x + ship_w/2 - projectile_w/2, 'y': ship_y}
            projectiles.append(projectile)
            projectile_fired = False


        ## Drawing ##
        screen.fill((0,0,0)) 

        # 3 images --> tick % 3
        # 100% animation speed: tick % 3
        # 25% animation speed: int(tick/4) % 3
        r = int(tick/4) % 3 
        screen.blit(ship_images[r], (ship_x, ship_y))

        # Alien
        
        r = int(tick/8) % 2
        
        
        
        for alien in aliens:
            ratiomaxhealth = alien['hp']/n
            changegreen = 255*ratiomaxhealth
            changered = 255-255*ratiomaxhealth
            img= change_color(alien_images[r], (changered,changegreen,0))
            screen.blit(img, (alien['x'], alien['y']))
           
            #for i in range(2):
                #img = pg.image.load(f"images/alien_{i}.png")
                #for k in red_color:
                    #newred = k/alien['hp']     THIS DOESNT WORK
                #img = change_color(img, newred)
                #red_alien_images.append(img)
            
            #screen.blit(red_alien_images[r], (alien['x'], alien['y']))


            #Alien killing you logic
            if alien['y'] == height-40:
             state = "GAME OVER"
            
        
        
        

        # Projectiles
        for projectile in projectiles:
            rect = (projectile['x'], projectile['y'], projectile_w, projectile_h)
            pg.draw.rect(screen, (255, 0, 0), rect) 

        # Scoreboard
        text = font_scoreboard.render(f"{score:04d}", True, (255,255,255))
        screen.blit(text, (10,560))

    elif state == "GAME OVER":
        scores.append(score)
        highscore = max(scores)
        strscore = str(score)
        connection.execute(f"insert into whoknowswhat values ({name}, {strscore}); ")
        connection.commit()
        state = "GAME OVER1"

    elif state == "GAME OVER1":
        #event logic
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    state = "RESTART"
                if event.type == pg.QUIT:
                    running = False

        #Drawing
        screen.fill((0,0,0)) 
        text = font_scoreboard.render("Lost in Level: "f"{lvln+1}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2-130))

        text = font_scoreboard.render("GAME OVER", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2-50))
        
        text = font_scoreboard.render("Score: " f"{score:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2))

        text = font_scoreboard.render("Highscore: " f"{highscore:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2+40))

        text = font_scoreboard.render("Press [tab] to", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2+130))
        
        text = font_scoreboard.render("play again", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2+170))
       
    
    elif state == "LEVELWIN":
        score += 100
        scores.append(score)
        highscore = max(scores)
        lvln += 1
        state = "LEVELWIN1"

    elif state == "LEVELWIN1":
        #event logic
        events = pg.event.get()
        
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    state = "NEXTLEVEL"
               
        #Drawing
        screen.fill((0,0,0)) 
        text = font_scoreboard.render("Level "f"{lvln}"" complete!", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2-120))

        text = font_scoreboard.render("You have been ", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2-50))

        text = font_scoreboard.render("awarded 100 points!", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2-20))

        
        text = font_scoreboard.render("Score: " f"{score:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2+50))
        text = font_scoreboard.render("Highscore: " f"{highscore:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2+80))

        text = font_scoreboard.render("Press [tab] to", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2+160))
        
        text = font_scoreboard.render("play again", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2+190))


        if lvln == 6:
            screen.fill((0,0,0)) 
            text = font_scoreboard.render("Level "f"{lvln}"" complete!", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,height/2-120))
            
            text = font_scoreboard.render("Next level is the", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,height/2-50))
            
            text = font_scoreboard.render("LAST LEVEL", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,height/2-20))
            
            text = font_scoreboard.render("Score: " f"{score:04d}", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,height/2+50))

            text = font_scoreboard.render("Highscore: " f"{highscore:04d}", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,height/2+80))


    


  


    
    # Update window with newly drawn pixels
    pg.display.flip()
    
    # Limit/fix frame rate (fps)
    clock.tick(50)
    tick += 1