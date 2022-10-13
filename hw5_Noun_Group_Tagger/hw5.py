"""
author: Xiaohan Wu
NYU ID: xw2788
email: xiaohanwu12@gmail.com
"""

import sys


BEGIN_SENT = "Begin_Sent"
END_SENT = "End_Sent"
def parse_input(filename):
    context = []
    with open(filename, 'r', encoding='utf-8') as f:
        # add begin sentence at starting
        context.append([BEGIN_SENT])
        for line in f.readlines():
            line = line.rstrip('\n')
            # print(f"'{line}'", end=', ')
            if line == '':
                # add to context to indicate an empty line
                if context[-1] != [BEGIN_SENT]:
                    context.append([END_SENT])
                # context.apend([''])
                continue
            if context[-1] == [END_SENT]:
                context.append([BEGIN_SENT])
            context.append(line.split('\t'))
        # add end sentence at the end
        if context[-1] != [END_SENT]:
            context.append([END_SENT])
    return context

def write_output(filename, context):
    with open(filename, "w", encoding='utf-8') as f:
        for line in context:
            if line == BEGIN_SENT:
                line = ''
            if line == END_SENT:
                continue
            f.write(f"{line}\n")
        f.write('\n')

def parse_context(context):
    features = []
    for line in context:
        feature = []
        if len(line) < 2:
            feature.append(line[0])
        else:
            word = line[0]
            feature.append(word)
            feature.append(f"POS={line[1]}")
            feature.append(line[-1])
        features.append('\t'.join(feature))
    return features

def generate_features(input_file, output_file):
    context = parse_input(input_file)
    features = parse_context(context)
    write_output(output_file, features)

def main():
    file_type = sys.argv[1]
    dev_files = ['WSJ_24.pos', 'test.feature']
    test_files = ['WSJ_23.pos', 'test.feature']
    test_input, test_output = eval(f"{file_type}_files")
    training_input, training_output = ['WSJ_02-21.pos-chunk', 'training.feature']

    generate_features(training_input, training_output)
    generate_features(test_input, test_output)

if __name__ == "__main__":
    main()
