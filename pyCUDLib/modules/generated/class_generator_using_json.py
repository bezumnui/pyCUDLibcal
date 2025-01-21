import copy
import os
import datetime
import time

import json


# example: python3 class_generator_using_json.py -c Booking

recurse = False
token_verified_symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"

def compare_keys_of_two_lists(list1, list2):
	for key in list1:
		if key not in list2:
			return False

	for key in list2:
		if key not in list1:
			return False

	return True



def syntax_replacer(text: str):
	return text.replace("-", "_")


def syntax_key_replacer(text: str):
	text = replace_unsafe(text, "_")
	if text == "" or text == " ":
		return "_"
	return text


def replace_python_keyword(text: str):
	keywords = ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue",
				"def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in",
				"is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
				"self"]
	if text in keywords:
		return f"{text}_"
	return text


def replace_unsafe(text: str, replace_to: str):
	if len(text) == 0:
		return "_"
	if text[0].isdigit():
		text = "_" + text
	for symbol in text:
		if symbol not in token_verified_symbols:
			text = text.replace(symbol, replace_to)

	return replace_python_keyword(text)


def generate_new_class(key, value, classes_imports, class_name=None, classes_exists=None, is_list=False):
	sub_class_name = syntax_replacer(class_name + str(key).capitalize())
	if not compare_keys_of_two_lists(list(classes_exists), list(value.keys())):
		classes_exists.update({sub_class_name: value.keys()})
		generate_class(sub_class_name, value, classes_imports, classes_exists)
	safe_key = key
	type_hint = sub_class_name
	field_value = f"{sub_class_name}(**{safe_key}) if {safe_key} else None"

	if is_list:
		type_hint = f"list[{type_hint}]"
		field_value = f"[{sub_class_name}(**key) for key in {safe_key}] if {safe_key} else []"

	return f"\t\t__self__.{safe_key}: \"{type_hint}\" = {field_value}\n"


def generate_class(class_name, data, classes_imports: list, classes_exists=None):
	if classes_exists is None:
		classes_exists = {}

	result = ""
	result += "\n" * 2
	result += f"class {class_name}:\n"
	while isinstance(data, list):
		if len(data) == 0:
			return
		data = data[0]
	keys = [syntax_key_replacer(key) for key in data.keys()]
	if len(keys) >= 1:
		result += f"\tdef __init__(__self__, {'=None, '.join(keys)}=None, **kwargs):\n"
	else:
		result += f"\tdef __init__(__self__, **kwargs):\n"
	result += f"\t\t__self__._kwargs = kwargs\n"

	for key, value in data.items():
		safe_key = syntax_key_replacer(key)
		if not isinstance(value, dict):
			if isinstance(value, list):
				if len(value) == 0:
					result += f"\t\t__self__.{safe_key}: list = {safe_key}\n"
					continue

				if isinstance(value[0], dict):
					if recurse:
						result += generate_new_class(safe_key, value[0], classes_imports, class_name, classes_exists, True)
					continue

			value_type = f": {type(value).__name__}"
			if value is None:
				value_type = ""
			result += f"\t\t__self__.{safe_key}{value_type} = {safe_key}\n"
		else:
			if recurse:
				result += generate_new_class(safe_key, value, classes_imports, class_name, classes_exists, False)

	result += "\n"
	result += f"\tdef __repr__(__self__):\n"
	result += f"\t\treturn f'{class_name}["
	for key, value in data.items():
		safe_key = syntax_key_replacer(key)
		result += f"{safe_key}: " + "{" + f"__self__.{safe_key}" + "}"
		if key != list(data.keys())[-1]:
			result += ", "
	result += "]'\n"
	classes_imports.append(result)


def write_to_the_file(filepath: str, text: str):
	with open(filepath, "w") as f:
		f.write(text)



def parce_argv():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--class', help='a class name', required=True)
	parser.add_argument('-i', '--input', help='a json file to be parsed', required=False)
	parser.add_argument('-o', '--output', help='a .py file to write the output', required=False)
	parser.add_argument('-r', '--recurse', help='use that flag to recurse', required=False)

	args = vars(parser.parse_args())
	args_class: str = args.get('class')
	args_input: str = args.get('input')
	args_output: str = args.get('output')
	args_recurse: str = args.get('recurse')

	if not args_input:
		args_input = "json_templates/" + args_class + ".json"
	if not args_output:
		args_output = pythonize_file_name(args_class) + ".py"

	if not args_output.endswith(".py"):
		args_output += ".py"

	if args_recurse:
		global recurse
		recurse = True

	return args_class, args_input, args_output

def pythonize_file_name(filename: str):
	output = ""
	for letter in filename:
		if not letter.islower():
			if len(output) == 0:
				output += letter.lower()
				continue
			output += "_" + letter.lower()
			continue
		output += letter.lower()
	return output


def json_value_normaliser(data: dict, return_data: dict = None):
	if return_data is None:
		return_data = {}
	if not isinstance(data, dict):
		return data
	for key, value in data.items():
		new_key = replace_unsafe(key, "_")
		if isinstance(value, dict):
			return_data[new_key] = json_value_normaliser(value)
		elif isinstance(value, list):
			return_data[new_key] = [json_value_normaliser(item) for item in value]
		else:
			return_data[new_key] = value
	return return_data


def main():
	class_to_be_generated, input_file_name, output_file_name = parce_argv()
	input_file = json.load(open(input_file_name))
	classes_imports = []
	generate_class(class_to_be_generated, input_file, classes_imports)

	total = (f"# generated by bezik: {datetime.datetime.now()}\n"
			 f"# github: https://github.com/bezumnui/pyCUDLibcal")

	for class_import in reversed(classes_imports):
		total += class_import
	total = syntax_replacer(total)
	write_to_the_file(output_file_name, total)
	print(f"Class {class_to_be_generated} was generated and saved to {output_file_name}")


if __name__ == '__main__':
	main()
