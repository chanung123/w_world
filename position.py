
FIREPOSITION = 35
BOXSCALE = 130
MARGIN = 100

#격자 스케일(이미지 정렬)
def point_core(postionx, postiony, box_scale, scale):
    #중심을 기준으로 포지션
    if box_scale < scale:
        if postionx >= 0 and postionx <= 3:
            if postiony >= 0 and postiony <= 3:
                return ((postionx * BOXSCALE) + MARGIN - (scale-box_scale)/2, ((postiony) * BOXSCALE) + MARGIN -(scale-box_scale)/2)
        if postionx > 3 or postiony > 3:
            return ((postionx * BOXSCALE) + MARGIN - (scale-box_scale)/2, ((postiony-1) * BOXSCALE) + MARGIN - (scale-box_scale)/2)
    if box_scale == scale:
        if postionx >= 0 and postionx <= 3:
            if postiony >= 0 and postiony <= 3:
                return ((postionx * BOXSCALE) + MARGIN, ((postiony) * BOXSCALE) + MARGIN)
        if postionx > 3 or postiony > 3:
            return (((postionx) * BOXSCALE) + MARGIN, ((postiony - 1) * BOXSCALE) + MARGIN)
    if box_scale > scale:
        if postionx >= 0 and postionx <= 3:
            if postiony >= 0 and postiony <= 3:
                return ((postionx * BOXSCALE) + MARGIN + (box_scale-scale)/2, ((postiony) * BOXSCALE) + MARGIN + (box_scale-scale)/2)
        if postionx > 3 or postiony > 3:
            return ((postionx * BOXSCALE) + MARGIN + (box_scale-scale)/2, ((postiony-1) * BOXSCALE) + MARGIN + (box_scale-scale)/2)

#마우스 격자
def mouse_pos_x(pos_x):
    if pos_x >= MARGIN and pos_x < MARGIN + BOXSCALE:
        return 0
    if pos_x >= MARGIN + BOXSCALE and pos_x < MARGIN + (BOXSCALE*2):
        return 1
    if pos_x >= MARGIN + (BOXSCALE*2) and pos_x < MARGIN + (BOXSCALE*3):
        return 2
    if pos_x >= MARGIN + (BOXSCALE*3) and pos_x < MARGIN + (BOXSCALE*4):
        return 3
    else:
        return 0

def mouse_pos_y(pos_y):
    if pos_y >= MARGIN and pos_y < MARGIN + BOXSCALE:
        return 0
    if pos_y >= MARGIN + BOXSCALE and pos_y < MARGIN + (BOXSCALE*2):
        return 1
    if pos_y >= MARGIN + (BOXSCALE*2) and pos_y < MARGIN + (BOXSCALE*3):
        return 2
    if pos_y >= MARGIN + (BOXSCALE*3) and pos_y < MARGIN + (BOXSCALE*4):
        return 3
    else:
        return 0

def point(postionx, postiony):
    """플레이어 포지션 정하기"""
    if postionx >= 0 and postionx <= 3:
        if postiony >= 0 and postiony <= 3:
            return ((postionx * BOXSCALE) + MARGIN, ((postiony) * BOXSCALE) + MARGIN)

    if postionx > 3 or postiony > 3:
        return (((postionx) * BOXSCALE) + MARGIN, ((postiony - 1) * BOXSCALE) + MARGIN)

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
    screen.blit(fire_img_down, (BOXSCALE + FIREPOSITION, BOXSCALE * 4 + FIREPOSITION * 2))
    screen.blit(fire_img_down, ((3 * BOXSCALE) + 35, BOXSCALE * 4 + FIREPOSITION * 2))
    screen.blit(fire_img_left, (0, BOXSCALE + FIREPOSITION))
    screen.blit(fire_img_left, (0, (3 * BOXSCALE) + FIREPOSITION))
    screen.blit(fire_img_right, ((4 * BOXSCALE) + FIREPOSITION * 2, BOXSCALE + FIREPOSITION))
    screen.blit(fire_img_right,((4 * BOXSCALE) + FIREPOSITION * 2, (3 * BOXSCALE) + FIREPOSITION),)