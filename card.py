import cairo
import pango
import pangocairo
import rsvg

from math import pi

class Card:
    width, height = 256, 384
    font = "Sans"
    border = 4

    def __init__(self, title, description):
        im = "Input/" + self.prefix + title + ".svg"
        out = "Output/" + self.prefix + title + ".svg"
        with open(out, 'w') as output:
            surface = cairo.SVGSurface(output, self.width, self.height)
            self.drawBorder(surface)
            if description != "":
                self.drawText(surface, title, self.height / 3)
                self.drawText(surface, description, self.height / 2, 9)
            else:
                self.drawText(surface, title, self.height / 2)
            self.drawImage(surface, self.loadSVG(im))
            surface.finish()

    def drawBorder(self, surface):
        context = cairo.Context(surface)
        context.rectangle(self.border/2, self.border/2,
                          self.width - 2 * self.border,
                          self.height - 2 * self.border)
        context.set_line_width(self.border)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()

    def drawText(self, surface, text, y_offset, size=18):
        context = cairo.Context(surface)
        context.move_to(self.width/2, y_offset)
        pangocairo_context = pangocairo.CairoContext(context)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription(self.font + " " + str(size))
        layout.set_font_description(font)
        layout.set_width((self.width - self.border) * 2)
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_text(text)
        context.set_source_rgb(0, 0, 0)
        pangocairo_context.update_layout(layout)
        pangocairo_context.show_layout(layout)

    def drawImage(self, surface, svg): 
        pass 

    def loadSVG(self, svg_name):
        try:
            return rsvg.Handle(file=svg_name)
        except:
            print "error processing " + svg_name
            return None

class Object(Card):
    prefix = "Objects/"
    def drawImage(self, surface, svg):
        if svg != None:
            context = cairo.Context(surface)
            context.scale(0.2, 0.2)
            context.translate(self.width / 2, self.height / 2)
            svg.render_cairo(context)
            context.translate(self.width * 4, self.height * 4)
            context.rotate(pi)
            svg.render_cairo(context)
            
            
            

def ReadList(name, cardType):
    with open(name) as ls:
        for line in ls:
            title, description = (l.strip() for l in line.split(":"))
            cardType(title, description)
