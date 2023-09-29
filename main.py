import time
import commandlines
from src.while_lang.syntax import WhileParser
from synthesizer import Synthesizer

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
    mode_interactive = 1
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
                synth = Synthesizer()
                while invalid_program:
                    ast = WhileParser()(program)
                    if not ast:
                        print(">> Invalid program, Please Provide a Valid Program in While_lang:")
                        program = input()
                    else:
                        invalid_program = False
                print("Please Provide a loop invariant:")
                linv = input()
                print("Please Provide the number of Examples:")
                num_examples = input()
                ast = WhileParser()(program)
                pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip' and n != '??')
                print("The format of the example should be:\n"
                      f"input: {tuple(pvars)} \n"
                      f"output: {tuple(pvars)} \n"
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

                synth.synthesis_pbe(inputs, outputs, program, pvars, linv)



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
