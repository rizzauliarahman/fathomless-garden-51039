import load_dataset as ld
import random
import numpy as np
import pickle


data, label_list = ld.load_dataset()

idx = random.sample([i for i in range(len(data['x_train'].tolist()))], 15)

x_val = [data['x_train'].tolist()[i] for i in idx]
y_val = [data['y_train'].tolist()[i] for i in idx]

data_val = dict()
data_val['x_val'] = np.array(x_val)
data_val['y_val'] = np.array(y_val, dtype=int)

svfile = open("data_val.dat", mode="wb")
pickle.dump(data_val, svfile)
svfile.close()
