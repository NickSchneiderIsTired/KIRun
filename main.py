import numpy as np
import numpy.random
from sklearn import linear_model
import sklearn as sk
import opensmile
from utils import create_dict, read_chunk


model = linear_model.LinearRegression()
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.Functionals,
    num_channels=2
)

train_dict = create_dict('data/train/')

X = np.empty((0, 176), dtype="float32")
y = np.empty(shape=0, dtype="int32")


# Create X and y from dataset
for audio, annotations in train_dict.items():
    for annotation in annotations:
        print(audio)
        start = int(np.ceil(annotation.running_start))
        end = int(np.floor(annotation.running_stop)) - 5
        for i in range(8):
            if start >= end:
                break
            x_values = read_chunk(smile, audio, start, 5)
            X = np.append(X, x_values, axis=0)
            y = np.append(y, annotation.wealth)
            start = start + 5

X, y = sk.utils.shuffle(X, y)
print("fitting")
model.fit(X, y)
print("fitted")

# VALIDATE TRAINED MODEL
val_dict = create_dict('data/val/')
val_X = np.empty((0, 176), dtype="float32")

# Create X to validate with
for audio, annotations in val_dict.items():
    for annotation in annotations:
        x_values = read_chunk(smile, audio, int(np.ceil(annotation.running_start)), 5)
        val_X = np.append(val_X, x_values, axis=0)

print(model.predict(val_X))

