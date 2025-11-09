import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.image import imread
from skimage.transform import resize


width, height = 200, 200
canvas = np.ones((height, width, 3))

def put_pixel(x, y, color=(0, 0, 0)):
    if 0 <= x < width and 0 <= y < height:
        canvas[y, x] = color

def draw_line(x1, y1, x2, y2, color=(0, 0, 0)):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        put_pixel(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_dashed_line(x1, y1, x2, y2, dash=4, gap=4, color=(0, 0, 0)):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    count = 0
    draw = True

    while True:
        if draw:
            put_pixel(x1, y1, color)
        count += 1
        if count == dash:
            draw = False
        if count == dash + gap:
            draw = True
            count = 0

        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_circle(cx, cy, r, color=(0, 0, 0)):
    x = r
    y = 0
    err = 1 - x
    while x >= y:
        for dx, dy in [(x,y),(y,x),(-y,x),(-x,y),(-x,-y),(-y,-x),(y,-x),(x,-y)]:
            put_pixel(cx + dx, cy + dy, color)
        y += 1
        if err < 0:
            err += 2*y + 1
        else:
            x -= 1
            err += 2*(y - x + 1)


def sign(p1, p2, p3):
    return (p1[0] - p3[0])*(p2[1] - p3[1]) - (p2[0] - p3[0])*(p1[1] - p3[1])

def point_in_triangle(x, y, A, B, C):
    p = (x, y)
    b1 = sign(p, A, B) < 0
    b2 = sign(p, B, C) < 0
    b3 = sign(p, C, A) < 0
    return b1 == b2 == b3


A = (60, 130)
B = (100, 50)
C = (140, 130)

center = (100, 100)
r = 20
r_dash = 17


try:
    img = imread("pict2.jpg")
    img_resized = resize(img, (height, width))

    for x in range(width):
        for y in range(height):
            if point_in_triangle(x, y, A, B, C):

                if math.hypot(x - center[0], y - center[1]) > r:
                    canvas[y, x] = img_resized[y, x]

except FileNotFoundError:
    print("Файл your_image.jpg не найден")


draw_line(*A, *B)
draw_line(*B, *C)
draw_line(*C, *A)


draw_circle(center[0], center[1], r)


for i in range(6):
    start = math.radians(i * 60)
    end = math.radians(i * 60 + 30)
    a = start
    while a <= end:
        x = int(center[0] + r_dash * math.cos(a))
        y = int(center[1] + r_dash * math.sin(a))
        put_pixel(x, y)
        a += math.radians(1)


A2 = (56, 133)
B2 = (100, 45)
C2 = (144, 133)

draw_dashed_line(*A2, *B2)
draw_dashed_line(*B2, *C2)
draw_dashed_line(*C2, *A2)


canvas = np.flipud(canvas)


plt.imshow(canvas)
plt.axis('off')
plt.show()
