# tests for feature 1
def tests1():
    # simple examples with one hole

    num = 2
    pvars = ['x', 'y']
    examples_before = [(0, '_'), (1, '_')]
    examples_after = [(0, 1), (1, 2)]
    prog_in = "y:= x + ??"
    prog_out = "y:= x + 1"

    num = 2
    pvars = ['x', 'y']
    examples_before = [(2, '_'), (4, '_')]
    examples_after = [(2, 0), (4, 2)]
    prog_in = "y:= x - ??"
    prog_out = "y:= x - 2"

    num = 3
    pvars = ['x', 'y']
    examples_before = [(0, '_'), (2, '_'), (3, '_')]
    examples_after = [(0, 0), (2, 4), (3, 9)]
    prog_in = "y:= x * ??"
    prog_out = "y:= x * x"

    num = 3
    pvars = ['x', 'y']
    examples_before = [(1, '_'), (2, '_'), (3, '_')]
    examples_after = [(1, 4), (2, 7), (3, 10)]
    prog_in = "y:= x * ?? + 1"
    prog_out = "y:= x * 3 + 1"

    # simple examples with two hole

    num = 4
    pvars = ['x', 'y']
    examples_before = [(0, '_'), (1, '_'), (2, '_'), (3, '_')]
    examples_after = [(0, 2), (1, 6), (2, 10), (3, 14)]
    prog_in = "y:= x * ?? + ?? "
    prog_out = "y:= x * 4 + 2"

    num = 3
    pvars = ['x', 'y']
    examples_before = [(2, '_'), (3, '_'), (4, '_')]
    examples_after = [(2, 2), (3, 4), (4, 6)]
    prog_in = "y:= ?? * 2 - ??"
    prog_out = "y:= x * 2 - 2"

    num = 2
    pvars = ['x', 'y', 'z']
    examples_before = ((1, '_', '_'), (2, '_', '_'))
    examples_after = (('_', 4, '_'), ('_', 8, '_'))
    prog_in = " z := ?? ; y := x * z"
    prog_out = " z := 4 ; y := x * z"

    # if statements with holes

    num = 3
    pvars = ['x', 'y']
    examples_before = [(1, '_'), (3, '_'), (4, '_')]
    examples_after = [(1, 5), (3, 6), (4, 7)]
    prog_in = "if x >= 3 then y:= x + ?? else y:= 5"
    prog_out = "if x >= 3 then y:= x + 3 else y:= 5"

    num = 5
    pvars = ['x', 'y', 'z']
    examples_before = [(0, 1, '_'), (1, 2, '_'), (2, 3, '_'), (3, 4, '_'), (4, 5, '_')]
    examples_after = [(0, 2, 1), (1, 3, 2), (2, 3, 3), (3, 4, 4), (4, 5, 5)]
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
    pvars = ['x', 'y']
    examples_before = ((0, '_'), (1, '_'), (2, '_'))
    examples_after = ((1, 8), (1, 5), (2, 6))
    prog_in = " y := 0 ; while y < ?? do ( y := y + x + ?? ); "
    prog_out = " y := 0 ; while y < 5 do ( y := y + x + 4 );"

    num = 3
    pvars = ['x', 'y']
    examples_before = [(0, 0), (1, 2), (2, 2)]
    examples_after = [(9, 1), (14, 4), (8, 3)]
    prog_in = " while x < 8 do ( x := x + y + 4 ; y:= y + ??);"
    prog_out = " while x < 8 do ( x := x + y + 4 ; y:= y + 1);"

    num = 3
    pvars = ['x', 'y']
    examples_before = [(0, 0), (1, 2), (2, 2)]
    examples_after = [(9, 1), (14, 4), (8, 3)]
    prog_in = " while x < 8 do ( x := x + y + 4 ; y:= y + ??);"
    prog_out = " while x < 8 do ( x := x + y + 4 ; y:= y + 1);"


#######################################################################################################
# tests for feature 2

def tests2():
    pvars = ['x']
    prog_in = "x := 5 + ?? ; assert x = 7;"
    prog_out = "x := 5 + 2"

    pvars = ['x']
    prog_in = "x := 2 - ?? ; assert x > 0;"
    prog_out = "x := 2 - 1"

    pvars = ['x', 'y']
    prog_in = "y := ?? * x ; assert y = x + x + x;"
    prog_out = "y := 3 * x ;"

    pvars = ['x', 'y']
    prog_in = "y := x + ?? ; assert y = x ;"
    prog_out = "y := x + 0 ;"

    pvars = ['x', 'y', 'z']
    prog_in = "x := x + 1 ; y := x + x ; z := x * ?? + ?? ; assert z = x + y;"
    prog_out = "x := x + 1 ; y := x + x ; z := x * 3 + 1;"

    pvars = ['x', 'y']
    prog_in = "x := 8; y:= ??; assert (y > x); y = y - ??; assert (x > y)"
    prog_out = "x := 8; y:= 9; assert (y > x); y = y - 2 ; assert (x > y)"  # there is more than one answer

    pvars = ['x', 'y']
    prog_in = "x := 2 * ??; if x = 6 then y:= 4; assert y = 4 else skip"
    prog_out = "x := 2 * 3; if x = 6 then y:= 4; assert y = 4 else skip"

    pvars = ['x', 'y', 'z']
    prog_in = "x := 8 + ?? , z:= x + y;  if z = 20 then y := 8 else y := 5; assert y = 8 "
    prog_out = "x := 8 + 4 , z:= x + y;  if z = 20 then y := 8 else y := 5; assert y = 8 "

    pvars = ['x', 'y', 'z']
    prog_in = "x := 8 + ?? , if z = y + ?? then y := 20 - x else y := 5; assert y > 5 "
    prog_out = " there is more than one answer"

    pvars = ['x', 'y', 'z']
    prog_in = "y := x + ?? ; z := y + ?? ; i = x * ?? ; if z = 10 then i * x := 8 else i * x := 10 ; assert z = 10;"
    prog_out = "y := x + 3 ; z := y + 5 ; i = x * 2 ; if z = 10 then i * x := 8 else i * x := 10 ;"
    # there is more than one answer

    pvars = ['x', 'y']
    prog_in = "x:= 2; y:= ??; assert (y - 1 > x); if y - 3 = 5 then x := x + ?? else x:= x + 2 ; assert (x = 5);"
    prog_out = "x:= 2; y:= 8 ; assert (y - 1 > x); if y - 3 = 5 then x := x + 3 else x:= x + 2 ; assert (x = 5);"


    pvars = ['x', 'y']
    prog_in = " y := ?? ; while x < 6 do ( x := y + 4 )  ; assert x = 6;"
    prog_out = " y := 1 ; while x < 6 do ( x := y + 4 )"

    pvars = ['x', 'y']
    prog_in = "x := 0 ; y := x; while x < 8 do (x := x + 2; y := y + ??); assert (y > x)"
    prog_out = "x := 0 ; y := x; while x < 8 do (x := x + 2; y := y + 3);"  # there is more than one answer

    pvars = ['x', 'y']
    prog_in = "x := 3; y:= ??; assert (y > x); while x < 10 do (x := x + ?? ; y := y + 2); assert (x > y)"
    prog_out = "x := 3; y:= 4; assert (y > x); while x < 10 do (x := x + 5 ; y := y + 2); assert (x > y)"
