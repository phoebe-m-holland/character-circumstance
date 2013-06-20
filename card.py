import cairo
import pango
import pangocairo
import rsvg

class Card:
    width, height = 256, 384
    font = "Sans"

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
            self.printText(context, description, self.description_y)
            surface.finish()

    def printText(self, context, text, y_offset):
        context.move_to(self.width/2, y_offset)
        pangocairo_context = pangocairo.CairoContext(context)
#        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription(self.font + " 25")
        layout.set_font_description(font)
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

