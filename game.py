# Arcade-style space shooter inspired by Galaga and Spacer Invaders.
# Made for the purpose of teaching git version control to beginners.
#Github test
import pygame as pg
from Levels.util import load_level 
from Levels.util import change_color
import sqlite3
import random

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

#Player data
name = ""
health = 1
coins = 0
selectedtext = 1
bulletspeed = 8
bulletdmg = 1
explosivebullets = False
explosionx1 = 5
explosionx2 = 10
explosiony1 = 70
explosiony2 = 90

# Spaceship character
ship_images = []
for i in range(3):
    img = pg.image.load(f"images/ship_{i}.png")
    ship_images.append(img)
    
ship_x = 180 
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
t = "alien"


alien_w = alien_images[0].get_rect().size[0]
alien_h = alien_images[0].get_rect().size[1]
aliens = load_level("Levels/level0.txt", alien_h,alien_w,n,t)
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
                    state = "GAMEMODE"

            screen.fill((0,0,0))

            text = font_title.render(f"Space Shooter", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,100))

            text = font_title.render(f"Press [tab]", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,300))

            text = font_title.render(f"to play!", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,350))
    
    elif state == "GAMEMODE":
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

            # Keypresses
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False
                
                elif event.key == pg.K_1:
                    state = "PLAY"
                    currentgamemode = "SUPER"
                    health = 5
                    

                elif event.key == pg.K_2:
                    state = "PLAY"
                    currentgamemode = "normal"
                    health = 3
                
                elif event.key == pg.K_3:
                    state = "PLAY"
                    currentgamemode = "hard"
                    health = 1
                
                elif event.key == pg.K_4:
                    state = "PLAY"
                    currentgamemode = "nightmare"
                    health = 1
            #drawing
            screen.fill((0,0,0))

            text = font_title.render(f"SELECT THE", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,70))
            
            text = font_title.render(f"GAMEMODE:", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,100))

            text = font_title.render(f"Press 1 for", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,170))
            text = font_title.render(f"SUPER SHOOTER", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,200))


            text = font_title.render(f"Press 2 for", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,250))

            text = font_title.render(f"normal", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,280))


            text = font_title.render(f"Press 3 for", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,340))

            text = font_title.render(f"hard", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,370))


            text = font_title.render(f"Press 4 for", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,430))

            text = font_title.render(f"NIGHTMARE", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,460))




    elif state == "RESTART":
        events = pg.event.get()
        aliens.clear()
        alien.clear()
        projectiles.clear()
        score = 0
        n = 1
        left_pressed = False
        right_pressed = False
        ship_x = 180 
        lvln = 0
        aliens = load_level(f"Levels/level{lvln}.txt",alien_h,alien_w,n,t)
        if name == "":  
            name = random.choice(["John Doe", "Jane Doe"])
        else:
            name = name
        if currentgamemode == "hard":
            connection.execute(f"insert into whoknowswhat values ('{name}' , '{strscore}'); ")
            connection.commit()
        state = "GAMEMODE"



    elif state == "NEXTLEVEL":
        events = pg.event.get()
        aliens.clear()
        alien.clear()
        projectiles.clear()
        
        n += 1
        left_pressed = False
        right_pressed = False
        ship_x = 180 
        if lvln == 7:
            n = 1
            aliens = load_level(f"Levels/level{lvln}.txt", alien_h,alien_w,n, t)
        aliens = load_level(f"Levels/level{lvln}.txt", alien_h,alien_w,n, t)

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
                elif event.key == pg.K_p:
                    state = "LEVELWIN"

            # Keyreleases
            elif event.type == pg.KEYUP:

                if event.key == pg.K_a:
                    left_pressed = False 

                if event.key == pg.K_d:
                    right_pressed = False 


        ## Updating (movement, collisions, etc.) ##

        # Spaceship
        if left_pressed:
            if ship_x > 0:
                ship_x -= 8

        if right_pressed:
            if ship_x < width-ship_w:
                ship_x += 8
        
        #Alien movement
        if currentgamemode == "normal" or "SUPER":
            alienspeed = 0.8
        if currentgamemode == "hard":
            alienspeed = 1
        if currentgamemode == "nightmare":
            alienspeed = 1.2

        for a in aliens:
            a['y'] += alienspeed
        
       

    
        # Projectile movement
        # Reverse iteration needed to handle each projectile correctly
        # in cases where a projectile is removed.
        for projectile in reversed(projectiles):
            projectile['y'] -= bulletspeed

            # Remove projectiles leaving the top of the screen
            if projectile['y'] < 0:
                projectiles.remove(projectile)

        # Alien / projectile collision 
        # Test each projectile against each alien
        for projectile in reversed(projectiles):
            for alien in aliens:

                if alien['hp'] < 0 or alien['hp'] == 0:
                    # Alien is hit dead
                    aliens.remove(alien)
                    sound_alienKill.play()
                    score += 10
                    if currentgamemode == "SUPER":
                        if alien['type'] == "coin":
                            coins += 1
                
                # Horizontal (x) overlap
                if (alien['x'] < projectile['x'] + projectile_w and 
                    projectile['x'] < alien['x']+alien_w):
                    
                    # Vertical (y) overlap 
                    if (projectile['y'] < alien['y'] + alien_h and 
                        alien['y'] < projectile['y'] + projectile_h):
                        

                        # Alien is hit
                        if alien['type'] == "alien":
                            alien['hp'] -= bulletdmg
                        if currentgamemode == "SUPER":
                            if alien['type'] == "coin":
                                alien['hp'] -= 0.5*bulletdmg
                        
                        explosionx1 = projectile['x'] - 100
                        explosionx2 = projectile['x'] + 50
                        explosiony1 = projectile['y'] - 100
                        explosiony2 = projectile['y'] + 50
                        projectiles.remove(projectile)
                        
                        if alien['hp'] < 0 or alien['hp'] == 0:
                            # Alien is hit dead
                            aliens.remove(alien)
                            sound_alienKill.play()
                            score += 10
                            if currentgamemode == "SUPER":
                                if alien['type'] == "coin":
                                    coins += 1
                        else:
                            sound_alienHit.play()
                
                        
                        # No further aliens can be hit by this projectile 
                        # so skip to the next projectile 
                        break
        
        for alien in aliens:
            if explosivebullets == True:
                if alien['x'] > explosionx1 and alien['x'] < explosionx2:
                    if alien['y'] > explosiony1 and alien['y'] < explosiony2:
                        alien['hp'] -= 1
        
        # Firing (spawning new projectiles)
        if projectile_fired:
            sound_laser.play()

            projectile = {'x': ship_x + ship_w/2 - projectile_w/2, 'y': ship_y}
            projectiles.append(projectile)
            projectile_fired = False


        ## Drawing ##
        screen.fill((0,0,0)) 
        #explosion
        pg.draw.rect(screen, [225, 20, 0, 100], [explosionx1,explosiony1,explosionx2-explosionx1,explosiony2-explosiony1], 2)
        pg.draw.rect(screen, [225, 20, 255, 200], [explosionx1+50,explosiony1+50,explosionx2-explosionx1-50,explosiony2-explosiony1-50])

        # 3 images --> tick % 3
        # 100% animation speed: tick % 3
        # 25% animation speed: int(tick/4) % 3
        r = int(tick/4) % 3 
        screen.blit(ship_images[r], (ship_x, ship_y))
        
        # Alien
        
        r = int(tick/8) % 2
        
        
        
        for alien in aliens:
            if alien['hp'] > 0:
                ratiomaxhealth = alien['hp']/n
            changegreen = 255*ratiomaxhealth
            changered = 255-255*ratiomaxhealth
            changeyellow = -200*ratiomaxhealth+200

            img= change_color(alien_images[r], (changered,changegreen,0))
            if currentgamemode == "SUPER":
                if alien['type'] == "coin":
                    img= change_color(alien_images[r], (255,255,changeyellow))
            screen.blit(img, (alien['x'], alien['y']))
           


            #Alien killing you logic
            if alien['type'] != "coin":
                if alien['y'] > height-40:
                    health -= 1
                    aliens.remove(alien)
                    if health == 0:
                        state = "GAME OVER"
            if alien['y'] > height:
                aliens.remove(alien)
        
        
                    
            
        
        
        

        # Projectiles
        for projectile in projectiles:
            rect = (projectile['x'], projectile['y'], projectile_w, projectile_h)
            pg.draw.rect(screen, (255, 0, 0), rect) 

        # Scoreboard
        text = font_scoreboard.render(f"{score:04d}", True, (255,255,255))
        screen.blit(text, (10,560))

        #Player Health
        
        text = font_scoreboard.render(f"HEALTH: {health}", True, (255,100,100))
        screen.blit(text, (200,560))
        #player coin amount
        if currentgamemode == "SUPER":
            text = font_scoreboard.render(f"{coins}", True, (250,250,50))
            screen.blit(text, (10,530))

    elif state == "GAME OVER":
        scores.append(score)
        highscore = max(scores)
        strscore = str(score)

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

                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if not event.key == pg.K_TAB:
                        name += event.unicode  

        

        #Drawing
        screen.fill((0,0,0)) 
        text = font_scoreboard.render("Lost in Level: "f"{lvln+1}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,50))

        
        text = font_scoreboard.render("Score: " f"{score:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/3))

        text = font_scoreboard.render("Highscore: " f"{highscore:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/3+40))

        text = font_scoreboard.render("WRITE YOUR NAME:", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height/2))

        
        text = font_scoreboard.render(f"{name}", True, (255,255,255))
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
    
    
    elif state == "POWERUP":
        
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    state = "NEXTLEVEL"
                #debug
                if event.key == pg.K_c:
                    coins += 1
                if event.key == pg.K_s:
                    if selectedtext < 5:
                        selectedtext +=1
                if event.key == pg.K_w:
                    if selectedtext > 1:
                        selectedtext -=1
                if event.key == pg.K_SPACE:
                    if selectedtext == 1:
                        health += 1
                        coins -= 5
                    if selectedtext == 2:
                        bulletspeed += 2
                        coins -= 3
                    if selectedtext == 3:
                        bulletdmg += 1
                        coins -= 3
                    if selectedtext == 4:
                        explosivebullets = True
                        coins -= 20
                    

        

        screen.fill((0,0,0)) 
        text = font_scoreboard.render("POWERUP SHOP", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,10))
        
        text = font_scoreboard.render(f"COINS: {coins}", True, (235,235,50))
        text_width = text.get_rect().width 
        screen.blit(text, ((10)/2,height-20))
        
        text = font_scoreboard.render(f"Tab = continue", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height-70))

        text = font_scoreboard.render(f"Spacebar = buy", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,height-100))

        if selectedtext == 1:
            bluetext = 100
        else:
            bluetext = 255
        text = font_scoreboard.render("+1 Health [5]", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,100))

        if selectedtext == 2:
            bluetext = 100
        else:
            bluetext = 255
        text = font_scoreboard.render("Bullet speed [3]", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,150))

        if selectedtext == 3:
            bluetext = 100
        else:
            bluetext = 255
        text = font_scoreboard.render("Bullet damage [3]", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,200))

        if selectedtext == 4:
            bluetext = 100
        else:
            bluetext = 255
        
        text = font_scoreboard.render("Explosive", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,250))
        text = font_scoreboard.render("bullets  [20]", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,280))


        


    
    
    elif state == "LEVELWIN1":
        #event logic
        events = pg.event.get()
        
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    if currentgamemode == "SUPER":
                        state = "POWERUP"
                    else:
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
        
        if currentgamemode == "SUPER":
            text = font_scoreboard.render("go to the SHOP", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,height/2+190))    
        else:
            text = font_scoreboard.render("continue", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,height/2+190))


        if lvln == 7:
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