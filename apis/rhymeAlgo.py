vowels_set = {'aey','aa', 'ee', 'oo', 'ai', 'ae', 'au', 'a', 'e' , 'i', 'o' ,'u'}

def isContainsAnyVowel(word):
    for e in vowels_set:
        if e in word:
            return True
    return False


def clean(word):
    if word[-1] == '-':
        return word[0:-1]
    else:
        return word


def findRhyme(word, ansPrefix):
    if word == '':
        return clean(ansPrefix)

    if not isContainsAnyVowel(word = word):
        return ansPrefix + 'a'
    
    if not (word[0] in vowels_set):
        if not (word[1] in vowels_set) and word[1] != 'h':
            if not (word[2] in vowels_set) and word[2] != 'h': 
                return findRhyme(word = word[3:],ansPrefix = ansPrefix + 'a-')
            else:
                return findRhyme(word = word[2:],ansPrefix = ansPrefix + '^-')
        return findRhyme(word = word[1:],ansPrefix = ansPrefix)
    else:
        #case for last a;
        if len(word) == 1 and word[0] == 'a':
            return findRhyme(word = word[1:], ansPrefix = ansPrefix + word[0] + 'a')
        if (word[0:2] in vowels_set):
            if(word[0:3] in vowels_set):
                return findRhyme(word = word[3:], ansPrefix = ansPrefix + word[0:3] + '-')
            else:
                return findRhyme(word = word[2:], ansPrefix = ansPrefix + word[0:2] + '-')
        else:
            return findRhyme(word = word[1:], ansPrefix = ansPrefix + word[0] + '-')


def rhymeOf(word):
    word = word.lower()
    rhymePattern = findRhyme(word = word, ansPrefix = '')
    return rhymePattern


#algo
#if first is vowel:
    # if till second is vowel:
    #     if till thirod is vowel:
    #         return thirod se leker end
    #     return second se leker end
    # return first se leker end

# if first is not vower:
#   nikaal do letter and again call
# but lets try more - if next letter is 'h' uuse bhi nikal do
# if two consicutive letters are not vowel and next is vowel then add ^
# if two three letters are not vowel add an extra 'a'