import math

"""
P(S|E) = P(E|S) * P(S) / P(E) = P(S) * Product of P(w_i|S) / P(E)
P(H|E) = P(E|H) * P(H) / P(E) = P(H) * Product of P(w_i|S) / P(E)
"""
def parse_line(line):
    class_val = ''
    text = ''
    if line[0] == 'h':
        class_val = 'H'
        text = line[4:-3].replace('"','')
    else:
        class_val = 'S'
        text = line[5:-3].replace('"','')
    return class_val, text

def create_table():
    word_table = {}
    outfile = open('word_table.csv','wb')
    outfile.write('word\tspam\tham\tP(w_i|S)\tP(w_i|H)\n')
    spam_count = 0
    ham_count = 0
    total_count = 0
    with open('spam.csv') as infile:
        for line in infile.readlines():
            class_val, text = parse_line(line)
            if class_val == 'H':
                ham_count += 1
            else:
                spam_count += 1
            for word in text.split():
                if word not in word_table.keys():
                    word_table[word] = [0,0,0,0]
                if class_val == 'S':
                    word_table[word][0] += 1
                else:
                    word_table[word][1] += 1
    outfile.write('spam count: ' + str(spam_count) + '\t' + 'ham count: ' + str(ham_count) + '\n')
    total_count = spam_count + ham_count
    P_S = spam_count / float(total_count)
    P_H = ham_count / float(total_count)
    for key, val in word_table.iteritems():
        p_wi_s = val[0] / float(total_count)
        p_wi_h = val[1] / float(total_count)
        p_wi_given_s = p_wi_s / P_S
        p_wi_given_h = p_wi_h / P_H
        word_table[key][2] = p_wi_given_s
        word_table[key][3] = p_wi_given_h
        outfile.write(key + '\t' + str(val[0]) + '\t' + str(val[1]) + '\t' + str(p_wi_given_s) + '\t' + str(p_wi_given_h) + '\n')

def main():
    table = open('word_table.csv')
    word_dict = {}



if __name__ == "__main__":
    create_table()
