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
    radian = 0
    inv = 0
    
    def bbscale(time1):
        """
        時間で爆弾のスケールが増加する。
        ・当たり判定が増加しない
        ・加速度あげてない
        """
        bb_imgs = []
        time2 = int(time1 / 40)
        if time2 >= 9:
            time2 = 9
        for r in range(1, 11):
            bb_img = pg.Surface((20*r,20*r))
            pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            bb_img.set_colorkey((0, 0, 0))
            bb_rct = bb_img.get_rect()
            bb_imgs.append(bb_img)
        return bb_imgs[time2]
    
    #kk_muki = {[-5, 0]:pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9), [-5, 5]:pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9), [0, +5]:pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 0.9)}
    def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
        """
        こうかとんの進行方向に合わせて向きかえるやつ。
        """
        radian = 0
        inv = 0
        if sum_mv == [-5, 0]:
            radian = 0
            inv = 0
        elif sum_mv == [-5, 5]:
            radian = 45
            inv = 0
        elif sum_mv == [0, 5]:
            radian = 90
            inv = 90
        elif sum_mv == [5, 5]:#okasii
            radian = 45
            inv = 90
        elif sum_mv == [5, 0]:
            radian = 0
            inv = 90
        elif sum_mv == [5, -5]:#okasii
            radian = -45
            inv = 90
        elif sum_mv == [0, -5]:
            radian = 270
            inv = 0
        elif sum_mv == [-5, -5]:
            radian = 315
            inv = 0
        else:
            radian = 0
            inv = 0
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), radian, 0.9)#360
        kk_img = pg.transform.flip(kk_img, inv, 0)#90, 0で反転
        return kk_img
    
    def cale_orientation(org: pg.Rect, dst: pg.Rect,
                         current_xy: tuple[float, float]) -> tuple[float, float]:
        """
        爆弾の自動追尾、慣性なし
        """
        nolm_org = 0
        nolm_dst = 0
        ans = 0
        x_bb = 0
        y_bb = 0
        nolm_org = ((int(str(org[0]))**2)+(int(str(org[1]))**2))**(1/2)
        nolm_dst = ((int(str(dst[0]))**2)+(int(str(dst[1]))**2))**(1/2)
        ans = nolm_org - nolm_dst
        if int(str(org[0])) - int(str(dst[0])) > 0:
            x_bb = -1
        else:
            x_bb = 1
        if int(str(org[1])) - int(str(dst[1])) > 0:
            y_bb = -1
        else:
            y_bb = 1
        return [int(str(current_xy[0]))*x_bb, int(str(current_xy[1]))*y_bb]

    
    bb_rct = bbscale(tmr).get_rect()
    bb_rct.center = 700, 100
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)#360
    kk_img = pg.transform.flip(kk_img, 0, 0)#90, 0で反転
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

        bb_move = cale_orientation(bb_rct, kk_rct, [2, 2])
        #if cheak_bound(bb_rct) == "xout_left" or cheak_bound(bb_rct) == "xout_right":
            #x += 1
        #elif cheak_bound(bb_rct) == "yout_down" or cheak_bound(bb_rct) == "yout_up":
            #y += 1
        #bb_move[0] += 5 * ((-1)**x)
        #bb_move[1] += 5 * ((-1)**y)
        print(bb_move)
        


    

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
        bb_rct = bbscale(tmr).get_rect()
        screen.blit(get_kk_img(sum_mv), kk_rct)
        screen.blit(bbscale(tmr), bb_rct)
        print(tmr, bbscale(tmr), bb_rct)
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
