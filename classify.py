from keras.utils.image_utils import img_to_array
from keras.utils import load_img
import cv2
import numpy as np
from keras.models import load_model
import pickle
import matplotlib.pyplot as plt
from keras.layers import Input
from keras.models import Model
import sklearn
import sys;

# initialize the list of class label names
CLASSES = ["normal", "benign", "malignant"]

# define the path to our output directory
OUTPUT_PATH = "./output"

# define input image spatial dimensions
IMAGE_SIZE = (128, 128)

# set the batch size
BATCH_SIZE = 16
EARLY_STOPPING_PATIENCE = 5
EPOCHS = 50

DEEP_MODEL_PATH = "deepModel.h5"
BEST_FEATURES_PATH = "features.npy"
CLASSIC_MODEL_PATH = "MLModel.pkl"
# ---------------------------------------


imagePath = sys.argv[1]
# print("image is: ",imagePath)

image = load_img(imagePath, target_size=IMAGE_SIZE)
image = img_to_array(image)

# preprocess the image by
# (1) expanding the dimensions and
# (2) subtracting the mean RGB pixel intensity from the ImageNet dataset
image = np.expand_dims(image, axis=0)
# pass the images through the network and use the outputs as
# our actual features, then reshape the features into a flattened volume
baseModel = load_model(DEEP_MODEL_PATH)  # Load The Deep Model
features = baseModel.predict(image)
features = features.reshape((1, 4 * 4 * 2048))

bestFeaturesLocations = np.load(BEST_FEATURES_PATH).astype(np.int32)  # Load The Beast (4096) Features Locations
beastFeatures = features[0][bestFeaturesLocations]
beastFeatures = beastFeatures.reshape((1, beastFeatures.shape[0]))

svcModel = pickle.load(open(CLASSIC_MODEL_PATH, "rb"))  # Load The Classic ML Model For Final Prediction
pred = svcModel.predict(beastFeatures)
print("\nclass\n", CLASSES[pred[0]].strip(), "\n")

output = cv2.imread(imagePath)
output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
output = cv2.resize(output, (IMAGE_SIZE[0] * 2, IMAGE_SIZE[0] * 2))

label = imagePath.split('/')[-1].split(' ')[0]

text1 = f"True: {label}"
text2 = f"pred: {CLASSES[pred[0]]}"

cv2.putText(output, text1, (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 50), 2)
cv2.putText(output, text2, (5, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 50, 25), 2)
plt.imshow(output)

plt.imsave("/home/leer/tst.png", output)
cv2.waitKey(1000)
