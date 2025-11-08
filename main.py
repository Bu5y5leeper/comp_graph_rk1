from PIL import Image
import math

image = Image.new('RGB', (250, 250))
triangle = [
    [60, 130],
    [100, 50],
    [140, 130],
]
dotted_triangle = [
    [56, 133],
    [100, 45],
    [144, 133],
]

circle = [100, 100]
circle_rad = 20
dotted_circle_rad = 17
arc_rad = 90

out_line = [[0, 7], [200, 110]]


def draw_line(img, point0, point1, color):
    x0 = point0[0]
    y0 = point0[1]
    x1 = point1[0]
    y1 = point1[1]

    dx = x1 - x0
    dy = y1 - y0

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x0, y0
    e = 0
    img.putpixel((x, y), color)
    for i in range(el):
        e += 2 * es
        if e > el:
            e -= 2 * el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        img.putpixel((x, y), color)


def draw_polygon(img, dots):
    for i in range(len(dots)):
        draw_line(img, dots[i], dots[(i + 1) % len(dots)], (255, 0, 0))


def draw_dotted_polygon(img, dots, gaps):
    for i in range(len(dots)):
        draw_dotted_line(img, gaps, dots[i], dots[(i + 1) % len(dots)], (255, 0, 0))


def get_side_array(dots):
    ret_arr = []
    for i in range(len(dots)):
        if dots[i][1] == dots[(i + 1) % len(dots)][1]:
            continue
        ret_arr.append(((dots[i][0], dots[i][1]), (dots[(i + 1) % len(dots)][0], dots[(i + 1) % len(dots)][1])))
    return ret_arr


def get_intersect(side, y):
    if side[0][1] < side[1][1]:
        side = side[::-1]
    if side[0][1] >= y > side[1][1]:
        t = (y - side[1][1]) / abs(side[0][1] - side[1][1])
        x0 = int(t * side[0][0] + (1 - t) * side[1][0])
        return x0, y


def get_intersect_array(sides, y):
    arr = []
    for side in sides:
        point = get_intersect(side, y)
        if point:
            arr.append(point)
    arr.sort(key=lambda a: a[0])
    return arr


def draw_dotted_line(img, gaps, point0, point1, color):
    line_parts = (gaps * 2) + 1
    dx = (point1[0] - point0[0]) / line_parts
    dy = (point1[1] - point0[1]) / line_parts
    dots_array = []
    for i in range(0, line_parts):
        dots_array.append((point0[0] + int(dx * i), point0[1] + int(dy * i)))
    dots_array.append(point1)
    for i in range(0, len(dots_array) - 1, 2):
        draw_line(img, dots_array[i], dots_array[i + 1], color)


def draw_circle(img, center, radius, color):
    x0, y0 = center
    x = 0
    y = radius
    delta = 2 - 2 * radius
    error = 0

    while y >= 0:
        img.putpixel((x0 + x, y0 + y), color)
        img.putpixel((x0 + x, y0 - y), color)
        img.putpixel((x0 - x, y0 + y), color)
        img.putpixel((x0 - x, y0 - y), color)

        error = 2 * (delta + y) - 1

        if delta < 0 and error <= 0:
            x += 1
            delta += 2 * x + 1
            continue

        error = 2 * (delta - x) - 1

        if delta > 0 and error > 0:
            y -= 1
            delta += 1 - 2 * y
            continue

        x += 1
        delta += 2 * (x - y)
        y -= 1


def draw_dotted_circle(img, segment_angle, center, radius, color):
    x0, y0 = center
    dx = 0
    dy = radius
    delta = 2 - 2 * radius
    error = 0

    while dy >= 0:
        for x, y in [(dx, dy), (dx, -dy), (-dx, dy), (-dx, -dy)]:
            angle = math.degrees(math.atan2(y, x)) % 360
            segment = int(angle / segment_angle)
            if segment % 2 == 0:
                img.putpixel((x0 + x, y0 + y), color)

        error = 2 * (delta + dy) - 1

        if delta < 0 and error <= 0:
            dx += 1
            delta += 2 * dx + 1
            continue

        error = 2 * (delta - dx) - 1

        if delta > 0 and error > 0:
            dy -= 1
            delta += 1 - 2 * dy
            continue

        dx += 1
        delta += 2 * (dx - dy)
        dy -= 1


def draw_arc_225(img, center, radius, color):
    x0, y0 = center
    x = 0
    y = radius
    delta = 1 - 2 * radius
    error = 0

    while y >= x:
        img.putpixel((x0 + x, y0 + y), color)
        img.putpixel((x0 - x, y0 + y), color)
        img.putpixel((x0 + y, y0 + x), color)
        img.putpixel((x0 - y, y0 + x), color)
        img.putpixel((x0 - y, y0 - x), color)

        error = 2 * (delta + y) - 1

        if delta < 0 and error <= 0:
            x += 1
            delta += 2 * x + 1
            continue

        error = 2 * (delta - x) - 1

        if delta > 0 and error > 0:
            y -= 1
            delta += 1 - 2 * y
            continue

        x += 1
        delta += 2 * (x - y)
        y -= 1


def segment_intersection(point0, point1, side):
    x1, y1 = point0
    x2, y2 = point1
    x3, y3 = side[0]
    x4, y4 = side[1]

    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if d == 0:
        return

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / d

    if 0 <= t <= 1 and 0 <= u <= 1:
        x = int(x1 + t * (x2 - x1))
        y = int(y1 + t * (y2 - y1))
        return x, y
    return


def draw_line_outside_polygon(img, point0, point1, sides, color):
    points = [point0]
    for side in sides:
        inter = segment_intersection(point0, point1, side)
        if inter:
            points.append(inter)

    points.append(point1)

    points.sort(key=lambda p: (p[0] - point0[0]) ** 2 + (p[1] - point0[1]) ** 2)

    for i in range(0, len(points) - 1, 2):
        draw_line(img, points[i], points[i + 1], color)


def fill_texture_outside_circle(img, intersect, texture_obj, circle_dot, radius):
    tex_w, tex_h = texture_obj.size
    cx, cy = circle_dot
    r2 = (radius + 2) ** 2

    for i in range(0, len(intersect) - 1, 2):
        x_start, y = intersect[i]
        x_end, _ = intersect[i + 1]
        x_start += 1
        if 0 <= y < img.height:
            for x in range(x_start, x_end):
                if 0 <= x < img.width:
                    if (x - cx) ** 2 + (y - cy) ** 2 >= r2:
                        tx = x % tex_w
                        ty = y % tex_h
                        color = texture_obj.getpixel((tx, ty))
                        img.putpixel((x, y), color)


def texture_fill(sides, polygon, circle_center, rad):
    texture = Image.open("texture.png").convert("RGB")

    for y in range(min(p[1] for p in polygon), max(p[1] for p in polygon)):
        intersect_array = get_intersect_array(sides, y)
        if len(intersect_array) >= 2:
            fill_texture_outside_circle(image, intersect_array, texture, circle_center, rad)


draw_polygon(image, triangle)
draw_dotted_polygon(image, dotted_triangle, 5)
draw_circle(image, circle, circle_rad, (255, 0, 0))
draw_dotted_circle(image, 30, circle, dotted_circle_rad, (255, 0, 0))
draw_arc_225(image, circle, arc_rad, (255, 0, 0))
polygon_sides = get_side_array(triangle)
draw_line_outside_polygon(image, out_line[0], out_line[1], polygon_sides, (255, 0, 0))
texture_fill(polygon_sides, triangle, circle, circle_rad)

image.save('kg.png')
