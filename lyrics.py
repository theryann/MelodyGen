
def syllable_count(word: str) -> int:
    word = word.lower()
    vovels = 'aeiou'
    syl_count: int = 0

    # adding syllables
    for letter in word:
        if letter in vovels +'y':
            syl_count += 1

    if "'" in word and 'l' in word:
        syl_count += 1

    # removing syllables
    if word.startswith('y'):
        syl_count -= 1

    for v1 in vovels:
        for v2 in vovels:
            if v1+v2 in word:
                syl_count -= 1

    return syl_count
