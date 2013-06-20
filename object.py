import cairo
import pango
import pangocairo
import rsvg

WIDTH, HEIGHT = 256, 384
FONTNAME = "Sans"

def MakeObjectCard (obj):
    with open("Cards/Objects/"+obj[0]+".svg", 'w') as output:
        surface = cairo.SVGSurface (output, WIDTH, HEIGHT)
        context = cairo.Context(surface)

        inputsvg = "Objects/"+obj[0]+".svg"
        print inputsvg
        handle = rsvg.Handle(file=inputsvg)
        
        context.translate(0, 128)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        layout = pangocairo_context.create_layout()
        font = pango.FontDescription(FONTNAME + " 25")
        layout.set_font_description(font)
        layout.set_text(obj[0])
        context.set_source_rgb(0, 0, 0)
        pangocairo_context.update_layout(layout)
        pangocairo_context.show_layout(layout)

        context.translate(0, 256)
        font = pango.FontDescription(FONTNAME + " 18")
        layout.set_font_description(font)
        layout.set_text(obj[1])
        context.set_source_rgb(0.01,0.01,0.01)
        pangocairo_context.update_layout(layout)
        pangocairo_context.show_layout(layout)

        surface.finish()


def ReadObjectList(fileName):
    with open(fileName) as ls:
        [MakeObjectCard(line.split(":")) for line in ls]
