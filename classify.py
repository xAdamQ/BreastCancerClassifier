from keras.utils.image_utils import img_to_array
from keras.utils import load_img
import numpy as np
from keras.models import load_model
import pickle
import sys

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

DEEP_MODEL_PATH = "./models/deepModel.h5"
BEST_FEATURES_PATH = "./models/features.npy"
CLASSIC_MODEL_PATH = "./models/MLModel.pkl"
# ---------------------------------------

imagePath = sys.argv[1]

image = load_img(imagePath, target_size=IMAGE_SIZE)  # Must Be RGB
image = img_to_array(image)
# preprocess the image by expanding the dimensions
image = np.expand_dims(image, axis=0)
# pass the images through the network and use the outputs as
# our actual features, then reshape the features into a flattened volume
baseModel = load_model(DEEP_MODEL_PATH)  # Load The Deep Model
features = baseModel.predict(image)
features = features.reshape((1, 4 * 4 * 2048))  # New Dimension (1, 32000)
# Extracting The Best (4096) Features From The Image
bestFeaturesLocations = np.load(BEST_FEATURES_PATH).astype(np.int32)  # Load The Beast (4096) Features Locations
beastFeatures = features[0][bestFeaturesLocations]  # Dimension (4096,)
beastFeatures = beastFeatures.reshape((1, beastFeatures.shape[0]))  # New Dimension (1, 4096)
# Final Prediction Using Classic (SVC) ML Model
svcModel = pickle.load(open(CLASSIC_MODEL_PATH, "rb"))  # Load The Classic ML Model For Final Prediction
pred = svcModel.predict(beastFeatures)
print("\nclass\n", CLASSES[pred[0]].strip(), "\n")
