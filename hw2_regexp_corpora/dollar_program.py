# Program 1 should identify dollar amounts
# Cover as many cases as possible
# including those with words like million or billion
# include numbers and decimals
# include dollar signs, the words “dollar”, “dollars”, “cent” and “cents".
# include US dollars and optionally other types of dollars
# do not include currencies that are not stated in terms of dollars and cents (e.g., ignore yen, franc, etc.)
# The program should return each match of your regular expression into an output file, one match per line.
# For example, if the program matched exactly 3 cases, than it would be a short file consisting of 3 lines like:
# $500 million
# $6.57
# 1 dollar and 7 cents

import sys
import re


def read_input(filename):
    context = ""
    with open(filename, "r", encoding='utf-8') as f:
        context = f.read()
    return context

def write_output(filename, context):
    context_with_eol = map(lambda r: r + '\n', context)
    with open(filename, "w", encoding='utf-8') as f:
        f.writelines(context_with_eol)
    print(f"\n{len(context)} lines of dollars are found\n")

def identify_dollar(context):
    pattern = regexp_or([
        f"\${regular_number()}",
        f"{regular_number()}\s{types_of_dollars()}",
        f"(?:(?:{number_words()})\s)+{types_of_dollars()}",
        "(?:half )?a dollar"
    ])
    # print(pattern)
    result = re.findall(pattern, context, re.IGNORECASE)
    return result

def regexp_or(regexps):
    regexps = [f"(?:{x})" for x in regexps]
    return '|'.join(regexps)

def regular_number():
    return "\d+(?:,\d+)*(?:.\d+)?"

def number_words():
    units = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
    ]

    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    scales = ["hundred", "thousand", "million", "billion", "trillion"]

    connects = ["and", "or"]

    return '|'.join(['|'.join(units), '|'.join(tens), '|'.join(scales), '|'.join(connects)])

def types_of_dollars():
    nations = [
        "Eastern Caribbean",
        "Australian",
        "Bahamian",
        "Barbadian",
        "Belize",
        "Bermudian",
        "Brunei",
        "Canadian",
        "Cayman Islands",
        "United States",
        "Fijian",
        "Guyanese",
        "Hong Kong",
        "Jamaican",
        "Kiribati",
        "Liberian",
        "Namibian",
        "New Zealand",
        "Singapore",
        "Solomon Islands",
        "Surinamese",
        "Spanish",
        "New Taiwan",
        "Trinidad and Tobago",
        "Tuvaluan"
    ]

    
    return f"(?:(?:{'|'.join(nations)})\s)?dollar(?:s)?"

def main():
    context = read_input(sys.argv[1])
    result = identify_dollar(context)
    write_output("dollar_output.txt", result)

if __name__ != "main":
    main()