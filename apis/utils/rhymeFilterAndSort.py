from apis.const.RhymeType import RhymeType

# compare suffixes
def typeOneScore(word_a, word_b):
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

# 2 * length of (largest common similar substring in both) * 100 / total len of both words's pronounciation... 
# can ignore the half letter
def typeTwoScore(word_a, word_b):
    score = 0

    word_a_array = word_a.split(sep="-")
    word_b_array = word_b.split(sep="-")

    # code for ignoring halfs

    n = len(word_a_array)
    m = len(word_b_array)
 
    # Auxillary dp[][] array
    dp = [[0 for i in range(n + 1)] for i in range(m + 1)]
 
    # Updating the dp[][] table
    # in Bottom Up approach
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
 
            # If A[i] is equal to B[i]
            # then dp[j][i] = dp[j + 1][i + 1] + 1
            if word_a_array[i] == word_b_array[j]:
                dp[j][i] = dp[j + 1][i + 1] + 1
    maxm = 0
 
    # Find maximum of all the values
    # in dp[][] array to get the
    # maximum length
    for i in dp:
        for j in i:
 
            # Update the length
            maxm = max(maxm, j)
 
    # Return the maximum length
    return maxm

def score(word_a, word_b, type = 1):
    ans = 0
    if type == RhymeType.RHYME_BY_LAST:
        ans = typeOneScore(word_a, word_b)
    if type == RhymeType.RHYME_BY_SUBSTRING:
        ans = typeTwoScore(word_a, word_b)
    return ans


# get voices which are matched with voice at least with <level> characters
def filterMatchedVoices(voices, voice, level = 2, rhyme_type = RhymeType.RHYME_BY_LAST):
    level = min(level, len(voice)/2)
    a = sorted(voices, key = lambda elem: score(word_a = voice, word_b = elem["v_title"], type = rhyme_type),reverse=True)
    a_filtered = list(filter(lambda elem: score(word_a = voice, word_b = elem["v_title"], type = rhyme_type) >= level, a))
    return a_filtered