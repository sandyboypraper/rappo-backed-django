vowels_set = {'aey','aa', 'ee', 'oo', 'ai', 'ae', 'au', 'a', 'e' , 'i', 'o' ,'u'}

# make equality b/w 'oo' and 'u'

example_word = ["Rakhta",
"Sabka",
"Mereko",
"sarkaar",
"savaal",
"mukadma",
"desh",
"drohi",
"thokenge",
"patrakaar",
"sthan",
"Antaraashtriya",
"antyeshti",
"vilambit",
"keemat",
"deemak",
"arthvyavastha",
"taansen",
"namcheen",
"garje",
"kranti",
"bandobast",
"paudhe",
"maarpeet",
"narbhaksh",
"karkash",
"rakshas",
"shanichar",
"khushiya",
"manticore"
]

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


def findPhonetics(word, ansPrefix):

    # if word is '' then we remove last '-' if it presents
    if word == '':
        return clean(ansPrefix)

    # if word does'nt contains any vowels from vowels_set then we just add 'a'
    # in place of word and return it
    if not isContainsAnyVowel(word = word):
        return ansPrefix + 'a'
    

    if not (word[0] in vowels_set):
        if not (word[1] in vowels_set) and word[1] != 'h':
            if not (word[2] in vowels_set) and word[2] != 'h': 
                return findPhonetics(word = word[3:],ansPrefix = ansPrefix + 'a-')
            else:
                return findPhonetics(word = word[2:],ansPrefix = ansPrefix + '^-')
        return findPhonetics(word = word[1:],ansPrefix = ansPrefix)
    else:
        #case for last a;
        if len(word) == 1 and word[0] == 'a':
            return findPhonetics(word = word[1:], ansPrefix = ansPrefix + word[0] + 'a')
        if (word[0:2] in vowels_set):
            if(word[0:3] in vowels_set):
                return findPhonetics(word = word[3:], ansPrefix = ansPrefix + word[0:3] + '-')
            else:
                return findPhonetics(word = word[2:], ansPrefix = ansPrefix + word[0:2] + '-')
        else:
            return findPhonetics(word = word[1:], ansPrefix = ansPrefix + word[0] + '-')


def phoneticsOf(word):
    word = word.lower()
    rhymePattern = findPhonetics(word = word, ansPrefix = '')
    return rhymePattern

def phoneticsOf_array(words):
    return map(lambda word: phoneticsOf(word), words)

def test():
    for word in example_word:
        print(word, " -> ", phoneticsOf(word))


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