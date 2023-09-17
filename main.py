import commandlines
import time
from src.while_lang.syntax import WhileParser


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
            print('outputs',outputs)
            ast = WhileParser()(program)
            pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip' and n != '??')
            P, Q = create_conditions(inputs, outputs, pvars)
            print('P', P)
            print('Q', Q)
            print('pvars', pvars)

            for i in range(int(num_examples)):
                p = lambda d: P[i]
                q = lambda d: Q[i]
                linv = None


                # print("Please Provide a bound:")
            # bound = input()
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
