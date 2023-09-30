# tests for feature 1
def tests1():
    # simple examples with one hole

    num = 2
    pvars = ['y', 'x']
    examples_before = [('_', 0), ('_', 1)]
    examples_after = [(1, 0), (2, 1)]
    prog_in = "y:= x + ??"
    prog_out = "y:= x + 1"

    num = 2
    pvars = ['y', 'x']
    examples_before = [('_', 2), ('_', 4)]
    examples_after = [(0, 2), (2, 4)]
    prog_in = "y:= x - ??"
    prog_out = "y:= x - 2"

    num = 3
    pvars = ['y', 'x']
    examples_before = [('_', 0), ('_', 2), ('_', 3)]
    examples_after = [(0, 0), (4, 2), (6, 3)]
    prog_in = "y:= x * ??"
    prog_out = "y:= x * 2"

    num = 3
    pvars = ['y', 'x']
    examples_before = [('_', 1), ('_', 2), ('_', 3)]
    examples_after = [(4, 1), (7, 2), (10, 3)]
    prog_in = "y:= x * ?? + 1"
    prog_out = "y:= x * 3 + 1"

    num = 2
    pvars = ['z', 'x', 'y']
    examples_before = [(0, 1, '_'), (1, 3, '_')]
    examples_after = [('_', '_', 4), ('_', '_', 7)]
    prog_in = "z:= x + y + ??"
    prog_out = "z:= x + y + 3"

    # simple examples with two hole

    num = 3
    pvars = ['y', 'x']
    examples_before = [('_', 0), ('_', 1), ('_', 2)]
    examples_after = [(2, 0), (6, 1), (10, 2)]
    prog_in = "y:= x * ?? + ?? "
    prog_out = "y:= x * 4 + 2"

    num = 3
    pvars = ['y', 'x', 'z']
    examples_before = [('_', 1, 2), ('_', 2, 1), ('_', 3, 3)]
    examples_after = [(10, 1, 2), (12, 2, 1), (17, 3, 3)]
    prog_in = "y:= x * ?? + z + ??"
    prog_out = "y:= x * 3 + z + 5"

    num = 2
    pvars = ['z', 'y', 'x']
    examples_before = (('_', '_', 1), ('_', '_', 2))
    examples_after = ((4, 4, 1), (8, 8, 2))
    prog_in = " z := ?? ; y := x * z"
    prog_out = " z := 4 ; y := x * z"

    # if statements with holes

    num = 3
    pvars = ['x', 'y']
    examples_before = [(1, '_'), (3, '_'), (4, '_')]
    examples_after = [(1, 5), (3, 6), (4, 7)]
    prog_in = "if x >= 3 then y:= x + ?? else y:= 5"
    prog_out = "if x >= 3 then y:= x + 3 else y:= 5"

    num = 3
    pvars = ['z', 'x', 'y']
    examples_before = [('_', 1, '_'), ('_', 2, '_'), ('_', 3, '_')]
    examples_after = [(2, 1, 3), (3, 2, 3), (4, 3, 4)]
    prog_in = "z:= x + ?? ; if  z >= 3 then y:= x + 1 else y:= x + ??"
    prog_out = "z:= x + 1 ; if  z >= 3 then y:= x + 1 else y:= x + 2"

    num = 4
    pvars = ['x', 'y']
    examples_before = [(1, '_'), (2, '_'), (3, '_'), (4, '_')]
    examples_after = [(1, 4), (2, 4), (3, 18), (4, 24)]
    prog_in = "if x > 2 then y:= x * ?? else y:= ??"
    prog_out = "if x > 2 then y:= x * 6 else y:= 4"

    num = 4
    pvars = ['x', 'y']
    examples_before = [(0, '_'), (1, '_'), (4, '_'), (5, '_')]
    examples_after = [(0, 0), (1, 2), (4, 4), (5, 5)]
    prog_in = "if x >= ?? then y:= x * ?? else y:= x * ??"
    prog_out = "if x >= 2 then y:= x * 1 else y:= x * 2"

    # while loops with holes

    num = 3
    pvars = ['y', 'x']
    examples_before = (('_', 0), ('_', 1), ('_', 2))
    examples_after = ((8, 1), (5, 1), (6, 2))
    prog_in = " y := 0 ; while y < ?? do ( y := y + x + ??)"
    prog_out = " y := 0 ; while y < 5 do ( y := y + x + 4)"

    num = 3
    pvars = ['x', 'y']
    examples_before = [(0, 0), (1, 2), (2, 2)]
    examples_after = [(9, 1), (14, 4), (8, 3)]
    prog_in = " while x < 8 do ( x := x + y + 4 ; y:= y + ??)"
    prog_out = " while x < 8 do ( x := x + y + 4 ; y:= y + 1)"

    num = 3
    pvars = ['x', 'y']
    examples_before = [(0, 0), (1, 2), (2, 2)]
    examples_after = [(9, 1), (14, 4), (8, 3)]
    prog_in = " while x < 8 do ( x := x + y + 4 ; y:= y + ??)"
    prog_out = " while x < 8 do ( x := x + y + 4 ; y:= y + 1)"


