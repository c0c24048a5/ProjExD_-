import os
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    r = 0
    tmr = 0
    
    def bbscale(time1):
        bb_imgs = []
        time2 = int(time1 / 40)
        if time2 >= 9:
            time2 = 9
        for r in range(1, 11):
            bb_img = pg.Surface((20*r,20*r))
            pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            bb_img.set_colorkey((0, 0, 0))
            bb_imgs.append(bb_img)
        return bb_imgs[time2]
    


    
    bb_rct = bbscale(tmr).get_rect()
    bb_rct.center = 700, 100
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 100, 200
    clock = pg.time.Clock()
    
    DELTA = {"up":None, "down":None, "left":None, "right":None}
    A = 0
    B = 0
    C = 0
    D = 0
    x = 0
    y = 0

    def cheak_bound(position):
        """
        引数：rect
        戻り値：上下左右の判定結果
        """
        size = int(str(position[3]))
        if position[0] >= 1100 - size:
            return "xout_left"
        elif position[0] <= 0:
            return "xout_right"
        elif position[1] >= 650 - size:
            return "yout_down" 
        elif position[1] <= 0:
            return "yout_up"
        else:
            return True
        
    def gameover(screen: pg.Surface) -> None:
        """
        かなり荒いので修正の必要あり
        ・テキストを中心に出す方法
        ・イメージとテキストを同時に並べる方法
        """
        blackout = pg.Surface((1100, 650))
        pg.draw.rect(blackout, (0, 0, 0), (0, 0,1100, 650), 1)
        pg.Surface.set_alpha(blackout, 100)
        fonto = pg.font.Font(None, 90)
        kks_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
        txt = fonto.render("GAMEOVER",
                           True, (0, 0, 0))
        screen.blit(blackout, [0, 0])
        screen.blit(kks_img, [450, 300])
        screen.blit(txt, [500, 300])
        screen.blit(kks_img, [870, 300])
        pg.display.update()
        time.sleep(5)
        return main

        #一瞬しか出ないが
        
    


    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        bb_move = [0, 0]
        if cheak_bound(bb_rct) == "xout_left" or cheak_bound(bb_rct) == "xout_right":
            x += 1
        elif cheak_bound(bb_rct) == "yout_down" or cheak_bound(bb_rct) == "yout_up":
            y += 1
        bb_move[0] += 5 * ((-1)**x)
        bb_move[1] += 5 * ((-1)**y)

    

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        if key_lst[pg.K_UP]:
            if cheak_bound(kk_rct) != "yout_up":    
                sum_mv[1] -= 5
                A += int(sum_mv[1])
                DELTA["up"] = A

        if key_lst[pg.K_DOWN]:
            if cheak_bound(kk_rct) != "yout_down":
                sum_mv[1] += 5
                B += int(sum_mv[1])
                DELTA["down"] = B
            
        if key_lst[pg.K_LEFT]:
            if cheak_bound(kk_rct) != "xout_right":
                sum_mv[0] -= 5
                C += int(sum_mv[0])
                DELTA["left"] = C

        if key_lst[pg.K_RIGHT]:
            if cheak_bound(kk_rct) != "xout_left":
                sum_mv[0] += 5
                D += int(sum_mv[1])
                DELTA["right"] = D
             
        kk_rct.move_ip(sum_mv)
        bb_rct.move_ip(bb_move)
        screen.blit(kk_img, kk_rct)
        screen.blit(bbscale(tmr), bb_rct)
        print(tmr, bbscale(tmr))
        pg.display.update()
        tmr += 1
        clock.tick(50)
        #print(kk_rct)
        if kk_rct.colliderect(bb_rct):
            #return main
            gameover(screen)





if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
