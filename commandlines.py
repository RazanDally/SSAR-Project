import argparse


def parse_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--I', required=False, action='store_true', help="Interactive mode")
    parser.add_argument('--A', required=False, action='store_true', help="Automatic mode")
    parser.add_argument('--PBE', required=False, action='store_true', help="Synthesis with PBE")
    parser.add_argument('--ASSERT', required=False, action='store_true', help="Synthesis with Assertions")
    parser.add_argument('--PBE_ASSERT', required=False, action='store_true', help="Synthesis with both PBE and Assertions")
    parser.add_argument('--file', required=False, type=str, help="In Automatic mode: File path to the program to be synthesized")
    if parser.parse_args().I and parser.parse_args().A:
        parser.error("Interactive and Automatic modes are mutually exclusive.")
    if parser.parse_args().A and parser.parse_args().file is None:
        parser.error("File path must be provided in Automatic mode.")
    if parser.parse_args().A and not parser.parse_args().PBE and not parser.parse_args().ASSERT and not parser.parse_args().PBE_ASSERT:
        parser.error("Synthesis mode must be provided in Automatic mode.")
    if parser.parse_args().PBE and parser.parse_args().ASSERT:
        parser.error("To use both PBE and Assertions, use the PBE_ASSERT flag.")
    args = parser.parse_args()

    return args
