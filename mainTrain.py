import load_dataset as ld
import HelperFunction as h
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten, Dropout, BatchNormalization, Activation
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras.optimizers import Adam, SGD
import keras
import pickle
import numpy as np
import os


def main():
    classifier_name = 'Convolutional Neural Network (7 Layers)'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    data, label_list = ld.load_dataset()

    for k, v in data.items():
        print('%s : %s' % (k, v.shape))

    x_train = data['x_train']
    y_train = data['y_train']

    print('===============================================================================================')

    model = Sequential()

    model.add(Flatten(input_shape=(82, 3)))
    model.add(Dense(2048, activation='relu'))
    model.add(Dropout(0.5))
    model.add(BatchNormalization())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Dense(2, activation='sigmoid'))

    print('===============================================================================================')
    print(classifier_name)
    print('')
    print('Training')

    param = dict(lr=1e-2, clipvalue=0.5)

    adam = SGD(**param)

    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
    n = 0
    csvscores = []

    for train, val in kfold.split(x_train, y_train):
        y_train_sp = np.array(keras.utils.to_categorical(y_train, num_classes=2))

        print('Fold - %d' % (n+1))
        model.compile(optimizer=adam, loss='binary_crossentropy',
                      metrics=['accuracy'])

        model.fit(x_train[train], y_train_sp[train], epochs=40, batch_size=10, verbose=1)

        scores = model.evaluate(x_train[val], y_train_sp[val], verbose=1)
        print("Fold Accuracy : %.2f%%\n" % (scores[1] * 100))
        csvscores.append(scores[1] * 100)
        n += 1

    model.save('cnn_model.h5')
    print("Average Folds Accuracy %.2f%% (+/- %.2f%%)" % (np.mean(csvscores), np.std(csvscores)))

    # h.save_performance(classifier_name, acc, param)
    #
    # labels_file = open('labels', mode='wb')
    # pickle.dump(label_list, labels_file)


def retrain():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    model = load_model("cnn_model.h5")

    x_add, y_add = ld.load_new_data()
    x_add = np.array(x_add)
    y_add = np.array(keras.utils.to_categorical(y_add, num_classes=2))

    model.fit(x_add, y_add, epochs=20, batch_size=10, verbose=1)

    ldfile = open("data_val.dat", mode="rb")
    data_val = pickle.load(ldfile)

    x_val = data_val['x_val']
    y_val = np.array(keras.utils.to_categorical(data_val['y_val'], num_classes=2))

    scores = model.evaluate(x_val, y_val, verbose=1)
    print("Fold Accuracy : %.2f%%\n" % (scores[1] * 100))
    # model.save("cnn_model.h5")
