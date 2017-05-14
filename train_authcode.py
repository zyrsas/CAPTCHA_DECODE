import urllib
from PIL import ImageFilter, Image
from identify_picture import identify_pic
from identify import identify_pic
import time

BLACK = 0
WHITE = 255
PIC_SIZE = (60, 20)


def get_pic(pic_namel):
    pic_name = pic_namel
    return pic_name


def convert_to_bw(pic_name):
    im = Image.open(pic_name)
    im.load()
    r = im.split()[0] # r,g,b
    filtered_r = r.filter(ImageFilter.DETAIL)

    threshold = 128
    table = [0]*threshold+[1]*(256-threshold)
    converted_r = filtered_r.point(table, '1')
    pic_name_bw = '%s.tif' % pic_name[:pic_name.rfind('.')]
    converted_r.save(pic_name_bw)
    return pic_name_bw


def get_flood_point(pic_size, pix):
    width, height = pic_size
    y_line = height / 2
    
    flood_point = []
    for x in range(width):
        if pix[x, y_line] == BLACK:
            flood_point.append((x, y_line))
    return flood_point


def append_pix(x, y, pix, stack, result):
    if x < 0 or x >= PIC_SIZE[0] or y < 0 or y >= PIC_SIZE[1]:
        return
    if pix[x, y] == BLACK:
        stack.append((x, y))
        result.append((x, y))
        pix[x, y] = WHITE


def flooding(start_pt, pix, pic_name):
    stack, result = [start_pt], [start_pt]
    left, right, up, down = 99, 0, 99, 0

    pix[start_pt[0], start_pt[1]] = WHITE
    while stack:
        pt = stack.pop(0)
        left = min(pt[0], left)
        right = max(pt[0], right)
        up = min(pt[1], up)
        down = max(pt[1], down)

        append_pix(pt[0] - 1, pt[1] - 1, pix, stack, result)
        append_pix(pt[0], pt[1] - 1, pix, stack, result)
        append_pix(pt[0] + 1, pt[1] - 1, pix, stack, result)
        append_pix(pt[0] - 1, pt[1], pix, stack, result)
        append_pix(pt[0] + 1, pt[1], pix, stack, result)
        append_pix(pt[0] - 1, pt[1] + 1, pix, stack, result)
        append_pix(pt[0], pt[1] + 1, pix, stack, result)
        append_pix(pt[0] + 1, pt[1] + 1, pix, stack, result)

    im_new = Image.new('L', (right - left + 1, down-up + 1))
    pix_new = im_new.load()
    for pt in result:
        pix_new[pt[0] - left, pt[1] - up] = WHITE
    im_new.save(pic_name)

    return pic_name


def split_pic(pic_name):
    im = Image.open(pic_name)
    pix = im.load()
    flood_point = get_flood_point(im.size, pix)

    count = 0
    result = ''
    for pt in flood_point:
        if pix[pt[0], pt[1]] == WHITE:
            continue
        sp_name = '%s_%d.png' % (pic_name[:pic_name.rfind('.')], count)
        flooding(pt, pix, sp_name)
        result += identify_pic(sp_name)
        count += 1
    return result


def split_picture(pic_name):
    im = Image.open(pic_name)
    pix = im.load()
    flood_point = get_flood_point(im.size, pix)

    count = 0
    result = ''
    for pt in flood_point:
        if pix[pt[0], pt[1]] == WHITE:
            continue
        sp_name = '%s_%d.png' % (pic_name[:pic_name.rfind('.')], count)
        flooding(pt, pix, sp_name)
        count += 1


def get_train_set(count=1000):
    for i in range(0, count):
        split_picture(convert_to_bw(get_pic('train_set\origin\%d.jpg' % i)))
        print (i)
        time.sleep(1)


if __name__ == '__main__':
    print(split_pic(convert_to_bw(get_pic('127.jpg'))))
    #get_train_set()