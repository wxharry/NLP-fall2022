

def read_input(filename):
    with open(filename, "r", encoding='utf-8') as f:
        context = f.read()
    return context

def read_with_lines(filename):
    context = []
    line = []
    with open(filename, 'r', encoding='utf-8') as f:
        for token in f.read().split("\n"):
            if token == '' and len(line) > 0:
                context.append(line)
                line = []
            else:
                line.append(token)
    return context

def calc_probability(freq_dict):
    total = 0
    prob_dict = {}
    for _, v in freq_dict.items():
        total += v
    for k, v in freq_dict.items():
        prob_dict[k] = v/total
    return prob_dict

def generate_unknown_word(word_count, word_freq):
    for word, count in list(word_count.items()):
        if count == 1:
            word_count.pop(word)
            word_count['UNKNOWN_WORD'] = word_count.get('UNKNOWN_WORD', 0) + 1
            for state, words in list(word_freq.items()):
                if word in words.keys():
                    word_freq[state].pop(word)
                    word_freq[state]['UNKNOWN_WORD'] = word_freq[state].get('UNKNOWN_WORD', 0) + 1
    return word_count, word_freq

def parse_input(context):
    state_word_freq = {}
    state_state_freq = {}
    word_count = {}
    state_list = set()
    pre_state = "Begin_Sent"
    for line in context.split('\n'):
        if len(line.split('\t')) < 2:
            if pre_state == "Begin_Sent":
                continue
            state = 'End_Sent'
            state_list.add(state)
            state_state_freq[pre_state] = state_state_freq.get(pre_state, {})
            state_state_freq[pre_state][state] = state_state_freq[pre_state].get(state, 0) + 1
            pre_state = 'Begin_Sent'
        else:
            [word, state] = line.split('\t')
            word = word.lower()
            word_count[word] = word_count.get(word, 0) + 1
            state_word_freq[state] = state_word_freq.get(state, {})
            state_word_freq[state][word] = state_word_freq[state].get(word, 0) + 1

            state_list.add(state)
            state_state_freq[pre_state] = state_state_freq.get(pre_state, {})
            state_state_freq[pre_state][state] = state_state_freq[pre_state].get(state, 0) + 1
            pre_state = state

    # word_count, state_word_freq = generate_unknown_word(word_count, state_word_freq)

    state_word_prob = {}
    state_state_prob = {}
    for state in state_word_freq:
        total = 0
        for freq in state_word_freq[state].values():
            total += freq
        for word in word_count:
            state_word_prob[state] = state_word_prob.get(state, {})
            if word in state_word_freq[state]:
                state_word_prob[state][word]= state_word_freq[state].get(word, 0) / total
            else:
                state_word_prob[state][word] = 0

    for pre_state in state_state_freq:
        total = 0
        for freq in state_state_freq[pre_state].values():
            total += freq
        for state in state_list:
            state_state_prob[pre_state] = state_state_prob.get(pre_state, {})
            if state in state_state_freq[pre_state]:
                state_state_prob[pre_state][state] = state_state_freq[pre_state].get(state, 0) / total
            else:
                state_state_prob[pre_state][state] = 0
    return state_word_prob, state_state_prob, list(word_count.keys())

def viterbi_HMM_POS_tagger(sentence, emissions, transitions, word_list):
    tables = [{'Begin_Sent': 1}]
    pointers = [{'Begin_Sent': None}]
    for word in sentence:
        word = word.lower()
        table = {}
        pointer = {}
        for pre_state in pointers[-1].keys():
            for state in transitions[pre_state]:
                if state == 'End_Sent':
                    continue
                probability = transitions[pre_state].get(state, 0)
                likelihood = emissions[state].get(word, 0.001)
                # if not likelihood:
                #     likelihood = emissions[state].get("UNKNOWN_WORD", 0.001)
                pre_prob = tables[-1][pre_state]
                score = pre_prob * probability * likelihood
                max_score = table.get(state, 0)
                # print(pre_state, state, word)
                # print(pre_prob, probability, likelihood)
                # print(score, max_score)
                # for k, v in pointer.items():
                #     print(f"{k}->{v}", end='\t')
                # input()
                if score > table.get(state, -1):
                    table[state] = score
                    pointer[state] = pre_state
        tables.append(table)
        pointers.append(pointer)
        # print(table)
        # for k, v in pointer.items():
        #     print(f"{k}->{v}")
        # input()
    state = 'End_Sent'
    table = {}
    pointer = {}
    for pre_state in pointers[-1].keys():    
        probability = transitions[pre_state].get(state, 0)
        pre_prob = tables[-1][pre_state]
        score = pre_prob * probability
        if score > table.get(state, -1):
            table[state] = score
            pointer[state] = pre_state
    tables.append(table)
    pointers.append(pointer)

    tagging = []
    state = 'End_Sent'
    # for line in pointers:
    #     print(line)
    # print()
    for idx in range(len(pointers)-1, 1, -1):
        pre_state = pointers[idx][state]
        tagging = [pre_state] + tagging
        state = pre_state
    return tagging


def write_output(filename, context):
    with open(filename, "w", encoding='utf-8') as f:
        for line in context:
            f.write(line + '\n')

def main():
    training_txts = ['WSJ_02-21.pos', 'WSJ_24.pos']
    context = ""
    for txt in training_txts:
        context += read_input(txt)
    emissions, transitions, word_list = parse_input(context)

    testing_txt = 'WSJ_23.words'
    context = read_with_lines(testing_txt)
    sent_tag = []
    for sentence in context:
        res = viterbi_HMM_POS_tagger(sentence, emissions, transitions, word_list)
        sent_tag.extend([sent + '\t' + tag for sent, tag in zip(sentence, res)])
        sent_tag.append('')
        # break
    output_txt = 'submission.pos'
    write_output(output_txt, sent_tag)

if __name__ == "__main__":
    main()