#######################################################################################################
# tests for feature 2

def tests2():
    pvars = ['x']
    prog_in = "x := 5 + ?? ; assert x = 7"
    prog_out = "x := 5 + 2"

    pvars = ['x']
    prog_in = "x := 2 - ?? ; assert x > 0"
    prog_out = "x := 2 - 1"

    pvars = ['y', 'x']
    prog_in = "y := ?? * x ; assert y = x + x + x"
    prog_out = "y := 3 * x"

    pvars = ['y', 'x']
    prog_in = "y := x + ?? ; assert y = x"
    prog_out = "y := x + 0"

    pvars = ['y', 'x']
    pre_conditions = ['x == 2']
    post_conditions = ['y == 7']
    prog_in = "y := x + ?? ; assert y >= x"
    prog_out = "y := x + 5"

    pvars = ['x', 'y', 'z']
    prog_in = "x := x + 1 ; y := x + x ; z := x * ?? + ?? ; assert z = x + y"
    prog_out = "x := x + 1 ; y := x + x ; z := x * 3 + 1"

    pvars = ['x', 'y']
    pre_conditions = ['y > 0']
    post_conditions = ['y == 9']
    prog_in = "x := 8; y:= ??; assert (y > x); y = y - ??; assert (x > y)"
    prog_out = "x := 8; y:= 9; assert (y > x); y = y - 2 ;"

    pvars = ['x', 'y']
    prog_in = "x := 2 * ??; if x = 6 then y:= 4; assert y = 4 else skip"
    prog_out = "x := 2 * 3; if x = 6 then y:= 4  else skip"

    pvars = ['x', 'z', 'y']
    prog_in = "x := 8 + ?? , z:= x + y;  if z = 20 then y := 8 else y := 5; assert y = 8"
    prog_out = "x := 8 + 4 , z:= x + y;  if z = 20 then y := 8 else y := 5"

    pvars = ['x', 'z', 'y']
    pre_conditions = ['And(y > 0 , z > 0)']
    post_conditions = ['And(x==12 ,y==8)']
    prog_in = "x := 8 + ?? , if z = y + ?? then y := 20 - x else y := 5; assert y > 5"
    prog_out = "x := 8 + 4 , if z = y + 4 then y := 20 - x else y := 5"

    pvars = ['y', 'x', 'z', 'i']
    pre_conditions = ['x > 0']
    post_conditions = ['']
    prog_in = "y := x + ?? ; z := y + ?? ; i = x * ?? ; if z = 10 then i * x := 8 else i * x := 10 ; assert z = 10"
    prog_out = "y := x + 3 ; z := y + 5 ; i = x * 2 ; if z = 10 then i * x := 8 else i * x := 10"

    pvars = ['x', 'y']
    prog_in = "x:= 2; y:= ??; assert (y - 1 > x); if y - 3 = 5 then x := x + ?? else x:= x + 2 ; assert (x = 5)"
    prog_out = "x:= 2; y:= 8 ; assert (y - 1 > x); if y - 3 = 5 then x := x + 3 else x:= x + 2"

    pvars = ['x', 'y']
    pre_conditions = []
    post_conditions = ['And(x == 8,y == 8)']
    prog_in = "x:= 3; y:= ??; assert (y - 1 > x); if y - 3 = 5 then x := x + ?? else x:= x + 6"
    prog_out = "x:= 3; y:= 8 ; assert (y - 1 > x); if y - 3 = 4 then x := x + 3 else x:= x + 6"

    # while loops with holes
    pvars = ['y', 'x']
    prog_in = " y := ?? ; while x < 6 do ( x := y + 4 )  ; assert x = 6"
    prog_out = " y := 1 ; while x < 6 do ( x := y + 4 )"

    pvars = ['x', 'y']
    prog_in = "x := 0 ; y := x; while x < 8 do (x := x + 2; y := y + ??); assert (y > x)"
    prog_out = "x := 0 ; y := x; while x < 8 do (x := x + 2; y := y + 3)"  # there is more than one answer

    pvars = ['x', 'y']
    prog_in = "x := 3; y:= ??; assert (y > x); while x < 10 do (x := x + ?? ; y := y + 2); assert (x > y)"
    prog_out = "x := 3; y:= 4; assert (y > x); while x < 10 do (x := x + 5 ; y := y + 2)"
