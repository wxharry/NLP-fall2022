"""
author: Xiaohan Wu
NYU ID: xw2788
email: xiaohanwu12@gmail.com
"""

import re
import sys
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
sno = nltk.stem.SnowballStemmer('english')
lemma = nltk.wordnet.WordNetLemmatizer()

def parse_input(filename):
    context = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            context.append(line.split('\t'))
    return context

def write_output(filename, context):
    with open(filename, "w", encoding='utf-8') as f:
        for line in context:
            f.write(f"{line}\n")

def parse_cap(word):
    if word.islower():
        if len(word) == 4 and word[1] == '.' and word[3] == '.':
            return "lowercaseWithPeriod"
        return "lowercase"
    elif word.isupper():
        if len(word) == 4 and word[1] == '.' and word[3] == '.':
            return "uppercaseWithPeriod"
        elif len(word) == 3:
            return "ThreeUpperWord"
        return "uppercase"
    elif word == word.capitalize():
        if word[-1] == '.' and not '.' in word[:-1]:
           return "capsEndsWithPeriod"
        return "capitalization"
    else:
        return None

def parse_num(word):
    if word.isdigit():
        if len(word) == 4:
            return "fourDigitNum"
        elif len(word) == 2:
            return "twoDigitNum"
        return "isdigit"
    elif re.match(r'\d+\.\d*', word):
        return "numWithPeriod"
    elif re.match(r'\d+(,\d+)+', word):
        return "numWithComma"
    elif re.match(r'\d+.*', word):
        if '-' in word:
            return "numContainsDash"
        elif '/' in word:
            return "numContainsSlash"
        return "numAlpha"
    else:
        return None

DATES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def parse_context(context, training=False):
    features = []
    offset = 0
    for i, line in enumerate(context):
        feature = []
        previous_line = context[i-1] if i > 0 and len(context[i-1]) > 1 else None
        following_line = context[i+1] if i < len(context) - 1 and len(context[i+1]) > 1 else None
        previous2_line = context[i-2] if previous_line and i > 1 and len(context[i-2]) > 1 else None
        following2_line = context[i+2] if following_line and i < len(context) - 2 and len(context[i+2]) > 1 else None
        if len(line) < 2:
            feature.append(line[0])
            offset = 0
        else:
            word = line[0]
            feature.append(word) # add word
            feature.append(f"POS={line[1]}")
            if parse_cap(word):
                feature.append(f"{parse_cap(word)}")
            if parse_num(word):
                feature.append(f"{parse_num(word)}")
            if word == "``":
                inside = ""
                for c in context[i + 1: i + 5]:
                    inside += c[0]
                    if "''" in c[0]:
                        feature.append(f"closeIn4={parse_cap(inside)}")
                        break
            if offset == 0:
                feature.append(f"Begin_Sent")
            offset += 1
            feature.append(f"STEMMED={sno.stem(word)}")
            # feature.append(f"LEMMA={lemma.lemmatize(word)}")
            if previous_line:
                word = previous_line[0]
                feature.append(f"previous_word={word}")
                feature.append(f"previous_POS={previous_line[1]}")
                if training:
                    feature.append(f"previous_BIO={previous_line[-1]}")
                else:
                    feature.append(f"previous_BIO=@@")
            if following_line:
                word = following_line[0]
                feature.append(f"following_word={word}")
                feature.append(f"following_POS={following_line[1]}")
                if word in DATES:
                    feature.append(f"following_date")
            if previous2_line:
                word = previous2_line[0]
                feature.append(f"previous2_word={word}")
                feature.append(f"previous2_POS={previous2_line[1]}")
            if following2_line:
                word = following2_line[0]
                feature.append(f"following2_word={word}")
                feature.append(f"following2_POS={following2_line[1]}") 
            if training:
                feature.append(line[-1])
        features.append('\t'.join(feature))
    return features

def generate_features(input_file, output_file):
    context = parse_input(input_file)
    features = parse_context(context, "training" in output_file)
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
