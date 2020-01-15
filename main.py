import os
import struct
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

def LoadMNIST(path, kind='train'):
    """ Load MNIST mnist from path """
    labels_path = os.path.join(path, '%s-labels-idx1-ubyte' % kind)
    images_path = os.path.join(path, '%s-images-idx3-ubyte' % kind)
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II', lbpath.read(8))
        labels = np.fromfile(lbpath, dtype=np.uint8)
    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII', imgpath.read(16))
        images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)
    return images, labels

def List2Numpy(li1, li2):
    return np.concatenate((np.array(li1), np.array(li2)), axis=0)

if __name__ == "__main__":
    # Get mnist data set
    trn_images, trn_labels = LoadMNIST("./mnist", kind="train")
    t10k_images, t10k_labels = LoadMNIST("./mnist", kind="t10k")
    all_images = List2Numpy(trn_images, t10k_images)
    all_labels = List2Numpy(trn_labels, t10k_labels)
    # Get test set
    test_set = pd.read_csv("./data/test.csv")
    # Training
    print("Start training!")
    clf = KNeighborsClassifier(n_neighbors=1, n_jobs=5)
    clf.fit(all_images, all_labels)
    result = clf.predict(test_set)
    # Output
    outputs = pd.DataFrame({"ImageId": range(1, 28001), "Label": result})
    outputs.to_csv("./result.csv", index=False)
    print("Done!")

