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


def pbe_examples_I(program, PBE=True):
    print("Please Provide the number of Examples:")
    num_examples = input()
    ast = WhileParser()(program)
    pvars = list(n for n in ast.terminals if isinstance(n, str) and n != 'skip' and n != '??')
    ordered_set = dict.fromkeys(pvars)
    pvars = list(ordered_set.keys())
    if int(num_examples) == 0:
        if PBE:
            while int(num_examples) <= 0:
                print(">> Error: number of examples must be greater than 0.")
                print("Please Provide the number of Examples:")
                num_examples = input()
        else:
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


def pbe_examples_A(program, section):
    num_examples = section['num']
    ast = WhileParser()(program)
    pvars = list(n for n in ast.terminals if isinstance(n, str) and n != 'skip' and n != '??')
    ordered_set = dict.fromkeys(pvars)
    pvars = list(ordered_set.keys())
    if int(num_examples) == 0:
        return [], [], pvars

    # Regular expression to match tuples
    pattern = re.compile(r'\([^)]*\)')

    # Extracting tuples as strings and storing in a list
    examples_before = [match.group() for match in pattern.finditer(section['examples_before'])]
    examples_after = [match.group() for match in pattern.finditer(section['examples_after'])]
    inputs = []
    outputs = []
    for i in range(int(num_examples)):
        example_in = examples_before[i]
        inputs.append(eval(example_in))
        if isinstance(inputs[i], int):
            inputs[i] = [inputs[i]]
        example_out = examples_after[i]
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
                inputs, outputs, pvars = pbe_examples_I(program)
                solved = synth.synthesis_pbe(program, pvars, linv, inputs, outputs)
                if not solved:
                    print(">> Synthesis Failed.")
                else:
                    print(">> Synthesis Successful.")
                    print(">> Synthesized Program:")
                    print(synth.synthesized_program)
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
                solved = synth.synthesis_assert(program, pre, post, linv)
                if not solved:
                    print(">> Synthesis Failed.")
                else:
                    print(">> Synthesis Successful.")
                    print(">> Synthesized Program:")
                    print(synth.synthesized_program)

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
                inputs, outputs, pvars = pbe_examples_I(program, PBE=False)
                if inputs == [] and outputs == []:
                    solved = synth.synthesis_assert(program, 'True', 'True', linv)
                else:
                    solved = synth.synthesis_pbe(program, pvars, linv, inputs, outputs)
                if not solved:
                    print(">> Synthesis Failed.")
                else:
                    print(">> Synthesis Successful.")
                    print(">> Synthesized Program:")
                    print(synth.synthesized_program)

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

        elif mode_automatic:
            filename = args.file
            sections = []
            section = {}

            try:
                with open(filename, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if not line:  # if line is empty, it means a section has ended
                            if section:  # if there is any data in the section, append it to sections
                                sections.append(section)
                                section = {}  # reset the section
                            continue

                        # Extract key-value pair from the line
                        key, value = map(str.strip, line.split('=', 1))

                        section[key] = value

                    if section:  # for the last section in the file
                        sections.append(section)

            except FileNotFoundError:
                print(f"The file {filename} does not exist.")
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")

            try:
                filename = filename.split('.')[0]
                with open(filename + "_out.txt", 'w') as file:
                    file.write("Synthesis Results:\n")
                    for i, section in enumerate(sections, 1):
                        file.write(f"Test {i}:")
                        file.write("\n")
                        program = section['prog_in']
                        invalid_program = True
                        while invalid_program:
                            if has_assert(program):
                                if args.PBE:
                                    file.write(f"PBE Error: Invalid Program, {program} has assertion.\n")
                                    break
                            elif args.PBE_ASSERT:
                                file.write(f"Assert Error: Invalid Program, {program} must have assertion.\n")
                                break
                            ast = WhileParser()(program)
                            if not ast:
                                file.write(
                                    f"Error: Invalid Program, {program} is not a valid program in While_lang.\n")
                                break
                            else:
                                invalid_program = False
                        if invalid_program:
                            continue
                        if 'linv' in section.keys():
                            linv = section['linv'][2:-2]
                        else:
                            linv = 'True'
                        if args.PBE or args.PBE_ASSERT:
                            inputs, outputs, pvars = pbe_examples_A(program, section)
                        if 'pre_conditions' in section.keys():
                            pre = section['pre_conditions'][2:-2]
                        else:
                            pre = 'True'
                        if 'post_conditions' in section.keys():
                            post = section['post_conditions'][2:-2]
                        else:
                            post = 'True'
                        synth_done = False
                        if args.ASSERT:
                            synth_done = synth.synthesis_assert(program, pre, post, linv)
                        else:
                            if inputs == [] and outputs == []:
                                if args.PBE:
                                    file.write(f"PBE Error: No examples provided.\n")
                                else:
                                    synth_done = synth.synthesis_assert(program, 'True', 'True', linv)
                            else:
                                synth_done = synth.synthesis_pbe(program, pvars, linv, inputs, outputs)

                        file.write(f"Program: {program}\n")
                        file.write(f"Program Expected Output: {section['prog_out']}\n")
                        if synth_done:
                            file.write(f"Synthesized Program: {synth.synthesized_program}\n")
                        else:
                            file.write(f"Synthesized Program: No Valid Program Found.\n")
                        file.write("\n")

            except Exception as e:
                print(f"An error occurred while writing to the file: {e}")

            time.sleep(0.5)
            break
        else:
            print("Invalid mode, Please run: python main.py --help")
            break
    print(">> Exiting Synthesis Engine.")
    time.sleep(0.5)
    print("-" * 40)
    print(">> Thank you for using the Synthesis Engine.")
    time.sleep(0.5)
    print(">> Goodbye. :)")
