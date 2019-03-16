import numpy as np
import os


def count_accuracy(result, target):
    right = 0

    for i in range(len(result)):

        if np.argmax(result[i]) == np.argmax(target[i]):
            right += 1

    return right / len(result)


def save_performance(classifier_name, val_acc, param=None):
    text = 'Classifier : ' + classifier_name + '. '

    if param:
        keys = list(param.keys())

        for k, v in param.items():
            if k != keys[0]:
                text += ', '

            text += k + ' = ' + repr(v)

    text += '\nValidation Accuracy : %.3f%%\n\n' % val_acc

    exists = os.path.isfile('performances.txt')
    ex_lines = []

    if exists:
        fread = open('performances.txt', mode='r')
        line = fread.readline()

        while line:
            ex_lines.append(line)
            line = fread.readline()

        fread.close()

    fobj = open('performances.txt', mode='w')

    ex_lines.append(text)

    for line in ex_lines:
        fobj.write(line)

    fobj.close()
