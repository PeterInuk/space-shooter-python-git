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
bulletdmg = 0

spacehold = 0
spaceholding = False

# Spaceship character
ship_images = []
for i in range(3):
    img = pg.image.load(f"Space-Shooter/images/ship_{i}.png")
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
    img = pg.image.load(f"Space-Shooter/images/alien_{i}.png")
    alien_images.append(img)

aliens = []
alienspeed = 1
bottomalien = 0
n = 1
t = "alien"


alien_w = alien_images[0].get_rect().size[0]
alien_h = alien_images[0].get_rect().size[1]
hit = False
aliens = load_level(f"Space-Shooter/Levels/level{lvln}.txt", alien_h,alien_w,n,t, hit)
# Projectiles 
projectile_fired = False
projectiles = []
projectile_w = 4 
projectile_h = 8

# Explosive bullets
explosivebullets = []
explosivebulletsmode = False
explosivebullet_fired = False
penbullets = False
bullethits = 0
penbulletupgradelvl = 2
explosionx1 = 0
explosionx2 = 0
explosiony1 = 0
explosiony2 = 0
explosionsize = 100
explosivebullet_w = 15
explosivebullet_h = 15
explosivecount = 2

# Keypress status
left_pressed = False
right_pressed = False
shift_pressed = False

# Sound: weapon / laser 
sound_laser = pg.mixer.Sound("Space-Shooter/sounds/laser.wav")

# Sound: weapon / explosion
sound_explosivebullet = pg.mixer.Sound("Space-Shooter/sounds/ExplosiveBullet.wav")
sound_explosion = pg.mixer.Sound("Space-Shooter/sounds/explosion.wav")

# Sound: Buying sound
sound_buying = pg.mixer.Sound("Space-Shooter/sounds/buying.wav")

# Sound: Invalid input sound
sound_invalid = pg.mixer.Sound("Space-Shooter/sounds/invalid.wav")

# Sound: Select sound
sound_select = pg.mixer.Sound("Space-Shooter/sounds/select.wav")

# Sound: Change text sound and alternate select
sound_select2 = pg.mixer.Sound("Space-Shooter/sounds/selectText.wav")

# Sound: Alien death sound
sound_alienKill = pg.mixer.Sound("Space-Shooter/sounds/AlienKill.wav")

# Sound: Alien hit sound
sound_alienHit = pg.mixer.Sound("Space-Shooter/sounds/AlienHit.wav")

# Music
# Music: fightmusic
pg.mixer.init()
music = pg.mixer.music
load_music_intro = music.load("Space-Shooter/sounds/intromusic.wav")
load_music_fight = music.load("Space-Shooter/sounds/fightmusic.wav")
play_music = music.play(loops=-1)

music.load("Space-Shooter/sounds/intromusic.wav")
music.play(loops=-1)
music.set_volume(0.3)


# Fonts
# https://fonts.google.com/specimen/Press+Start+2P/about
font_scoreboard = pg.font.Font("Space-Shooter/fonts/PressStart2P-Regular.ttf", 20)

font_start = pg.font.Font("Space-Shooter/fonts/PressStart2P-Regular.ttf", 20)

font_title = pg.font.Font("Space-Shooter/fonts/PressStart2P-Regular.ttf", 25)


### Game loop ###
running = True
tick = 0
score = 0
state = "START"

