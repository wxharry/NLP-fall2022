# Program 2 should identify telephone numbers
# Attempt to handle as many cases as possible: with and without area codes, different punctuation, etc.
# 212-345-1234
# 777-1000

from string import punctuation
import sys
import re

VERBOSE = False

def read_input(filename):
    context = ""
    with open(filename, "r", encoding='utf-8') as f:
        context = f.read()
    return context

def write_output(filename, context):
    context_with_eol = map(lambda r: r + '\n', context)
    with open(filename, "w", encoding='utf-8') as f:
        f.writelines(context_with_eol)
    if VERBOSE:
        print(f"\n{len(context)} lines are found\n")

def identify_telephone(context):
    punctuations = [' ', '-']
    pattern = regexp_or([
        f"{area_code_pattern()}{regexp_or(punctuations)}{telephone_pattern(punctuations)}"
    ])
    if VERBOSE:
        print(pattern)
    result = re.findall(pattern, context, re.IGNORECASE)
    return result

def regexp_or(regexps):
    regexps = [f"(?:{x})" for x in regexps]
    return f"(?:{'|'.join(regexps)})"

def telephone_pattern(punctuations):
    return "\d{3}" + regexp_or(punctuations)  + r"\d{4}(?= |\n|\.|,)"

def area_code_pattern():
    patterns = ["\(" + "\d{3}" +"\)",
                "\d{3}",
                ]
    return regexp_or(patterns)

def main():
    context = read_input(sys.argv[1])
    global VERBOSE 
    VERBOSE = (len(sys.argv) > 2 and sys.argv[2] == '-v')
    result = identify_telephone(context)
    write_output("telephone_output.txt", result)

if __name__ != "main":
    main()