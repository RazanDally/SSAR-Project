import time
import commandlines
import re
from src.while_lang.syntax import WhileParser
from synthesizer import Synthesizer


def reset_flags(args):
    args.PBE = False
    args.ASSERT = False
    args.PBE_ASSERT = False
    return args


def pbe_examples(program):
    print("Please Provide the number of Examples:")
    num_examples = input()
    ast = WhileParser()(program)
    pvars = list(n for n in ast.terminals if isinstance(n, str) and n != 'skip' and n != '??')
    ordered_set = dict.fromkeys(pvars)
    pvars = list(ordered_set.keys())
    if int(num_examples) == 0:
        print(">> No examples provided. Synthesis will be performed without PBE.")
        return [], [], pvars
    print("The format of the example should be:\n"
          f"input: {tuple(pvars)} \n"
          f"output: {tuple(pvars)} \n"
          "if there is no input/output for a variable, please enter '_' instead.")
    inputs = []
    outputs = []
    for i in range(int(num_examples)):
        print(f"Enter the input of example #{i + 1}:")
        example_in = input()
        inputs.append(eval(example_in))
        if isinstance(inputs[i], int):
            inputs[i] = [inputs[i]]
        print(f"Enter the output of example #{i + 1}:")
        example_out = input()
        outputs.append(eval(example_out))
        if isinstance(outputs[i], int):
            outputs[i] = [outputs[i]]

    return inputs, outputs, pvars


def has_assert(program):
    return "assert" in program


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
        synth = Synthesizer()
        if mode_interactive:
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
                    if has_assert(program):
                        print(">> Invalid program, Please Provide a Valid Program Without Asserts:")
                        program = input()
                        continue
                    ast = WhileParser()(program)
                    if not ast:
                        print(">> Invalid program, Please Provide a Valid Program in While_lang:")
                        program = input()
                    else:
                        invalid_program = False
                print("Please Provide a loop invariant:")
                linv = input()
                inputs, outputs, pvars = pbe_examples(program)
                synth.synthesis_pbe(program, pvars, linv, inputs, outputs)

            elif args.ASSERT:
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
                print("Please Provide a loop invariant:")
                linv = input()
                synth.synthesis_assert(program, pre, post, linv)

            elif args.PBE_ASSERT:
                print("Please Provide a Program in While_lang that includes asserts :")
                program = input()
                invalid_program = True
                while invalid_program:
                    if not has_assert(program):
                        print("Invalid Program, "
                              "Please Provide a Program that includes asserts :")
                        program = input()
                        continue
                    ast = WhileParser()(program)
                    if not ast:
                        print(">> Invalid program, Please Provide a Valid Program in While_lang:")
                        program = input()
                    else:
                        invalid_program = False
                print("Please Provide a loop invariant:")
                linv = input()
                inputs, outputs, pvars = pbe_examples(program)
                if inputs == [] and outputs == []:
                    synth.synthesis_assert(program, 'True', 'True', linv)

                synth.synthesis_pbe(program, pvars, linv, inputs, outputs)


        elif mode_automatic:
            # TODO: Automatic mode
            print("Automatic mode is not yet supported.")
            time.sleep(0.5)
        else:
            print("Invalid mode, Please run: python main.py --help")
            break

        print("-" * 40)
        print(">> Would you like to continue? (y/n)")
        continue_flag = input()
        yes_pattern = re.compile(r"^[yY][eE][sS]$|^[yY]$")
        no_pattern = re.compile(r"^[nN][oO]$|^[nN]$")
        if no_pattern.match(continue_flag):
            break
        elif yes_pattern.match(continue_flag):
            print(">> Continuing Synthesis Engine...")
            args = reset_flags(args)
            time.sleep(0.3)
            continue
        else:
            print("Invalid input, exiting Synthesis Engine.")
            break
    print(">> Exiting Synthesis Engine.")
    time.sleep(0.5)
    print("-" * 40)
    print(">> Thank you for using the Synthesis Engine.")
    time.sleep(0.5)
    print(">> Goodbye. :)")
