from src.while_lang.syntax import WhileParser
from src.while_lang.wp import *
import operator
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat
import re

OP = {'+': operator.add, '-': operator.sub,
      '*': operator.mul, '/': operator.floordiv,
      '!=': operator.ne, '>': operator.gt, '<': operator.lt,
      '<=': operator.le, '>=': operator.ge, '=': operator.eq}


class Synthesizer:
    def __init__(self):
        self.program = ""
        self.holes = None
        self.P = None
        self.Q = None
        self.linv = ""
        self.filled_program = ""

    def synthesis_pbe(self, inputs, outputs, program, pvars, linv):
        # TODO implement this function
        self.P, self.Q = self.create_conditions(inputs, outputs, pvars)
        self.linv = lambda d: True
        self.program, self.holes = self.holes_to_vars(program)
        ast = WhileParser()(self.program)
        if ast:

            pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip')
            env = mk_env(pvars)

            # Iterate over all inputs to find a possible filled_program
            for i in range(len(inputs)):
                solver = Solver()  # Create a new Solver instance for each input
                formula = Implies(self.P[i](env), aux_verify(ast, self.Q[i], linv, env)(env))
                solver.add(formula)

                if solver.check() == unsat:
                    print('unable to synthesize program for input', i)
                    continue  # Continue with the next input

                # Get the model and fill the holes in the program
                sol = solver.model()
                filled_program = self.fill_holes(self.program, sol)
                ast_f = WhileParser()(filled_program)

                # Verify the filled program for all P and Q
                is_valid_for_all = all(verify(self.P[j], ast_f, self.Q[j], linv=self.linv) for j in range(len(inputs)))

                if is_valid_for_all:
                    print('found a valid filled program:', filled_program)
                    return True  # Return True if a valid filled program is found
                else:
                    print(f'filled program {filled_program} is not valid for all P and Q')

        print('No valid filled program found for all inputs')
        return False  # Return False if no valid filled program is found for all inputs

    def synthesis_assert(self, program, pre, post, linv):
        # TODO implement this function
        # TODO fix the P and Q and the printings
        self.P = lambda _: True #pre
        self.Q = lambda _: True #post
        self.linv = lambda _: True #linv
        self.program, self.holes = self.holes_to_vars(program)
        ast = WhileParser()(self.program)
        if ast:
            pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip')
            env = mk_env(pvars)
            solver = Solver()
            formula = Implies(self.P(env), aux_verify(ast, self.Q, linv, env)(env))
            solver.add(formula)
            if solver.check() == unsat:
                print('unable to synthesize program')
                return False
            else:
                sol = solver.model()
                filled_program = self.fill_holes(self.program, sol)
                ast_f = WhileParser()(filled_program)
                is_valid = verify(self.P, ast_f, self.Q, linv=self.linv)
                if is_valid:
                    print('found a valid filled program:', filled_program)
                    return True
                else:
                    print(f'filled program {filled_program} is not valid')
                    return False

    def synthesis_pbe_assert(program, pre, post, linv, bound, examples):
        # TODO implement this function do we need this function?
        pass

    def create_conditions(self, examples_before, examples_after, pvars):
        self.P = []
        self.Q = []

        for example_in, example_out in zip(examples_before, examples_after):
            p = lambda d: True
            q = lambda d: True

            for var, value in zip(pvars, example_in):
                if value != '_':
                    prev_p = p  # store the previous lambda
                    p = lambda d, p=prev_p, var=var, value=value: And(p(d), d[var] == value)

            for var, value in zip(pvars, example_out):
                if value != '_':
                    prev_q = q  # store the previous lambda
                    q = lambda d, q=prev_q, var=var, value=value: And(q(d), d[var] == value)

            self.P.append(p)
            self.Q.append(q)

        return self.P, self.Q

    def combine_conditions(self, condition_list):  # this function combines the conditions into one condition
        if not condition_list:
            return None
        elif len(condition_list) == 1:
            return condition_list[0]
        else:
            combined_condition = condition_list[0]
            for i in range(len(condition_list) - 1):
                combined_condition = And(combined_condition, condition_list[i + 1])
            return combined_condition

    def holes_to_vars(self, program):  # this function replaces the holes with variables
        hole_pattern = re.compile(r'\?\?')
        vars = []

        # Function to replace each match with a unique variable name
        def replace_hole(match):
            nonlocal vars
            variable_name = f'v{len(vars) + 1}'
            vars.append(variable_name)
            return variable_name

        output_program = re.sub(hole_pattern, replace_hole, program)
        self.program = output_program
        self.holes = vars
        return output_program, vars

    def fill_holes(self, program, model):
        program_lines = program.split(';')

        # Extract variable assignments from the model
        variable_mapping = {}
        for d in model.decls():
            variable_mapping[d.name()] = model[d].as_long()  # Convert ExprRef to Python int

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

if __name__ == '__main__':
    # # example program
    pvars = ['y', 'x', '??']
    program = "y := x + ??"
    ast = WhileParser()(program)
    synth = Synthesizer()
    if ast:
        synth.synthesis_pbe([], [], program, pvars, None)
    else:
        print(">> Invalid program.")
