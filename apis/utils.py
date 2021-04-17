def score(word_a, word_b):
    score = 0
    word_a_array = word_a.split(sep="-")
    word_b_array = word_b.split(sep="-")
    for index in range(len(word_a_array) + 1):
        if index == 0:
            continue
        if(len(word_b_array) >= index):
            if(word_a_array[-index] == word_b_array[-index]):
                score = score + 1
            else:
                return score
        else:
            return score
    return score

def filterMatchedVoices(voices, voice, level = 2):
    level = min(level, len(voice)/2)
    global_word = voice
    a = sorted(voices, key = lambda elem: score(word_a = voice, word_b = elem["v_title"]),reverse=True)
    a_filtered = list(filter(lambda elem: score(word_a = voice, word_b = elem["v_title"]) >= level, a))
    print(a_filtered)
    return a_filtered