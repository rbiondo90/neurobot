# %%
# program to train Convolution Neural Network to detect toys and not toys
# import the necessary packages
import cv2
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import models
from keras.optimizers import Adam
from keras_preprocessing.image import img_to_array
from keras import backend
import os
import numpy as np
from keras.losses import mean_absolute_error

from sklearn.model_selection import train_test_split

import defaults
import matplotlib.pyplot as plt
from recognizers.object_bounding_box_recognizer.obbr_dataset_loader import load_dataset


class ObjectBoundingBoxRecognizer:
    DEFAULT_MODEL_FILE = "item_bounding_box_recognizer.model"
    DEFAULT_EPOCHS = 200
    DEFAULT_LEARNING_RATE = 1e-3
    DEFAULT_BATCH_SIZE = 32
    DEFAULT_TEST_SIZE = 0.2

    def __init__(self, width=128, height=128, depth=3, model_file_path=DEFAULT_MODEL_FILE):
        self.model_file_path = os.path.join(defaults.AI_MODELS_DIRECTORY, model_file_path)
        if os.path.isfile(self.model_file_path):
            print("Sto caricando il modello dal file %s..." % self.model_file_path)
            self.model = models.load_model(self.model_file_path)
            self.input_shape = self.model.input_shape[1:]
        else:
            print("Sto costruendo la rete CNN...")
            self.input_shape = (height, width, depth)
            # se si usa "channels first" aggiornare la forma dell'input
            if backend.image_data_format() == "channels_first":
                self.input_shape = (depth, height, width)
            self.rebuild_model()
        self.train_history = None

    def predict(self, image):
        if type(image) == str:
            image = cv2.imread(image)
        if image.shape[0:2] != self.model.input_shape[0:2]:
            image = cv2.resize(image, self.input_shape[0:2])
        if image.dtype == 'uint8':
            image = image.astype('float32') / 255.
        return self.model.predict(image.reshape((1,) + self.input_shape))[0]

    def train(self, input_images=None, output_classification=None, learning_rate=DEFAULT_LEARNING_RATE,
              epochs=DEFAULT_EPOCHS, test_size=DEFAULT_TEST_SIZE, batch_size=DEFAULT_BATCH_SIZE):
        if input_images is None or output_classification is None:
            print("Sto caricando il dataset di default...")
            input_images, output_classification = load_dataset()
        print("Sto creando l'ottimizzatore per il training...")
        opt = Adam(lr=learning_rate, decay=learning_rate / epochs)
        print("Sto compilando il modello della rete...")

        def heavier_mae_loss(y_true, y_pred):
            return 100 * mean_absolute_error(y_true, y_pred)

        self.model.compile(loss=heavier_mae_loss, optimizer=opt, metrics=["accuracy", ])
        print("Sto dividendo il dataset in train e test set con test_size = %.2f..." % test_size)
        (train_input, test_input, train_output, test_output) = train_test_split(input_images, output_classification,
                                                                                test_size=test_size)
        print("Sto avviando l'addestramento la rete...")
        self.train_history = self.model.fit(train_input, train_output, batch_size=batch_size,
                                            validation_data=(test_input, test_output), epochs=epochs, verbose=1)
        print("Addestramento terminato.\nSto salvando il modello nel file %s..." % self.model_file_path)
        self.model.save(self.model_file_path)

    def rebuild_model(self):
        # inizializza il modello
        print("Sto costruendo il modello...")
        model = Sequential()
        # model.add(Conv2D(20, (5, 5), input_shape=self.input_shape, padding="same"))
        # model.add(Activation("relu"))
        # model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(Conv2D(40, (5, 5), padding="same"))
        # model.add(Activation("relu"))
        # model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(Flatten())
        # model.add(Dense(500))
        # model.add(Activation("relu"))
        # model.add(Dense(4))
        model.add(Conv2D(20, (11, 11), input_shape=self.input_shape, padding="same", activation="relu"))
        model.add(Conv2D(40, (3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(40, (3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(40, (3, 3), padding="same", activation="relu"))
        model.add(Flatten())
        model.add(Dense(4))
        self.model = model

    def plot_history(self):
        if self.train_history is not None:
            print("Sto preparando il plot della storia del training...")
            plt.figure()
            plt.xlabel("Epoch")
            plt.ylabel("Loss/acc")
            plt.axis([0, 200, 0, 1.05])
            plt.plot(self.train_history.epoch, np.array(self.train_history['val_loss']), label='Validation loss')
            plt.plot(self.train_history.history['val_acc'], label='Validation accuracy')
            plt.plot(np.array(self.train_history.history['loss']), label='Train loss')
            plt.plot(self.train_history.history['acc'], label='Train accuracy')
            plt.legend()
            plt.show()
        else:
            print("Non c'e' nessuna storia da plottare.")

    def evaluate(self, (test_images, test_output) = load_dataset("", False)):
        self.model.evaluate(test_images, test_output)


if __name__ == '__main__':
    net = ObjectBoundingBoxRecognizer(model_file_path='new_test')
    net.train()
