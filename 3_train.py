import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras


# Loading Features & Labels
f_df = pd.read_csv("features.csv")
l_df = pd.read_csv("labels.csv")

# Converting Features & Labels into Numpy Array
x = np.array(f_df)
y = np.array(l_df).flatten()

# Spliting Training & Testing data
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.15)

# Normalized Data
x_train = x_train / 255         
x_test = x_test / 255           



# Creating Brain
model = keras.Sequential([
    keras.layers.Dense(100, input_shape=(4096,), activation='relu'),
    keras.layers.Dense(50, activation='relu'),
    keras.layers.Dense(24, activation='softmax')
])

# Compiling Model
model.compile(
    optimizer = 'adam',
    loss = 'sparse_categorical_crossentropy',
    metrics = 'accuracy'
)

# Saving Model
history = model.fit(x_train, y_train, epochs=5)
model.save('model/model-1.h5', history)


print("Done...")

