
from cairo import Context, PDFSurface
from cairo import LINE_JOIN_ROUND as rounded
from pangocairo import CairoContext
import pango
from pango import FontDescription
from rsvg import Handle as SVG
from StringIO import StringIO

class Card:
    font = "URW Palladio L, Roman"

    def __init__(self, title, description, width, height):
        self.title = title
        self.processDescription(description)
        self.w, self.h = width, height
        self.loadSVG()

    def processDescription(self, text):
        self.description = text

    def outputPDF(self):
        output = PDFSurface(None, self.w, self.h)
        self.outline(output)
        self.illustrate(output)
        self.typeset(output)
        return output

    def outline(self, surface):
        border = Context(surface)
        border.rectangle(self.w / 64, self.w / 64, self.w - self.w / 32, self.h - self.w / 32 - 2)
        border.set_line_width(self.w / 32)
        border.set_source_rgb(0.1, 0.1, 0.1)
        border.set_line_join(rounded)
        border.stroke()

    def panel(self, surface, y, h, shade, alpha):
        pane = Context(surface)
        pane.rectangle(self.w / 32, y, self.w * 15 / 16, y + h)
        pane.set_source_rgba(shade, shade, shade, alpha)
        pane.fill()

    def illustrate(self, surface):
        pass

    def typeset(self, surface):
        if self.description != "":
            self.renderText(surface, self.title, self.h * 2 / 5, self.w / 16, 0)
            self.renderText(surface, self.description, self.h / 2, self.w / 32, 0.1)
        else:
            self.renderText(surface, self.title, self.h * 4 / 9, self.w / 14, 0)

    def renderText(self, surface, text, y_offset, size, shade, w=(3,4)):
        origin = Context(surface)
        origin.set_source_rgb(shade, shade, shade)
        origin.translate(self.w * (w[1] - w[0]) / (w[1] * 2), y_offset)
        box = CairoContext(origin)
        layout = box.create_layout()
        layout.set_font_description(FontDescription(self.font + " " + str(size)))
        layout.set_width(self.w * w[0] / w[1] * pango.SCALE)
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_justify(True)
        layout.set_text(text)
        box.update_layout(layout)
        box.show_layout(layout)

    def loadSVG(self):
        svg_name = "Input/" + self.__class__.__name__ + "/" + self.title + ".svg"
        try:
            self.art = SVG(file=svg_name)
        except:
            print "Error processing", svg_name
            self.art = None

