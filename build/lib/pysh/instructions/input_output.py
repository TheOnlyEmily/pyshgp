# -*- coding: utf-8 -*-
"""
Created on July 24, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import pysh_state
from .. import instruction as instr
from .. import utils as u
from .. import pysh_globals as g
from . import registered_instructions as ri



def handle_input_instruction(instruction, state):
	'''
	Allows Push to handle inN instructions, e.g. in2, using things from the input
	stack. We can tell whether a particular inN instruction is valid if N-1
	values are on the input stack.
	'''
	input_depth = int(instruction.name.split("input")[1]) - 1
	input_value = state.stacks['_input'].stack_ref(input_depth)
	pysh_type = u.recognize_pysh_type(input_value)

	if pysh_type == '_instruction':
		state.stacks['_exec'].push_item(input_value)
	elif pysh_type == '_list':
		state.stacks['_exec'].push_item(input_value)
	else:
		state.stacks[pysh_type].push_item(input_value)

def printer(pysh_type):
	'''
	Returns a function that takes a state and prints the top item of the
	appropriate stack of the state.
	'''
	def prnt(state):
		if len(state.stacks[pysh_type]) < 1:
			return

		top_thing = state.stacks[pysh_type].stack_ref(0)
		top_thing_str = str(top_thing)
		if len(str(state.stacks["_output"].stack_ref(0)) + top_thing_str) > g.max_string_length:
			return
		state.stacks["_output"][0] = str(state.stacks["_output"].stack_ref(0)) + top_thing_str
	instruction = instr.Pysh_Instruction('print' + pysh_type,
										prnt,
										stack_types = ['_print', pysh_type])
	if pysh_type == '_exec':
		instruction.parentheses = 1
	return instruction
ri.register_instruction(printer('_exec'))
#<instr_open>
#<instr_name>print_exec
#<instr_desc>Prints the top item of the exec stack to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_integer'))
#<instr_open>
#<instr_name>print_integer
#<instr_desc>Prints the top integer to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_float'))
#<instr_open>
#<instr_name>print_float
#<instr_desc>Prints the top float to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_code'))
#<instr_open>
#<instr_name>print_code
#<instr_desc>Prints the top item on the code code stack to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_boolean'))
#<instr_open>
#<instr_name>print_boolean
#<instr_desc>Prints the top boolean to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_string'))
#<instr_open>
#<instr_name>print_string
#<instr_desc>Prints the top string to the string on the output stack.
#<instr_close>

def print_newline(state):
	if len(str(state.stacks["_output"].stack_ref(0)) + "\n") > g.max_string_length:
		return state
	state.stacks["_output"][0] = str(state.stacks["_output"].stack_ref(0)) + "\n"

print_newline_instruction = instr.Pysh_Instruction('print_newline',
												   print_newline,
												   stack_types = ['_print'])
ri.register_instruction(print_newline_instruction)
#<instr_open>
#<instr_name>print_newline
#<instr_desc>Prints a newline to the string on the output stack.
#<instr_close>