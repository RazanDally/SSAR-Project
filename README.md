# SSAR-Project
 Software Synthesis and Automated Reasoning - Final Project

--- 

## Overview:
The Synthesis Engine is a Python-based tool designed to synthesize programs based on user-input specifications, using Program By Example (PBE) and assertions. It provides an interactive and user-friendly interface allowing users to specify synthesis modes and input examples.

The synthesizer support Features 1 & 2 as requested in the project description, It operates in two modes:
### 1. Interactive Mode:
In this mode the user must choose one of the following options:

1. Synthesis with PBE.
        
2. Synthesis with Assertions. 
    
3. Synthesis with both PBE and Assertions.

### 2. Automatic Mode: 
In this mode the user must provide a file that includes the program to synthesize and the input examples. The file should be in the following format:

each test case in the following format : (the test cases are seperated by a new line)
```
 num = # of examples (Optional - depends on the mode of synthesis)
 pvars = List of variables in the program
 examples_before = input examples (based on the format provided) (Optional - depends on the mode of synthesis)
 examples_after = output examples (based on the format provided) (Optional - depends on the mode of synthesis)
 pre_conditions = pre-condition of the program (Optional - depends on the mode of synthesis)
 post_conditions = post-condition of the program (Optional - depends on the mode of synthesis)
 linv = loop invariant of the program (Optional - if not provided is assumed to be True)
 prog_in = the while program to synthesize
 prog_out = the expected output of the program (Optional)
```

(see the examples in the tests folder) in the automatic mode the engine will synthesize the program and output the result to an output file.

---

## Installation:
To install the Synthesis Engine, run the following command:

```shell
pip install -r requirements.txt
```

---

## Using Command Line Arguments

### Command Line Arguments
The Synthesis Engine supports several command-line arguments to configure its operation mode and specify additional options:

- `--I`: Run the engine in Interactive mode.
- `--A`: Run the engine in Automatic mode. (Currently not supported)
- `--PBE`: Enable Synthesis with Program By Example (PBE).
- `--ASSERT`: Enable Synthesis with Assertions.
- `--PBE_ASSERT`: Enable Synthesis with both Program By Example (PBE) and Assertions.
- `--file`: (Required in Automatic mode) Specify the file path to the program to be synthesized.

### Usage Examples:

1. **Interactive Mode with PBE:**
   ```shell
   python main.py --I --PBE
   ```
2. **Interactive Mode with Assertions:**
   ```shell
    python main.py --I --ASSERT
    ```
3. **Automatic Mode with Assertions:**
   ```shell
   python main.py --A --ASSERT --file <filepath> 
   ```
### Important Notes:
   - Both Interactive and Automatic modes are mutually exclusive; you can run the engine in either one of them but not both simultaneously.
   - In **Automatic** mode, a file path must be provided using the `--file` argument.
   - If you want to use both PBE and Assertions in Automatic mode, please use the `--PBE_ASSERT` flag.
   - In **Automatic** mode, If no mode or synthesis method is specified, the engine will return an error message prompting the user to choose the appropriate options.
   - In **Interactive** mode, if no mode of synthesis is specified, the engine will prompt the user to choose one of the available options.

### Errors & Troubleshooting:
If conflicting or incorrect arguments are provided, the engine will display an error message explaining the issue. Please refer to the error message and the usage examples above to resolve any argument-related issues.

### Help:
For more information on available command-line arguments, you can also run:

```shell
python main.py --help
```

---
## How to Use:

The Synthesis Engine offers a user-friendly interface to assist you in synthesizing programs in the While programming language. This section provides step-by-step instructions on how to use the engine effectively.

### Interactive Mode
To run the Synthesis Engine in Interactive Mode, run the following command: 

```shell
python main.py --I
``` 

The Synthesis Engine will then ask you to choose a mode of operation. You can choose one of the following options:
1. Synthesis with PBE:
   1. Select "Synthesis with PBE" by entering 1 when prompted.
   2. Provide the While language program you want to synthesize.
   3. Provide the number of examples you want to provide.
   4. Provide the input and output of each example based on the format provided.

2. Synthesis with Assertions:
   1. Select "Synthesis with Assertions" by entering 2 when prompted.
   2. Provide the While language program that includes asserts that you want to synthesize.

3. Synthesis with both PBE and Assertions:
    1. Select "Synthesis with both PBE and Assertions" by entering 3 when prompted.
    2. Provide the While language program that includes asserts that you want to synthesize.
    3. Provide the number of examples you want to provide.
    4. Provide the input and output of each example based on the format provided.

### Automatic Mode: 
To run the Synthesis Engine in Automatic Mode, run the following command: 

```shell
python main.py --A --<mode> --file <filepath>
```

example of automatic mode:
    
```shell 
python main.py --A --ASSERT --file Tests/test_assert_if.txt
```

---

## Contact:

| Name         | Email |
|--------------|-------|
| Razan Dally  | [razandally@gmail.com](mailto:razandally@gmail.com) |  
| Layan Haddad | [layanhaddad5@gmail.com](mailto:layanhaddad5@gmail.com) | 

