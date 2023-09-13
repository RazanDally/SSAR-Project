import commandlines
import time



if __name__ == "__main__":
    #args = commandlines.parse_cmd_args()
    print(">> Welcome to the Synthesis Engine.")
    time.sleep(0.8)
    print(">> For more information, please refer to the README.md file.")
    time.sleep(0.8)
    print(">> For help, please run: python main.py --help")
    time.sleep(0.8)
    print("-" * 40)
    print(">> Starting Synthesis Engine...")
    time.sleep(0.8)
    while True:
        print("Please choose a mode (interactive ('I')\ automatic ('A'):")
        time.sleep(0.8)
        mode = input()
        if mode == "I":
            #TODO: Interactive mode
            print("Interactive mode is not yet supported.")
        elif mode == "A":
            #TODO: Automatic mode
            print("Automatic mode is not yet supported.")
        else:
            print("Invalid mode.")
        break
    print(">> Exiting Synthesis Engine.")
    time.sleep(0.5)
    print("-" * 40)
    print(">> Thank you for using the Synthesis Engine.")
    time.sleep(0.5)
    print(">> Goodbye.")
