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
    filelist = []
    if isinstance(filename, list):
        filelist = filename
    else:
        filelist.append(filename)
    for file in filelist:
        with open(file, 'r', encoding='utf-8') as f:
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

def parse_context(context, training=False):
    features = []
    for i, line in enumerate(context):
        feature = []
        previous_line = context[i-1] if i > 0 and len(context[i-1]) > 1 else None
        following_line = context[i+1] if i < len(context) - 1 and len(context[i+1]) > 1 else None
        previous2_line = context[i-2] if previous_line and i > 1 and len(context[i-2]) > 1 else None
        following2_line = context[i+2] if following_line and i < len(context) - 2 and len(context[i+2]) > 1 else None
        previous3_line = context[i-3] if previous2_line and previous_line and i > 2 and len(context[i-3]) > 1 else None
        following3_line = context[i+3] if following2_line and following_line and i < len(context) - 3 and len(context[i+3]) > 1 else None
        previous4_line = context[i-4] if previous3_line and previous2_line and previous_line and i > 3 and len(context[i-4]) > 1 else None
        following4_line = context[i+4] if following3_line and following2_line and following_line and i < len(context) - 4 and len(context[i+4]) > 1 else None
        if len(line) < 2:
            feature.append(line[0])
        else:
            word = line[0]
            feature.append(word) # add word
            feature.append(f"POS={line[1]}")
            feature.append(f"BIO={line[2]}")
            feature.append(f"TokNum={line[3]}")
            # feature.append(f"SentNum={line[4]}")
            if parse_cap(word):
                feature.append(f"{parse_cap(word)}")
            feature.append(f"STEMMED={sno.stem(word)}")
            feature.append(f"LEMMA={lemma.lemmatize(word)}")
            if int(line[3]) > 0:
                feature.append(f"Previous_tag=@@")
            if previous_line:
                word = previous_line[0]
                feature.append(f"previous_word={word}")
                feature.append(f"previous_POS={previous_line[1]}")
                feature.append(f"previous_BIO={previous_line[2]}")
                feature.append(f"previous_STEM={sno.stem(word)}")
                # feature.append(f"previous_LEMMA={lemma.lemmatize(word)}")
            if following_line:
                word = following_line[0]
                feature.append(f"following_word={word}")
                feature.append(f"following_POS={following_line[1]}")
                feature.append(f"following_BIO={following_line[2]}")
                feature.append(f"following_STEM={sno.stem(word)}")
                # feature.append(f"following_LEMMA={lemma.lemmatize(word)}")
            if previous2_line:
                word = previous2_line[0]
                feature.append(f"previous2_word={word}")
                feature.append(f"previous2_POS={previous2_line[1]}")
                feature.append(f"previous2_BIO={previous2_line[2]}")
                feature.append(f"previous2_STEM={sno.stem(word)}")
                # feature.append(f"previous2_LEMMA={lemma.lemmatize(word)}")
            if following2_line:
                word = following2_line[0]
                feature.append(f"following2_word={word}")
                feature.append(f"following2_POS={following2_line[1]}")
                feature.append(f"following2_BIO={following2_line[2]}")
                feature.append(f"following2_STEM={sno.stem(word)}")
                # feature.append(f"following2_LEMMA={lemma.lemmatize(word)}")
            if previous3_line:
                word = previous3_line[0]
                feature.append(f"previous3_word={word}")
                feature.append(f"previous3_POS={previous3_line[1]}")
                feature.append(f"previous3_BIO={previous3_line[2]}")
                feature.append(f"previous3_STEM={sno.stem(word)}")
                # feature.append(f"previous3_LEMMA={lemma.lemmatize(word)}")
            if following3_line:
                word = following3_line[0]
                feature.append(f"following3_word={word}")
                feature.append(f"following3_POS={following3_line[1]}")
                feature.append(f"following3_BIO={following3_line[2]}")
                feature.append(f"following3_STEM={sno.stem(word)}")
                # feature.append(f"following3_LEMMA={lemma.lemmatize(word)}")
            if previous4_line:
                word = previous4_line[0]
                # feature.append(f"previous3_word={word}")
                feature.append(f"previous3_POS={previous4_line[1]}")
                feature.append(f"previous3_BIO={previous4_line[2]}")
                # feature.append(f"previous3_STEM={sno.stem(word)}")
                # feature.append(f"previous3_LEMMA={lemma.lemmatize(word)}")
            if following4_line:
                word = following4_line[0]
                # feature.append(f"following3_word={word}")
                feature.append(f"following4_POS={following3_line[1]}")
                feature.append(f"following4_BIO={following3_line[2]}")
                # feature.append(f"following3_STEM={sno.stem(word)}")
                # feature.append(f"following3_LEMMA={lemma.lemmatize(word)}")
            if training:
                if len(line) > 5:
                    feature.append(line[-1])
                else:
                    feature.append('')
        features.append('\t'.join(feature))
    return features

def generate_features(input_files, output_file, train=False):
    context = parse_input(input_files)
    features = parse_context(context, train)
    write_output(output_file, features)

def main():
    if len(sys.argv) > 1:
        file_type = sys.argv[1]
    if len(sys.argv) > 2:
        task_type = sys.argv[2]
    percent_task_dev = ['%_nombank.clean.train', '%_nombank.clean.dev']
    percent_task_test = [['%_nombank.clean.train', '%_nombank.clean.dev'], '%_nombank.clean.test']
    partitive_task_dev = ['partitive_group_nombank.clean.train', 'partitive_group_nombank.clean.dev']
    partitive_task_test = [['partitive_group_nombank.clean.train', 'partitive_group_nombank.clean.dev'], 'partitive_group_nombank.clean.test']

    data_path = 'data'
    files = eval(f"{task_type}_task_{file_type}")
    files = list(map(lambda x: f"{data_path}/{x}" if isinstance(x, str) else x, files))
    training_input, test_input = files
    if isinstance(training_input, list):
        training_input = list(map(lambda x: f"{data_path}/{x}" if isinstance(x, str) else x, training_input))
    training_output = 'training.feature'
    generate_features(training_input, training_output, True)
    generate_features(test_input, "test.feature")

if __name__ == "__main__":
    main()
