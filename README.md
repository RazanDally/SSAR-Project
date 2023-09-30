# SSAR-Project
 Software Synthesis and Automated Reasoning - 236347 Final Project


The synthesizer support Features 1 & 2 as requested in the project description, It mainly operates in two modes:
1. Interactive Mode:
    In this mode the user must choose one of the following options:
    1.1. Synthesis with PBE : The user must provide a set of input-output examples and a program in While_lang and the synthesizer will try to synthesize a program that is consistent with the examples provided.
    1.2. Synthesis with Assertions : The user must provide a program in While_lang that include assertions and 
    1.3. Synthesis with both PBE and Assertions : The user must provide a set of input-output examples and a program in While_lang that include assertions.
2. Automatic Mode: 
    In this mode the user must provide a file that 


How to Use: 
The Synthesis Engine offers a user-friendly interface to assist you in synthesizing programs in the While programming language. This section provides step-by-step instructions on how to use the engine effectively.
Interactive Mode
To run the Synthesis Engine in Interactive Mode, run the following command: python main.py --I
The Synthesis Engine will then ask you to choose a mode of operation. You can choose one of the following options:
1. Synthesis with PBE:
    1.1 Select "Synthesis with PBE" by entering 1 when prompted.
    1.2 Provide the While language program you want to synthesize.
    1.3 Provide the number of examples you want to provide.
    1.4 Provide the input and output of each example based on the format provided.

2. Synthesis with Assertions:
    2.1 Select "Synthesis with Assertions" by entering 2 when prompted.
    2.2 Provide the While language program that includes asserts that you want to synthesize.

3. Synthesis with both PBE and Assertions:
    3.1 Select "Synthesis with both PBE and Assertions" by entering 3 when prompted.
    3.2 Provide the While language program that includes asserts that you want to synthesize.
    3.3 Provide the number of examples you want to provide.
    3.4 Provide the input and output of each example based on the format provided.

Automatic Mode

Here's an example of using the Synthesis Engine:

example of interactive mode:
by running this line : python main.py --I  
>> Welcome to the Synthesis Engine.
>> For more information, please refer to the README.md file.
>> For help, please run: python main.py --help
----------------------------------------
>> Starting Synthesis Engine...
Please Choose Synthesis Mode:
1. Synthesis with PBE
2. Synthesis with Assertions
3. Synthesis with both PBE and Assertions
1
Please Provide a Program in While_lang:
y:= x + ??
Please Provide a loop invariant:
1
Please Provide the number of Examples:
1
The format of the example should be:
input: ('y', 'x')
output: ('y', 'x')
if there is no input/output for a variable, please enter '_' instead.
Enter the input of example #1:
('_', 1)
Enter the output of example #1:
(2,1)
Found a valid program for all Examples: 
 y:= x + 1
----------------------------------------
>> Would you like to continue? (y/n)

example of automatic mode:
by running this line : python main.py --A --file file.txt



