import math
import pandas as pd

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
    #outfile = open('word_table.csv','wb')
    #outfile.write('word\tspam\tham\tP(w_i|S)\tP(w_i|H)\n')
    spam_count = 0
    ham_count = 0
    total_count = 0
    rm = ',:!?*"()\\.'
    with open('spam.csv') as infile:
        for line in infile.readlines():
            class_val, text = parse_line(line)
            if class_val == 'H':
                ham_count += 1
            else:
                spam_count += 1
            for word in text.split():
                word = filter(lambda x: not (x in rm), word).lower()
                if word not in word_table.keys():
                    word_table[word] = [0,0,0,0]
                if class_val == 'S':
                    word_table[word][0] += 1
                else:
                    word_table[word][1] += 1
    #outfile.write('spam count: ' + str(spam_count) + '\t' + 'ham count: ' + str(ham_count) + '\n')
    total_count = spam_count + ham_count
    P_S = spam_count / float(total_count)
    P_H = ham_count / float(total_count)
    for key, val in word_table.iteritems():
        #using Laplace smoothing
        p_wi_given_s = val[0] / float(spam_count)
        p_wi_given_h = val[1] / float(ham_count)
        word_table[key][2] = p_wi_given_s
        word_table[key][3] = p_wi_given_h
        #outfile.write(key + '\t' + str(val[0]) + '\t' + str(val[1]) + '\t' + str(p_wi_given_s) + '\t' + str(p_wi_given_h) + '\n')
    return word_table, spam_count, ham_count, total_count

class NaiveBayesClassifier():
    def __init__(self):
        pass

    def fit(self, prob_table, spam_count, ham_count, total_count):
        self.prob_table = prob_table
        self.spam_count = spam_count
        self.ham_count = ham_count
        self.total_count = total_count

    def predict(self, msg):
        #1.0 for spam, 0.0 for ham
        rm = ',:!?*"()\\.'
        log_sum = 0
        words = msg.split()
        for word in words:
            word = filter(lambda x: not (x in rm), word).lower()
            #Laplace Smoothing with alpha=1
            p_wi_given_s = (self.prob_table[word][0] + 1) / float(self.spam_count + len(words))
            p_wi_given_h = (self.prob_table[word][1] + 1) / float(self.ham_count + len(words))
            log_sum += math.log(p_wi_given_s/p_wi_given_h)
        P_S = self.spam_count / float(self.total_count)
        P_H = self.ham_count / float(self.ham_count)
        log_sum += math.log(P_S / P_H)
        #print log_sum
        if log_sum > 0:
            #spam
            return 1.0
        else:
            #ham
            return 0.0
    
    def score(self, X_test, y_test):
        total_count = 0
        right_count = 0
        assert len(X_test) == len(y_test)
        for i in range(len(X_test)):
            if self.predict(X_test[i]) == y_test[i]:
                right_count += 1
            total_count += 1
        print 'right count is ' + str(right_count)
        print 'total count is ' + str(total_count)
        return right_count / float(total_count)


def predict(msg):
    rm = ',:!?*"()\\.'
    for word in msg.split():
        word = filter(lambda x: not (x in rm), word).lower()

def main():
    word_prob_table, spam_count, ham_count, total_count = create_table()
    NB = NaiveBayesClassifier()
    NB.fit(word_prob_table, spam_count, ham_count, total_count)
    lines = open('spam.csv').readlines()
    class_val, text = parse_line(lines[1])
    X_test = []
    y_test = []
    for line in lines:
        class_val, text = parse_line(line)
        X_test.append(text)
        if class_val == 'S':
            y_test.append(1.0)
        else:
            y_test.append(0.0)
    print NB.predict(text)
    print NB.score(X_test, y_test)



if __name__ == "__main__":
    main()
