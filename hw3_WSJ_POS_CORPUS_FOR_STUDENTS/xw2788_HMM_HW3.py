

def read_input(filename):
    with open(filename, "r", encoding='utf-8') as f:
        context = f.read()
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
    pre_state = "Begin_Sent"
    for line in context.split('\n'):
        if len(line.split('\t')) < 2:
            state = 'End_Sent'
            state_freq[pre_state] = state_freq.get(pre_state, {})
            state_freq[pre_state][state] = state_freq[pre_state].get(state, 0) + 1
            pre_state = 'Begin_Sent'
        else:
            [word, state] = line.split('\t')
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
    return word_prob, state_prob


def main():
    context = read_input('WSJ_24.pos')
    likelihood, probability = parse_input(context)
    

if __name__ == "__main__":
    main()