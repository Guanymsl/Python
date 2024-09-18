import turtle
from PIL import Image

pix = 512
screen = turtle.Screen()
screen.setup(width = pix, height = pix)
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

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

def hilbert_curve(order: int):

    img = Image.new("RGBA", (pix, pix), (255, 255, 255, 0))

    t.penup()
    t.goto(pix / (2 ** (order + 1)) - pix / 2, pix / (2 ** (order + 1)) - pix / 2)
    t.pendown()
    hilbert_curve_drawing(order, 1, 0, pix / 2)

    canvas = turtle.getcanvas()
    canvas.postscript(file="tmp.eps")
    img = Image.open("tmp.eps")
    img.save(f'./h{order}.png', "PNG")

    t.clear()

for i in range(1, 5):
    hilbert_curve(i)