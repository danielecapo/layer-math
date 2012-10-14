import fontforge
import psMat

def layer_contours (font, glyph, layer):
    return font[glyph].layers[layer]

# map (lambda c: c, font[glyph].layers[layer])
        

def selector (font, glyphs):
    def get_layer (layer):
        return map (lambda glyph:\
                    [glyph, layer_contours (font, glyph, layer)],\
                    glyphs)
    return get_layer

def sum_contours (c1, c2, *cs):
    def inner_sum (c1, c2):
        c = c1.dup()
        for i in range(len(c)):
            c[i].transform(psMat.translate(c2[i].x, c2[i].y))
        return c
    return reduce (inner_sum,  (c1, c2) + cs)

def scale_contour (c1, x, y=None):
    if y==None:
        y = x
    return c1.dup().transform(psMat.scale(x, y))


def sum_glyphs (l1, l2, *ls):
    def inner_sum (l1, l2):
        return map (sum_contours, l1, l2)
    return reduce (inner_sum, (l1, l2) + ls)
    # l = l1.dup()
    # for i in range (len(l)):
    #     l[i] = sum_contours (l1[i], l2[i])
    # return l
#    

def scale_glyph (l1, x, y=None):
    return map (lambda c: scale_contour(c, x, y), l1) 
    # l = l1.dup()
    # for i in range (len(l)):
    #     l[i] = scale_contour (l1[i], x, y)
    # return l
#
    
def sum (l1, l2, *ls):
    def inner_sum (l1, l2):
        return map (lambda l1, l2: [l1[0], sum_glyphs(l1[1], l2[1])], l1, l2)
    return reduce (inner_sum, (l1, l2) + ls)

def scale (l1, x, y=None):
    return map (lambda l: [l[0], scale_glyph(l[1], x, y)], l1)

def operation_space (font, glyphs):
    s = selector (font, glyphs)
    o = s(1)
    minus_o = scale (o, -1)

    def summer (l1, l2, *ls):
        def inner_sum (l1, l2):
            if isinstance (l1, str):
                a1 = s(l1)
            else:
                a1 = l1
            if isinstance (l2, str):
                a2 = s(l2)
            else:
                a2 = l2
            return sum(sum (a1, a2), minus_o)
        return reduce (inner_sum, (l1, l2) + ls)

    def scaler (l1, x, y=None):
        if isinstance (l1, str):
            a1 = s(l1)
        else:
            a1 = l1
        return sum (scale(sum (a1, minus_o), x, y), o)

    return (summer, scaler)

def design_space (font, glyphs, layers):
    s, m = operation_space (font, glyphs)
    def get_by_coord (*coord):
        scaled = map (lambda l, crd: apply (m, [l]+crd), layers, coord)
        return apply (s, scaled)
    return get_by_coord
        
        
    

def add_glyph (font, glyph, ext):
    new_glyph = font.createChar(-1, glyph[0] + "." + ext)
    nl = fontforge.layer()
    for c in glyph[1]:
        nl += c
    new_glyph.layers[1] = nl

def add_glyphs (font, glyphs, ext):
    for glyph in glyphs:
        add_glyph (font, glyph, ext)

