

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

def parse_input(context):
    word_freq = {}
    state_freq = {}
    word_list = set()
    pre_state = "Begin_Sent"
    for line in context.split('\n'):
        if len(line.split('\t')) < 2:
            if pre_state == "Begin_Sent":
                continue
            state = 'End_Sent'
            state_freq[pre_state] = state_freq.get(pre_state, {})
            state_freq[pre_state][state] = state_freq[pre_state].get(state, 0) + 1
            pre_state = 'Begin_Sent'
        else:
            [word, state] = line.split('\t')
            word_list.add(word)
            word_freq[state] = word_freq.get(state, {})
            word_freq[state][word] = word_freq[state].get(word, 0) + 1

            state_freq[pre_state] = state_freq.get(pre_state, {})
            state_freq[pre_state][state] = state_freq[pre_state].get(state, 0) + 1
            pre_state = state
    word_prob = {}
    state_prob = {}
    for k, d in word_freq.items():
        word_prob[k] = calc_probability(d)
    for k, d in state_freq.items():
        state_prob[k] = calc_probability(d)
    return word_prob, state_prob, word_list

def viterbi_HMM_POS_tagger(sentence, likelihood, probability, word_list):
    n = len(sentence) + 2
    table = {k: [0 for _ in range(n)] for k in probability}
    table['End_Sent'] = [0 for _ in range(n)]
    pointer = {k: ["" for _ in range(n)] for k in probability}
    pointer['End_Sent'] = ["" for _ in range(n)]
    table['Begin_Sent'][0] = 1000
    pre_states = ["Begin_Sent"]
    for col in range(1, n):
        if col == n - 1:
            state = 'End_Sent'
            for pre_state in pre_states:
                score = table[pre_state][col-1] * probability[pre_state].get(state, 0)
                if score > table[state][col]:
                    table[state][col] = score
                    pointer[state][col] = pre_state
        else:
            word = sentence[col-1]
            states = set()
            for pre_state in pre_states:
                for state in probability[pre_state]:
                    if state == 'End_Sent':
                        continue
                    states.add(state)
                    score = table[pre_state][col-1] * probability[pre_state].get(state, 0) * likelihood[state].get(word, 0)
                    if table[pre_state][col-1] > 0 and probability[pre_state].get(state, 0)>0 and likelihood[state].get(word, 0)>0 and score == 0:
                        score = min(table[pre_state][col-1],  probability[pre_state].get(state, 0), likelihood[state].get(word, 0))
                    if score > table[state][col]:
                        table[state][col] = score
                        pointer[state][col] = pre_state
            pre_states = list(states)

    tagging = []
    cur_state = 'End_Sent'
    for idx in range(n-1, 1, -1):
        pre_state = pointer[cur_state][idx]
        tagging = [pre_state] + tagging
        cur_state = pre_state
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
    likelihood, probability, word_list = parse_input(context)

    testing_txt = 'WSJ_24.words'
    context = read_with_lines(testing_txt)
    sent_tag = []
    for sentence in context:
        res = viterbi_HMM_POS_tagger(sentence, likelihood, probability, word_list)
        sent_tag.extend([sent + '\t' + tag for sent, tag in zip(sentence, res)])
        sent_tag.append('')
    output_txt = 'submission.pos'
    write_output(output_txt, sent_tag)

if __name__ == "__main__":
    main()