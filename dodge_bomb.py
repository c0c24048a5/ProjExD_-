import os
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

def bbscale(time1: int) -> tuple[int, int]:
        """
        時間で爆弾のスケールが増加する。
        """
        r = 0
        bb_imgs = []
        time2 = int(time1 / 40)
        if time2 >= 9:
            time2 = 9
        for r in range(1, 11):
            bb_img = pg.Surface((20*r,20*r))
            pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            bb_img.set_colorkey((0, 0, 0))
            #bb_rct = bb_img.get_rect()
            bb_imgs.append(bb_img)
        return bb_imgs[time2]

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
        elif sum_mv == [5, 5]:
            radian = 45
            inv = 90
        elif sum_mv == [5, 0]:
            radian = 0
            inv = 90
        elif sum_mv == [5, -5]:
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
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), radian, 0.9)
        kk_img = pg.transform.flip(kk_img, inv, 0)
        return kk_img

def cale_orientation(org: pg.Rect, dst: pg.Rect,
                         current_xy: tuple[float, float], bb_move1) -> tuple[float, float]:
        """
        爆弾の自動追尾、慣性なし
        """
        nolm = 0
        ans = [0, 0]
        x_bb = 0
        y_bb = 0
        nolm = ((int(org[0]) - int(dst[0]))**2 + ((int(org[1])) - (int(dst[1])))**2)**(1/2)
        if int(str(org[0])) - int(str(dst[0])) > 0:
            x_bb = -1
        else:
            x_bb = 1
        if int(str(org[1])) - int(str(dst[1])) > 0:
            y_bb = -1
        else:
            y_bb = 1
        if nolm < 300:
            print(bb_move1)
            #return current_xy
            return bb_move1
        else:
            ans = [int(current_xy[0])*x_bb, int(current_xy[1])*y_bb]
        return ans

def bb_accs(time3):
        """
        爆弾の加速
        """
        t = 0
        accs = []
        acc = [1, 1]
        time4 = int(time3 / 160)
        if time4 > 9:
            time4 = 9
        for t in range(1, 11):
            acc = [1*t, 1*t]
            accs.append(acc)
            #print(acc)
        return accs[time4]

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

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    tmr = 0
    bb_move = [0, 0]
    bb_rct = bbscale(tmr).get_rect()
    bb_rct.center = 700, 100
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)#360
    kk_img = pg.transform.flip(kk_img, 0, 0)#90, 0で反転
    kk_rct = kk_img.get_rect()
    kk_rct.center = 100, 200
    clock = pg.time.Clock()
    
    DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0, 5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(5, 0)}
    x = 0
    y = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        
        bb_move = cale_orientation(bb_rct, kk_rct, bb_accs(tmr), bb_move)

        #以下bb用のcheak_boundの残骸
        # if cheak_bound(bb_rct) == "xout_right" or cheak_bound(bb_rct) == "xout_left":
        #      bb_rct.move_ip([-int(bb_move[0]), 0])
        # elif cheak_bound(bb_rct) == "yout_down" or cheak_bound(bb_rct) == "yout_up":
        #      bb_rct.move_ip([0, -int(bb_move[1])])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key] == True:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if cheak_bound(kk_rct) == "xout_right" or cheak_bound(kk_rct) == "xout_left":
            kk_rct.move_ip([-int(sum_mv[0]), 0])
        if cheak_bound(kk_rct) == "yout_up" or cheak_bound(kk_rct) == "yout_down":
            kk_rct.move_ip([0, -int(sum_mv[1])])

        bb_rct.move_ip(bb_move)
        screen.blit(get_kk_img(sum_mv), kk_rct)
        screen.blit(bbscale(tmr), bb_rct)
        bb_rct[2] = bbscale(tmr).get_rect()[2]
        bb_rct[3] = bbscale(tmr).get_rect()[3]
        print(bb_rct)
        #print(tmr, bbscale(tmr), bb_rct)
        #print(bb_move)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        #print(kk_rct)
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return main





if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
