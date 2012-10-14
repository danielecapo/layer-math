import fontforge
import layermath

font = fontforge.activeFont()

sum, scale = layermath.operation_space (font, ['n', 'o'])

layermath.add_glyphs (font, sum ('weight', 'width'), "boldext")
layermath.add_glyphs (font, sum (scale ('weight' 0.4, 0.9),\
                                     scale ('width', 0.2), scale ('square', 0.1)), \
                          "bold1")

