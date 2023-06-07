def make_list():
    with open('One_Piece_Spoilers.txt', 'r', encoding='utf-8') as f:
        lst = list(map(str.strip, f))
    return lst


def addition(word, lst):
    with open('One_Piece_Spoilers.txt', 'a', encoding='utf-8') as f:
        if word in lst:
            return False
        else:
            f.write(word + '\n')
            lst.append(word)
    return True
