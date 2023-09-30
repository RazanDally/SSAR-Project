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
        self.filled_holes = 0
        self.synthesized_program = ""
        self.program = ""
        self.holes = None
        self.P = None
        self.Q = None
        self.linv = ""
        self.filled_program = ""

    def synthesis_pbe(self, program, pvars, linv, inputs, outputs):
        self.P, self.Q = self.create_conditions(inputs, outputs, pvars)
        self.linv = self.str_exp_to_z3(linv, pvars)
        self.program, self.holes = self.holes_to_vars(program)
        ast = WhileParser()(self.program)
        self.synthesized_program = ""
        if ast:

            pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip')
            env = mk_env(pvars)
            possible_programs = []
            # Iterate over all inputs to find a possible filled_program
            for i in range(len(inputs)):
                solver = Solver()  # Create a new Solver instance for each input
                formula = And(self.P[i](env), aux_verify(ast, self.Q[i], self.linv, env)(env))
                solver.add(formula)
                if solver.check() == unsat:
                    continue  # Continue with the next input
                # Get the model and fill the holes in the program
                sol = solver.model()
                filled_program = self.fill_holes(self.program, sol)
                ast_f = WhileParser()(filled_program)

                # Verify the filled program for all P and Q
                is_valid_for_all = all(verify(self.P[j], ast_f, self.Q[j], linv=self.linv) for j in range(len(inputs)))

                if self.filled_holes != len(self.holes):
                    possible_programs.append(filled_program)

                if is_valid_for_all:
                    self.set_synthesized_program(filled_program)
                    return True  # Return True if a valid filled program is found

            if len(possible_programs) > 0:
                curr = possible_programs[0]
                for prog in possible_programs:
                    if curr != prog:
                        curr = self.merge_programs(curr, prog)
                        ast_f = WhileParser()(curr)
                        is_valid_for_all = all(
                            verify(self.P[j], ast_f, self.Q[j], linv=self.linv) for j in range(len(inputs)))
                        if is_valid_for_all:
                            self.set_synthesized_program(curr)
                            return True

        return False  # Return False if no valid filled program is found for all inputs

    def merge_programs(self, prog1, prog2):
        prog1 = prog1.split(";")
        prog2 = prog2.split(";")
        var_pattern = re.compile(r'v\d+')

        for i in range(len(prog1)):
            matches1 = list(var_pattern.finditer(prog1[i]))
            matches2 = list(var_pattern.finditer(prog2[i]))
            if matches2 == 0:
                if prog1[i] != prog2[i]:
                    prog1[i] = prog2[i]
            if matches1 != 0:
                for m in matches1:
                    index = prog1[i].index(m.group())
                    if prog2[i][index] != prog1[i][index]:
                        prog1[i] = prog1[i].replace(m.group(), prog2[i][index])
        return ";".join(prog1)

    def synthesis_assert(self, program, pre, post, linv):
        self.program, self.holes = self.holes_to_vars(program)
        ast = WhileParser()(self.program)
        if ast:
            pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip')
            self.P = self.str_exp_to_z3(pre, pvars)
            self.Q = self.str_exp_to_z3(post, pvars)
            self.linv = self.str_exp_to_z3(linv, pvars)
            env = mk_env(pvars)
            solver = Solver()
            formula = And(self.P(env), aux_verify(ast, self.Q, self.linv, env)(env))
            solver.add(formula)
            if solver.check() == unsat:
                return False
            else:
                sol = solver.model()
                filled_program = self.fill_holes(self.program, sol)
                ast_f = WhileParser()(filled_program)
                is_valid = verify(self.P, ast_f, self.Q, linv=self.linv)
                if is_valid:
                    self.set_synthesized_program(filled_program)
                    return True
                else:
                    return False

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

    def str_exp_to_z3(self, s, pvars):
        if s == 'True':
            return lambda _: True
        elif s == 'False':
            return lambda _: False
        env_eval = mk_env(pvars)
        env_eval.update(
            {'And': And, 'Or': Or, 'Not': Not, 'Implies': Implies, 'ForAll': ForAll, 'True': True, 'False': False})
        expr = eval(s, None, env_eval)
        return lambda env: expr

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

    def vars_to_holes(self, program_with_vars):
        # Regular expression pattern to match variables of the form 'v' followed by one or more digits
        var_pattern = re.compile(r'\bv\d+\b')

        # Replace each match with '??'
        program_with_holes = re.sub(var_pattern, '??', program_with_vars)
        return program_with_holes

    def fill_holes(self, program, model):
        program_lines = program.split(';')

        # Extract variable assignments from the model
        variable_mapping = {}
        for d in model.decls():
            if d.name() in self.holes:
                self.filled_holes += 1
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

    def set_synthesized_program(self, filled_program):
        self.synthesized_program = filled_program


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
