import turtle
import numpy as np
from PIL import Image

def hilbert_curve_drawing(order, face, dir, len):
    if order > 1:
        hilbert_curve_drawing(order - 1, face + (-1) ** (dir + 1), 1 - dir, len / 2)

        t.setheading(90 * face)
        t.forward(len / 2 ** (order - 1))

        hilbert_curve_drawing(order - 1, face, dir, len / 2)

        t.setheading(90 * (face + (-1) ** (dir + 1)))
        t.forward(len / 2 ** (order - 1))

        hilbert_curve_drawing(order - 1, face, dir, len / 2)

        t.setheading(90 * (face + 2 * ((-1) ** (dir + 1))))
        t.forward(len / 2 ** (order - 1))

        hilbert_curve_drawing(order - 1, face + (-1) ** dir, 1 - dir, len / 2)

    else:
        t.setheading(90 * face)

        t.forward(len)
        t.right(90 * (-1) ** dir)
        t.forward(len)
        t.right(90 * (-1) ** dir)
        t.forward(len)
        turtle.update()

def minValue(_x, _y, _pixel):
    m = float('inf')

    for i in range(4):
        for j in range(4):
            m = min(m, _pixel[_x + i][_y + j])

    return m

def compare(a, b):
    if a < b:
        return 1
    else:
        return -1

def draw(_x, _y, _modify):
    order1 = np.ceil(_modify[_x][_y] / 85)
    order2 = np.ceil(_modify[_x][_y + 1] / 85)
    order3 = np.ceil(_modify[_x + 1][_y + 1] / 85)
    order4 = np.ceil(_modify[_x + 1][_y] / 85)

    t.penup()
    t.goto(_x * 16 + 16 / (2 ** (order1 + 1)) - w * 16, _y * 16 + 16 / (2 ** (order1 + 1)) - h * 16)
    t.pendown()

    hilbert_curve_drawing(order1, 0, 1, 8)
    t.setheading(90)
    t.forward(8 / (2 ** order1))
    if order1 != order2:
        t.setheading(90 + 90 * compare(order1, order2))
        t.forward(abs(8 / (2 ** order1) - 8 / (2 ** order2)))
    t.setheading(90)
    t.forward(8 / (2 ** order2))

    hilbert_curve_drawing(order2, 1, 0, 8)
    t.setheading(0)
    t.forward(8 / (2 ** order2))
    if order2 != order3:
        t.setheading(180 + 90 * compare(order2, order3))
        t.forward(abs(8 / (2 ** order2) - 8 / (2 ** order3)))
    t.setheading(0)
    t.forward(8 / (2 ** order3))

    hilbert_curve_drawing(order3, 1, 0, 8)
    t.setheading(270)
    t.forward(8 / (2 ** order3))
    if order3 != order4:
        t.setheading(90 - 90 * compare(order3, order4))
        t.forward(abs(8 / (2 ** order3) - 8 / (2 ** order4)))
    t.setheading(270)
    t.forward(8 / (2 ** order4))

    hilbert_curve_drawing(order4, 2, 1, 8)

img = Image.open('./example.jpg')

grey_img = img.convert('L')
pixel = np.array(grey_img)

w = len(pixel) // 8
h = len(pixel[0]) // 8

modify = np.zeros((h * 2, w * 2), dtype = float)

for x in range(0, w * 2):
    for y in range(0, h * 2):
        modify[y][w * 2 - 1 - x] = minValue(x * 4, y * 4, pixel)

screen = turtle.Screen()
screen.setup(width = w * 64, height = h * 64)
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
turtle.tracer(0, 0)

img = Image.new("RGBA", (w * 64, h * 64), (255, 255, 255, 0))

for x in range(h):
    for y in range(w):
        draw(x * 2, y * 2, modify)

canvas = turtle.getcanvas()
canvas.postscript(file="tmp2.eps")
img = Image.open("tmp2.eps")
img.save(f'./hibert_art.png', "PNG")

turtle.done()