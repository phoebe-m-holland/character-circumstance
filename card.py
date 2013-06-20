import cairo
import pango
import pangocairo
import rsvg

class Card:
    width, height = 256, 384
    font = "Sans"
    x_border = 16
    title_y = 128
    description_y = 256

    def __init__(self, title, description):
        im = "Input/" + self.prefix + title + ".svg"
        out = "Output/" + self.prefix + title + ".svg"
        with open(out, 'w') as output:
            surface = cairo.SVGSurface(output, self.width, self.height)
            context = cairo.Context(surface)
            handle = rsvg.Handle(file=im)
            self.printText(context, title, self.title_y)
            self.printText(context, description, self.description_y, 9)
            surface.finish()

    def drawBorder(self):
        cairo_new_sub_path

    def printText(self, context, text, y_offset, size=18):
        context.move_to(self.width/2, y_offset)
        pangocairo_context = pangocairo.CairoContext(context)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription(self.font + " " + str(size))
        layout.set_font_description(font)
        layout.set_width(self.width - self.x_border)
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_text(text)
        context.set_source_rgb(0, 0, 0)
        pangocairo_context.update_layout(layout)
        pangocairo_context.show_layout(layout)


class Object(Card):
    prefix = "Objects/"

def ReadList(name, cardType):
    with open(name) as ls:
        for line in ls:
            title, description = line.split(":")
            cardType(title, description)

