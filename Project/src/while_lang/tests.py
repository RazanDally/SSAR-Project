# tests for feature 1
def tests1():
    # examples format is: [(x1,y1), (x2,y2),...,(xn,yn)] as xi/yi is input/output of example i

    # simple examples with one hole

    num = 4
    pvars = ['x', 'y']
    examples = [(0, 1), (1, 2), (2, 3), (3, 4)]
    inputs = [0, 1, 2, 3]
    outputs = [1, 2, 3, 4]
    prog_in = "y:= x + ??"
    prog_out = "y:= x + 1"

    num = 3
    pvars = ['x', 'y']
    examples = [(2, 0), (4, 2), (6, 4)]
    inputs = [2, 4, 6]
    outputs = [0, 2, 4]
    prog_in = "y:= x - ??"
    prog_out = "y:= x - 2"

    num = 3
    pvars = ['x', 'y']
    examples = [(0, 0), (2, 4), (3, 9)]
    inputs = [0, 2, 3]
    outputs = [0, 4, 9]
    prog_in = "y:= x * ??"
    prog_out = "y:= x * x"

    num = 3
    pvars = ['x', 'y']
    examples = [(1, 4), (2, 7), (3, 10)]
    inputs = [1, 2, 3]
    outputs = [4, 7, 10]
    prog_in = "y:= x * ?? + 1"
    prog_out = "y:= x * 3 + 1"

    # simple examples with two hole

    num = 4
    pvars = ['x', 'y']
    examples = [(0, 2), (1, 6), (2, 10), (3, 14)]
    inputs = [0, 1, 2, 3]
    outputs = [2, 6, 10, 14]
    prog_in = "y:= x * ?? + ?? "
    prog_out = "y:= x * 4 + 2"

    num = 3
    pvars = ['x', 'y']
    examples = [(2, 2), (3, 4), (4, 6)]
    inputs = [2, 3, 4]
    outputs = [2, 4, 6]
    prog_in = "y:= ?? * 2 - ??"
    prog_out = "y:= x * 2 - 2"

    num = 2
    pvars = ['x', 'y', 'z']
    examples = ((1, 4), (2, 8))
    inputs = [1, 2]
    outputs = [4, 8]
    prog_in = " z := ?? ; y := x * z"
    prog_out = " z := 4 ; y := x * z"

    # if statements with holes

    num = 3
    pvars = ['x', 'y']
    examples = [(1, 5), (3, 6), (4, 7)]
    inputs = [1, 3, 4]
    outputs = [5, 6, 7]
    prog_in = "if x >= 3 then y:= x + ?? else y:= 5"
    prog_out = "if x >= 3 then y:= x + 3 else y:= 5"

    num = 5
    pvars = ['x', 'y', 'z']
    examples = [(0, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
    inputs = [0, 1, 2, 3, 4]
    outputs = [2, 3, 3, 4, 5]
    prog_in = "z:= x + ?? ; if  z >= 3 then y:= x + 1 else y:= x + ??"
    prog_out = "z:= x + 1 ; if  z >= 3 then y:= x + 1 else y:= x + 2"

    num = 4
    pvars = ['x', 'y']
    examples = [(1, 4), (2, 4), (3, 18), (4, 24)]
    inputs = [1, 2, 3, 4]
    outputs = [4, 4, 18, 24]
    prog_in = "if x > 2 then y:= x * ?? else y:= ??"
    prog_out = "if x > 2 then y:= x * 6 else y:= 4"

    num = 4
    pvars = ['x', 'y']
    examples = [(0, 0), (1, 2), (4, 4), (5, 5)]
    inputs = [0, 1, 4, 5]
    outputs = [0, 2, 4, 5]
    prog_in = "if x >= ?? then y:= x * ?? else y:= x * ??"
    prog_out = "if x >= 2 then y:= x * 1 else y:= x * 2"


# tests for feature 2

def tests2():

    pvars = ['x']
    prog_in = "x := 5 + ?? ; assert x == 7;"
    prog_out = "x := 5 + 2"

    pvars = ['x']
    prog_in = "x := 2 - ?? ; assert x > 0;"
    prog_out = "x := 2 - 1"

    pvars = ['x', 'y']
    prog_in = "y := ?? * x ; assert y == x + x + x;"
    prog_out = "y := 3 * x ;"

    pvars = ['x', 'y']
    prog_in = "y := x + ?? ; assert y == x ;"
    prog_out = "y := x + 0 ;"

    pvars = ['x', 'y', 'z']
    input = "x := x + 1 ; y := x + x ; z := x * ?? + ?? ; assert z == x + y;"
    output = "x := x + 1 ; y := x + x ; z := x * 3 + 1;"

    pvars = ['x', 'y']
    prog_in = "x := 2 * ??; if x == 6 then y:= 4; assert y == 4 "
    prog_out = "x := 2 * 3; if x == 6 then y:= 4; assert y == 4 "

    pvars = ['x', 'y', 'z']
    prog_in = "x := 8 + ?? , if z == y + ?? then y := 20 - x else y := 5; assert y > 5 "
    prog_out = " there is more than one answer"


# tests for loops with holes

def tests3():

    # PBE
    num = 4
    pvars = ['x', 'i', 'y']
    examples = [(0, 2), (1, 1), (2, ), (3, )]
    prog_in = "i := ?? ; while x < i do ( y := x + 1 ; x:= x + 1);"
    prog_out = "i := 2 ; while x < i do ( y := x + 1 ; x:= x + 1);"


    # asserts

    pvars = ['x', 'y']
    prog_in = " y := ?? ; while x < 6 do ( x := y + 4 )  ; assert x == 6"
    prog_out = " y := 1 ; while x < 6 do ( x := y + 4 )"
