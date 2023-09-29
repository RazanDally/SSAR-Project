import time
import commandlines
from src.while_lang.syntax import WhileParser
from src.while_lang.wp import verify
import re


def create_conditions(examples_before, examples_after, pvars):
    P = []
    Q = []

    for example_in, example_out in zip(examples_before, examples_after):
        p = []
        q = []

        for var, value in zip(pvars, example_in):
            if value != '_':
                p.append(f"d['{var}'] == {value}")

        for var, value in zip(pvars, example_out):
            if value != '_':
                q.append(f"d['{var}'] == {value}")

        P.append(p)
        Q.append(q)

    return P, Q


def combine_conditions(condition_list):  # TO DO : make it work with more than 2 conditions
    if not condition_list:
        return None
    elif len(condition_list) == 1:
        return condition_list[0]
    else:
        combined_condition = "And(" + ", ".join(condition_list) + ")"
        return combined_condition


def holes_to_vars(program):  # this function replaces the holes with variables
    hole_pattern = re.compile(r'\?\?')
    vars= []

    # Function to replace each match with a unique variable name
    def replace_hole(match):
        nonlocal vars
        variable_name = f'v{len(vars) + 1}'
        vars.append(variable_name)
        return variable_name

    output_program = re.sub(hole_pattern, replace_hole, program)

    return output_program, vars


def fill_holes(program, solution):
    program_lines = program.split(';')

    variable_mapping = {f'v{i + 1}': value for i, value in enumerate(solution)}

    # Function to replace variable placeholders with solution values
    def replace_variable(match):
        variable_name = match.group()
        return str(variable_mapping.get(variable_name, variable_name))

    # Iterate through each line and replace variables with solution values
    filled_program_lines = []
    for line in program_lines:
        filled_line = re.sub(r'v\d+', replace_variable, line)
        filled_program_lines.append(filled_line)

    # Join the lines to get the filled program
    filled_program = ';'.join(filled_program_lines)

    return filled_program


def remove_asserts(program):
    pass


if __name__ == "__main__":
    args = commandlines.parse_cmd_args()
    print(">> Welcome to the Synthesis Engine.")
    time.sleep(0.3)
    print(">> For more information, please refer to the README.md file.")
    time.sleep(0.3)
    print(">> For help, please run: python main.py --help")
    time.sleep(0.3)
    print("-" * 40)
    print(">> Starting Synthesis Engine...")
    time.sleep(0.3)
    mode_interactive = args.I
    mode_automatic = args.A
    while True:
        if mode_interactive:
            # TODO: Interactive mode
            if not args.PBE and not args.ASSERT and not args.PBE_ASSERT:
                print("Please Choose Synthesis Mode:")
                print("1. Synthesis with PBE")
                print("2. Synthesis with Assertions")
                print("3. Synthesis with both PBE and Assertions")
                synthesis_mode = input()
                if synthesis_mode == "1":
                    args.PBE = True
                elif synthesis_mode == "2":
                    args.ASSERT = True
                elif synthesis_mode == "3":
                    args.PBE_ASSERT = True
                else:
                    print("Invalid Synthesis Mode, Please run: python main.py --help")
            if args.PBE:
                print("Please Provide a Program in While_lang:")
                program = input()
                invalid_program = True
                while invalid_program:
                    ast = WhileParser()(program)
                    if not ast:
                        print(">> Invalid program, Please Provide a Valid Program in While_lang:")
                        program = input()
                    else:
                        invalid_program = False
                # print("Please Provide a pre-condition:")
                # pre = input()
                # print("Please Provide a post-condition:")
                # post = input()
                # print("Please Provide a loop invariant:")
                # linv = input()
                print("Please Provide the number of Examples:")
                num_examples = input()
                print("The format of the example should be:\n"
                      "input: (x1,y1...), (x2,y2...), ... , (xn,yn...) \n"
                      "output: (x1',y1'...), (x2',y2'...), ... , (xn',yn'...) \n"
                      "where (xi,yi...) are the input values of the variables in the program for example i.\n"
                      "and (xi',yi'...) are the output values of the variables for example i.\n"
                      "if there is no input/output for a variable, please enter '_' instead.")
                inputs = []
                outputs = []
                for i in range(int(num_examples)):
                    print(f"Enter the input of example #{i}:")
                    example_in = input()
                    inputs.append(eval(example_in))
                    print(f"Enter the output of example #{i}:")
                    example_out = input()
                    outputs.append(eval(example_out))

                print('inputs:', inputs)
                print('outputs', outputs)
                ast = WhileParser()(program)
                pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip' and n != '??')
                P, Q = create_conditions(inputs, outputs, pvars)
                print('P', P)
                print('Q', Q)
                print('pvars', pvars)
                holes = []
                new_program , holes = holes_to_vars(program)
                ast = WhileParser()(new_program)
                for i in range(int(num_examples)):
                    p = combine_conditions(P[i])
                    q = combine_conditions(Q[i])
                    print('p', p)
                    print('q', q)
                    p1 = lambda d: p
                    q1 = lambda d: q
                    linv = None
                    # verify(p1, ast, q1, linv=linv)
                    #

            elif args.ASSERT:
                # al so2al ana ba5od kol al asserts w ba7othn bl Q m3 kol al program bdon holes bl
                # verify wala ana ba5od assert wa7d w ba7otho bl Q wbkon al code ale abl howe al program ale bde adwr
                # 3la alholes wb3den bkml la 7d ma y5lso al asserts
                print("Please Provide a Program in While_lang that includes asserts :")
                program = input()
                invalid_program = True
                while invalid_program:
                    ast = WhileParser()(program)
                    if not ast:
                        print(">> Invalid program, Please Provide a Valid Program in While_lang:")
                        program = input()
                    else:
                        invalid_program = False
                print("Please Provide a pre-condition:")
                pre = input()
                print("Please Provide a post-condition:")
                post = input()

            elif args.PBE_ASSERT:
                pass
            print("Interactive mode is not yet supported.")
        elif mode_automatic:
            # TODO: Automatic mode
            print("Automatic mode is not yet supported.")
            time.sleep(0.5)
        else:
            print("Invalid mode, Please run: python main.py --help")
        break
    print(">> Exiting Synthesis Engine.")
    time.sleep(0.5)
    print("-" * 40)
    print(">> Thank you for using the Synthesis Engine.")
    time.sleep(0.5)
    print(">> Goodbye. :)")
