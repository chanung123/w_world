FIREPOSITION = 35
BOXSCALE = 130
MARGIN = 100


# 격자 스케일(이미지 정렬)
def point_core(pos_x, pos_y, scale):
    """중심을 기준으로 포지션"""

    if (0 <= pos_x <= 3) and (0 <= pos_y <= 3):
        if BOXSCALE < scale:
            return (
                (pos_x * BOXSCALE) + MARGIN - (scale - BOXSCALE) / 2,
                ((pos_y) * BOXSCALE) + MARGIN - (scale - BOXSCALE) / 2,
            )
        if BOXSCALE == scale:
            return ((pos_x * BOXSCALE) + MARGIN, ((pos_y) * BOXSCALE) + MARGIN)
        if BOXSCALE > scale:
            return (
                (pos_x * BOXSCALE) + MARGIN + (BOXSCALE - scale) / 2,
                ((pos_y) * BOXSCALE) + MARGIN + (BOXSCALE - scale) / 2,
            )
    if pos_y > 3 or pos_x > 3 :
        if BOXSCALE < scale:
            return (
                (4 * BOXSCALE) + MARGIN - (scale - BOXSCALE) / 2,
                ((4) * BOXSCALE) + MARGIN - (scale - BOXSCALE) / 2,
            )
        if BOXSCALE == scale:
            return ((4 * BOXSCALE) + MARGIN, ((4) * BOXSCALE) + MARGIN)
        if BOXSCALE > scale:
            return (  
                (4 * BOXSCALE) + MARGIN + (BOXSCALE - scale) / 2,
                ((4) * BOXSCALE) + MARGIN + (BOXSCALE - scale) / 2,
            )
        
    if pos_y < 0 or pos_x < 0 :
        if BOXSCALE < scale:
            return (
                (1 * BOXSCALE) + MARGIN - (scale - BOXSCALE) / 2,
                ((1) * BOXSCALE) + MARGIN - (scale - BOXSCALE) / 2,
            )
        if BOXSCALE == scale:
            return ((1 * BOXSCALE) + MARGIN, ((1) * BOXSCALE) + MARGIN)
        if BOXSCALE > scale:
            return (  
                (1 * BOXSCALE) + MARGIN + (BOXSCALE - scale) / 2,
                ((1) * BOXSCALE) + MARGIN + (BOXSCALE - scale) / 2,
            )
        
        



# 마우스 격자
def mouse_pos_x(pos_x):
    if pos_x < MARGIN :
        return 0
    if pos_x >= MARGIN and pos_x < MARGIN + BOXSCALE:
        return 0
    if pos_x >= MARGIN + BOXSCALE and pos_x < MARGIN + (BOXSCALE * 2):
        return 1
    if pos_x >= MARGIN + (BOXSCALE * 2) and pos_x < MARGIN + (BOXSCALE * 3):
        return 2
    if pos_x >= MARGIN + (BOXSCALE * 3) and pos_x < MARGIN + (BOXSCALE * 4):
        return 3
    if pos_x >= MARGIN + (BOXSCALE * 4): 
        return 3


def mouse_pos_y(pos_y):
    if pos_y < MARGIN :
        return 0
    if pos_y >= MARGIN and pos_y < MARGIN + BOXSCALE:
        return 0
    if pos_y >= MARGIN + BOXSCALE and pos_y < MARGIN + (BOXSCALE * 2):
        return 1
    if pos_y >= MARGIN + (BOXSCALE * 2) and pos_y < MARGIN + (BOXSCALE * 3):
        return 2
    if pos_y >= MARGIN + (BOXSCALE * 3) and pos_y < MARGIN + (BOXSCALE * 4):
        return 3
    if pos_y >= MARGIN + (BOXSCALE * 4): 
        return 3
    
    


def point(pos_x, pos_y):
    """플레이어 포지션 정하기"""
    if (0 <= pos_x <= 3) and (0 <= pos_y <= 3):
        return ((pos_x * BOXSCALE) + MARGIN, ((pos_y) * BOXSCALE) + MARGIN)
    if pos_x > 3 :
        return ((4 * BOXSCALE) + MARGIN, ((pos_y) * BOXSCALE) + MARGIN)
    if pos_y > 3 :
        return ((pos_x * BOXSCALE) + MARGIN, (4 * BOXSCALE) + MARGIN)
    
    
def point_fireball(pos_x, pos_y):
    """파이어볼 포지션 정하기"""
    if (0 <= pos_x <= 3) and (0 <= pos_y <= 3):
        return ((pos_x * BOXSCALE) + MARGIN + 66, ((pos_y) * BOXSCALE) + MARGIN + 66)
    if pos_x > 3 :
        return ((4 * BOXSCALE) + MARGIN+ 66, ((pos_y) * BOXSCALE) + MARGIN+ 66)
    if pos_y > 3 :
        return ((pos_x * BOXSCALE) + MARGIN+ 66, (4 * BOXSCALE) + MARGIN+ 66)
    



def RenderMap(
    screen,
    map_img,
    fire_img,
    fire_img_down,
    fire_img_left,
    fire_img_right,
):
    screen.blit(map_img, (24, 10))
    screen.blit(fire_img, (BOXSCALE + FIREPOSITION, 0))
    screen.blit(fire_img, ((3 * BOXSCALE) + FIREPOSITION, 0))
    screen.blit(
        fire_img_down, (BOXSCALE + FIREPOSITION, BOXSCALE * 4 + FIREPOSITION * 2)
    )
    screen.blit(fire_img_down, ((3 * BOXSCALE) + 35, BOXSCALE * 4 + FIREPOSITION * 2))
    screen.blit(fire_img_left, (0, BOXSCALE + FIREPOSITION))
    screen.blit(fire_img_left, (0, (3 * BOXSCALE) + FIREPOSITION))
    screen.blit(
        fire_img_right, ((4 * BOXSCALE) + FIREPOSITION * 2, BOXSCALE + FIREPOSITION)
    )
    screen.blit(
        fire_img_right,
        ((4 * BOXSCALE) + FIREPOSITION * 2, (3 * BOXSCALE) + FIREPOSITION),
    )