while running:
    if state == "START":
        
        #pg.mixer.music.play(loops=-1)
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
            #Screen reset
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
                    currentgamemode = "SUPER"
                    state = "SELECTEDGAMEMODE"

                    
                    

                elif event.key == pg.K_2:
                    currentgamemode = "space shooter"
                    state = "SELECTEDGAMEMODE"
                
                
            #drawing
            screen.fill((0,0,0))

            text = font_title.render(f"SELECT THE", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,70))
            
            text = font_title.render(f"GAMEMODE:", True, (150,150,255))
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
            screen.blit(text, ((width-text_width)/2,300))

            text = font_title.render(f"Space Shooter", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,330))


           


    elif state == "SELECTEDGAMEMODE":
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                    running = False
            
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False
                
                elif event.key == pg.K_1:
                    state = "PLAY"
                    difficulty = "easy"
                    health = 5
                    alienspeed = 0.75
                    pg.mixer.music.load("Space-Shooter/sounds/fightmusic.wav")
                    pg.mixer.music.play(loops=-1)
                    sound_select.play()
                
                elif event.key == pg.K_2:
                    state = "PLAY"
                    difficulty = "normal"
                    health = 3
                    alienspeed = 0.8
                    pg.mixer.music.load("Space-Shooter/sounds/fightmusic.wav")
                    pg.mixer.music.play(loops=-1)
                    sound_select.play()
                
                elif event.key == pg.K_3:
                    state = "PLAY"
                    difficulty = "hard"
                    health = 1
                    alienspeed = 1
                    pg.mixer.music.load("Space-Shooter/sounds/fightmusic.wav")
                    pg.mixer.music.play(loops=-1)
                    sound_select.play()
                
                elif event.key == pg.K_4:
                    state = "PLAY"
                    difficulty = "NIGHTMARE"
                    health = 1
                    alienspeed = 1.2
                    pg.mixer.music.load("Space-Shooter/sounds/fightmusic.wav")
                    pg.mixer.music.play(loops=-1)
                    sound_select.play()
                elif event.key == pg.K_5:
                    state = "GAMEMODE"
            #Reset screen
            screen.fill((0,0,0))

            text = font_title.render(f"SELECT THE", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,70))
            
            text = font_title.render(f"DIFFICULTY:", True, (255,150,150))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,100))

            #difficulty text
            text = font_title.render(f"Press 1 for", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,170))

            text = font_title.render(f"Easy", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,200))


            text = font_title.render(f"Press 2 for", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,250))

            text = font_title.render(f"Normal", True, (255,255,255))
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

            text = font_title.render(f"5 to go back", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,535))

            


    elif state == "RESTART":
        events = pg.event.get()
        aliens.clear()
        alien.clear()
        projectiles.clear()
        explosivebullets.clear()
        score = 0
        n = 1
        coins = 0
        left_pressed = False
        right_pressed = False
        ship_x = 180 
        lvln = 0
        bulletspeed = 8
        bulletdmg = 0
        explosivebullets = []
        explosivebulletsmode = False
        explosivebullet_fired = False
        penbullets = False
        penbulletupgradelvl = 2
        bullethits = 0
        explosionx1 = 0
        explosionx2 = 0
        explosiony1 = 0
        explosiony2 = 0
        explosivecount = 2

        aliens = load_level(f"Space-Shooter/Levels/level{lvln}.txt",alien_h,alien_w,n,t, hit)
        if name == "":  
            name = random.choice(["John Doe", "Jane Doe"])
        else:
            name = name
        if currentgamemode == "SUPER":
            connection.execute(f"insert into SUPERscore values ('{name}' , '{strscore}'); ")
            connection.commit() 

        if currentgamemode == "normal":
            connection.execute(f"insert into normalscore values ('{name}' , '{strscore}'); ")
            connection.commit()

        if currentgamemode == "hard":
            connection.execute(f"insert into hardscore values ('{name}' , '{strscore}'); ")
            connection.commit()

        if currentgamemode == "nightmare":
            connection.execute(f"insert into nightmarescore values ('{name}' , '{strscore}'); ")
            connection.commit()
        
        music.load("Space-Shooter/sounds/intromusic.wav")
        music.play(loops=-1)
        music.set_volume(0.3)
        play_music
        state = "GAMEMODE"



    elif state == "NEXTLEVEL":
        events = pg.event.get()
        aliens.clear()
        alien.clear()
        projectiles.clear()
        explosivebullets.clear()
        
        n += 1
        left_pressed = False
        right_pressed = False
        ship_x = 180 
        explosivecount =2
        if lvln == 7:
            n = 1
            aliens = load_level(f"Space-Shooter/Levels/level{lvln}.txt", alien_h,alien_w,n, t, hit)
        aliens = load_level(f"Space-Shooter/Levels/level{lvln}.txt", alien_h,alien_w,n, t, hit)

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
                if event.key == pg.K_ESCAPE:
                    running = False

                elif event.key == pg.K_d:
                    right_pressed = True
                elif event.key == pg.K_RIGHT:
                    right_pressed = True

                elif event.key == pg.K_a:
                    left_pressed = True
                elif event.key == pg.K_LEFT:
                    left_pressed = True
                
                elif event.key == pg.K_w:
                    if explosivecount > 0:
                        explosivebullet_fired = True
                        explosivecount -= 1
                elif event.key == pg.K_UP:
                    if explosivecount > 0:
                        explosivebullet_fired = True
                        explosivecount -= 1

                elif event.key == pg.K_SPACE:
                    projectile_fired = True
                    
                #debug
                elif event.key == pg.K_p:
                   state = "LEVELWIN"
                elif event.key == pg.K_LSHIFT:
                    shift_pressed = True
            
                

            
            # Keyrelease
            elif event.type == pg.KEYUP:                
                if event.key == pg.K_a:
                    left_pressed = False 
                elif event.key == pg.K_LEFT:
                    left_pressed = False 
                
                if event.key == pg.K_d:
                    right_pressed = False 
                elif event.key == pg.K_RIGHT:
                    right_pressed = False 
                elif event.key == pg.K_LSHIFT:
                    shift_pressed = False
        

        ## Updating (movement, collisions, etc.) ##

        # Spaceship
        if left_pressed:
            if ship_x > 0:
                if shift_pressed == True:
                    ship_x -= 4
                else:
                    ship_x -= 8

        if right_pressed:
            if ship_x < width-ship_w:
                if shift_pressed == True:
                    ship_x += 4
                else:
                    ship_x += 8
        
        
        #Alien movement
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
        #explosive bullet movement
        for explosivebullet in reversed(explosivebullets):
            explosivebullet['y'] -= bulletspeed

            # Remove projectiles leaving the top of the screen
            if explosivebullet['y'] < 0:
                explosivebullets.remove(explosivebullet)
        # Alien / projectile collision 
        # Test each projectile against each alien
        for projectile in reversed(projectiles):
            if penbullets == True:
                    if penbulletupgradelvl - projectile['alienshit'] == 0:
                        projectile['x'] = 420
                        projectile['y'] = 620
                        projectiles.remove(projectile)
            for alien in aliens:
                # Check if bullet is within alien hitbox
                # Horizontal (x) overlap
                if (alien['x'] < projectile['x'] + projectile_w and 
                    projectile['x'] < alien['x']+alien_w):
                    
                    # Vertical (y) overlap 
                    if (projectile['y'] < alien['y'] + alien_h and 
                        alien['y'] < projectile['y'] + projectile_h):
                        
                        # Alien is hit
                        

                        
                        if projectile['hitting'] == False:
                            if currentgamemode == "SUPER":
                                if alien['type'] == "coin":
                                    alien['hp'] -= 0.5+bulletdmg
                                else:
                                    alien['hp'] -= 1+bulletdmg
                                    
                            else:
                                alien['hp'] -= 1
                                
                        
                        if penbullets == True:
                            if projectile['hitting'] == False:
                                projectile['alienshit'] += 1
                            projectile['hitting'] = True  
                        else: 
                            projectiles.remove(projectile)
                        
                        
                        
                        if alien['hp'] < 0 or alien['hp'] == 0:
                            # Alien is hit dead
                            sound_alienKill.play()
                            score += 10
                           
                        else:
                            sound_alienHit.play()


                        
                        break
                    else:
                        projectile['hitting'] = False

                
                

        #explosive bullet collision check
        for explosivebullet in reversed(explosivebullets):
            for alien in aliens:

                # Horizontal (x) overlap
                if (alien['x'] < explosivebullet['x'] + explosivebullet_w and 
                    explosivebullet['x'] < alien['x']+alien_w):
                    
                    # Vertical (y) overlap 
                    if (explosivebullet['y'] < alien['y'] + alien_h and 
                        alien['y'] < explosivebullet['y'] + explosivebullet_h):
                        
                        # Alien is hit
                        
                        explosionx1 = explosivebullet['x'] - explosionsize
                        explosionx2 = explosivebullet['x'] + explosionsize
                        explosiony1 = explosivebullet['y'] - explosionsize
                        explosiony2 = explosivebullet['y'] + explosionsize
                        for alien in aliens:
                            if alien['x'] > explosionx1 and alien['x'] < explosionx2:
                                if alien['y'] > explosiony1 and alien['y'] < explosiony2:
                                    if alien['hp'] > 0:
                                        alien['hp'] -= 4

                        explosivebullets.remove(explosivebullet)
                    
                        
                        if alien['hp'] < 0 or alien['hp'] == 0:
                            # Alien is hit dead
                            sound_alienKill.play()
                            score += 10
                            
                        else:
                            sound_alienHit.play()
                        sound_explosion.play()
                        
                        # No further aliens can be hit by this projectile 
                        # so skip to the next projectile 
                        break

        #alien explosion hit detection
        for alien in aliens:
            if explosivebulletsmode == True:
                if alien['x'] > explosionx1 and alien['x'] < explosionx2:
                    if alien['y'] > explosiony1 and alien['y'] < explosiony2:
                        alien['hp'] -= 1
            
        # Firing (spawning new projectiles)
        if projectile_fired:
            sound_laser.play()

            projectile = {'x': ship_x + ship_w/2, 'y': ship_y, 'hitting': False, 'alienshit': 0}
            projectiles.append(projectile)
            projectile_fired = False

        # Firing new explosive bullets
        if explosivebulletsmode == True:
            if explosivebullet_fired:
                sound_explosivebullet.play()
                explosivebullet = {'x': ship_x + explosivebullet_w/2, 'y': ship_y}
                explosivebullets.append(explosivebullet)
                explosivebullet_fired = False
        
        
        if lvln == 7:
            bottomalien += alienspeed
            if bottomalien > 36:
                aliens = load_level(f"Space-Shooter/Levels/level{lvln}.txt",alien_h,alien_w,n,t, hit)     
                bottomalien = 0
                       

        ## Drawing ##
        screen.fill((0,0,0)) 
        #explosion
        pg.draw.rect(screen, [235, 100, 10, 200], [explosionx1+50,explosiony1+50,explosionx2-explosionx1-50,explosiony2-explosiony1-50])

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
            if alien ['y'] > height:
                aliens.remove(alien)
        
        
                    
            
        
        
        

        # Projectiles
        for projectile in projectiles:
            projectilerect = (projectile['x'], projectile['y'], projectile_w, projectile_h)
            if penbullets:
                pg.draw.rect(screen, (15, 15, 255), projectilerect) 
            else:
                pg.draw.rect(screen, (255, 0, 0), projectilerect) 


        # Explosive bullet
        for explosivebullet in explosivebullets:
            exrect = (explosivebullet['x'], explosivebullet['y'], explosivebullet_w, explosivebullet_h)
            pg.draw.rect(screen, (200, 100, 0), exrect) 
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
            explosionx1 = 0
            explosionx2 = 0
            explosiony1 = 0
            explosiony2 = 0
        if explosivebulletsmode == True:
            text = font_scoreboard.render(f"EB: {explosivecount}", True, (250,100,0))
            screen.blit(text, (280,530))

        #final alien death check
        for alien in aliens:
            if alien['hp'] == 0:
                if currentgamemode == "SUPER":
                    if alien['type'] == "coin":
                        coins += 1
                aliens.remove(alien)
            if alien['hp'] < 0:
                if currentgamemode == "SUPER":
                    if alien['type'] == "coin":
                        coins += 1
                aliens.remove(alien)

    elif state == "GAME OVER":
        scores.append(score)
        highscore = max(scores)
        strscore = str(score)

        state = "GAME OVER1"

    elif state == "GAME OVER1":
        #event logic
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                
                if event.key == pg.K_TAB:
                    state = "RESTART"
                    sound_select.play()
                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]
                    sound_select2.play()
                else:
                    if not event.key == pg.K_TAB:
                        name += event.unicode  
                        sound_select2.play()

        

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
        if currentgamemode == "SUPER":
            coins += 2
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
                if event.key == pg.K_ESCAPE:
                    running = False
                #debug
                if event.key == pg.K_c:
                    coins += 1
                if event.key == pg.K_s:
                    if selectedtext < 6:
                        selectedtext +=1
                        sound_select2.play()
                    else:
                        sound_invalid.play()
                if event.key == pg.K_w:
                    if selectedtext > 1:
                        selectedtext -=1
                        sound_select2.play()
                    else:
                        sound_invalid.play()
                if event.key == pg.K_TAB:
                    if selectedtext == 1:
                        if coins > 4:
                            sound_buying.play()
                            health += 1
                            coins -= 5
                    if selectedtext == 2:
                        if coins > 2:
                            sound_buying.play()
                            bulletspeed += 2
                            coins -= 3
                    if selectedtext == 3:
                        if coins > 9:
                            sound_buying.play()
                            bulletdmg += 0.5
                            coins -= 5
                    if selectedtext == 4:
                        if coins > 19:
                            sound_buying.play()
                            if explosivebulletsmode == True:
                                explosionsize += 30
                            explosivebulletsmode = True
                            coins -= 20
                            
                    if selectedtext == 5:
                        if penbullets == True:
                            penbulletupgradelvl += 1
                            coins -= 20
                        if coins > 29:
                            sound_buying.play()
                            penbullets = True
                            coins -= 30
                        
                    
                    if selectedtext == 6:
                        state = "NEXTLEVEL"
                    

        

        screen.fill((0,0,0)) 
        text = font_scoreboard.render("POWERUP SHOP", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,10))
        
        text = font_scoreboard.render(f"COINS: {coins}", True, (235,235,50))
        text_width = text.get_rect().width 
        screen.blit(text, ((10)/2,height-20))
        
        

        text = font_scoreboard.render(f"Tab = buy", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,70))

        if selectedtext == 1:
            bluetext = 100
        else:
            bluetext = 255
        text = font_scoreboard.render("+1 Health [5]", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,160))

        if selectedtext == 2:
            bluetext = 100
        else:
            bluetext = 255
        text = font_scoreboard.render("Bullet speed [3]", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,210))

        if selectedtext == 3:
            bluetext = 100
        else:
            bluetext = 255
        text = font_scoreboard.render("Bullet damage [10]", True, (bluetext,bluetext,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,260))

        if selectedtext == 4:
            bluetext = 100
        else:
            bluetext = 255
        if explosivebulletsmode == True:
            text = font_scoreboard.render("Increase explosion", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,310))
            text = font_scoreboard.render("size  [20]", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,340))
        else:
            text = font_scoreboard.render("Explosive", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,310))
            text = font_scoreboard.render("bullets  [20]", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,340))

        if selectedtext == 5:
            bluetext = 100
        else:
            bluetext = 255
        if penbullets:
            text = font_scoreboard.render("Increase", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,390))
            text = font_scoreboard.render("penetration [30]", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,420))
        else:
            text = font_scoreboard.render("Penetrating", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,390))
            text = font_scoreboard.render("bullets [30]", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,420))
        

        if selectedtext == 6:
            bluetext = 100
            text = font_scoreboard.render(f"Tab to Continue", True, (bluetext,bluetext,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,520))
        else:
            bluetext = 255
            text = font_scoreboard.render(f"SELECT to Continue", True, (180,180,180))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,520))



        


    
    
    elif state == "LEVELWIN1":
        #event logic
        events = pg.event.get()
        
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_TAB:
                    if currentgamemode == "SUPER":
                        state = "POWERUP"
                    else:
                        state = "NEXTLEVEL"
               
        #Drawing
        screen.fill((0,0,0)) 
        text = font_scoreboard.render("Level "f"{lvln}"" complete!", True, (5,255,5))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,50))

        text = font_scoreboard.render("You have been ", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,150))

        if currentgamemode == "SUPER":
            text = font_scoreboard.render("awarded 100 points", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,180))
            text = font_scoreboard.render("and 2 coins!", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,210))
        else:
            text = font_scoreboard.render("awarded 100 points!", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,180))
        
        


        
        text = font_scoreboard.render("Score: " f"{score:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,350))
        text = font_scoreboard.render("Highscore: " f"{highscore:04d}", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,380))

        text = font_scoreboard.render("Press [tab] to", True, (255,255,255))
        text_width = text.get_rect().width 
        screen.blit(text, ((width-text_width)/2,530))
        
        if currentgamemode == "SUPER":
            text = font_scoreboard.render("go to the SHOP", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,560))    
        else:
            text = font_scoreboard.render("continue", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((width-text_width)/2,560))


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