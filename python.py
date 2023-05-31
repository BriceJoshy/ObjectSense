#  this file shows how to read and show an image from an url in the csv file

import cv2 as cv
import numpy as np
import requests
import csv

"""Using the deeplabv3+ model silhoutteX.h5"""

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import cv2 as cv

#  extract all the input images
from glob import glob

# progress bar
from tqdm import tqdm

# ml library
import tensorflow as tf
from tensorflow import keras

# Code within a with statement will be able to access custom objects by name
from keras.utils import CustomObjectScope
from metrics import dice_loss, dice_coeff, iou

""" Defining Global Parameters """
# height
H = 512
# width
W = 512


#  i.e is a blank directory
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    np.random.seed(42)
    tf.random.set_seed(42)

    create_directory("removed_background_images")

    """Loading the model S_X"""

    with CustomObjectScope(
        {"iou": iou, "dice_coef": dice_coeff, "dice_loss": dice_loss}
    ):
        model = tf.keras.models.load_model("silhouetteX.h5")

    """Summary of the model"""
    # from the summary we can see that the imput is a 512,512,3 channel image
    # and the output is a 512,512,1 channel (binary mask)
    # model.summary()

    #  creating a empty list for storing the rows of the single column of the csv file
    image_from_csv_list = []
    image_name_saved = []
    #  setting the indexx for the image name so as to prevent the images from crashing while 'imshow' because of the same name
    with open("images.csv", mode="r") as file:
        csvfile = csv.reader(file)
        # that returns the reader object that iterates throughout the lines in the specified CSV document.
        # for every line adding the column[0] as the list row for the empty list created above
        for column in csvfile:
            image_from_csv_list.append(column[0])
        print(image_from_csv_list)
        index = 0
        for i in range(0, len(image_from_csv_list)):
            url = image_from_csv_list[i]
            # using the .get()  from requests to get the data as bytes and raw i.e without any change
            response = requests.get(url, stream=True).raw
            # .read reads the data into a bytstream and the datatype is changes to uint8
            image = np.asarray(bytearray(response.read()), dtype="uint8")
            #  reading the image as it is without any change
            image = cv.imdecode(image, cv.IMREAD_COLOR)
            filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpedned = cv.filter2D(image, -1, filter)
            cv.imshow("sharp image", sharpedned)

            """Reading the images"""
            # always convert image to the 3 channel BGR color image.
            # print(image.shape)
            #  now the image is an numpy array
            # i.e why the _ is given as there are more parameters in shape
            # save for later
            height, width, _ = sharpedned.shape
            resized_image = cv.resize(sharpedned, (W, H))
            # print(resized_image.shape)
            # Normalization of the resized_image
            # now the range of the pixel value is btw 0 and 1 as is divided by the max pixel value
            resized_image = resized_image / 255.0
            # print(resized_image.shape)
            """Explanation for the type conversion"""
            #  https://stackoverflow.com/questions/59986353/why-do-i-have-to-convert-uint8-into-float32
            resized_image = resized_image.astype(np.float32)
            # print(resized_image.shape)
            # adding th expanded dimension to the axis
            resized_image = np.expand_dims(resized_image, axis=0)
            #  (1,512,512,3) this is because this is a single image and we give the numpy array into the model by batches
            #  so we are giving it as one batch
            # print(resized_image.shape)

            """Making a Prediction"""
            # because we have given one image as an input
            # ouput would also be one mask not more than that will be predicted by the model
            predicted_mask = model.predict(resized_image)[0]
            # index 0 so the shape be came as below
            # (1, 512, 512, 1) as it is an binary mask
            # print(predicted_image.shape)
            #  this is the mask
            #  we resize the prdicted mask is resized to 512,512
            #  we make sure that the the size of the prediction mask is same as the origianl image
            predicted_mask = cv.resize(predicted_mask, (width, height))
            print(predicted_mask.shape)
            #  now we are going to expand its dimentions for the last axis
            predicted_mask = np.expand_dims(predicted_mask, axis=-1)
            print(predicted_mask.shape)

            # creaing the threshold
            predicted_mask = predicted_mask > 0.5
            # predicted maks contains range of 0 and 1
            # multiplying it by 255 to get the range of 0 to 255
            """saving the predicted mask"""
            # cv.imwrite(f"remove_background/{image_name}.png", predicted_mask * 255)

            # Need two kinds of masks
            """Photo mask"""
            # photo_mask is the main object
            photo_mask = predicted_mask
            background_mask = np.abs(1 - predicted_mask)
            # print(background_mask.shape)
            # cv.imwrite(f"remove_background/{image_name}.png", background_mask * 255)
            # reversed the color
            #  photot mask contain the mask for the main object and the background mask contain the mask for the background
            """why not * 255"""
            # we cant see the difference btw the 0 and 1 but we can see the diff os the 0 and 255
            # here by multiplying - because the background ,ask or the photo mask is for the array contain the values 0 or 1
            # pixel values multiplied by zero became 0 and the others are multiplied by  so the object remain the same in the result

            # cv.imwrite(f"remove_background/{image_name}.png", image * photo_mask)
            # seperating the background removing the object
            # cv.imwrite(f"remove_background/{image_name}.png", image * background_mask)

            """Custom background (color)"""

            masked_image = image * photo_mask
            #  to have a custom color there is need of 3 color channels
            #  checking the channel from shape
            # print(masked_image.shape)

            # stacking the 3 values of top of each other in the last axis
            background_mask = np.concatenate(
                [background_mask, background_mask, background_mask], axis=-1
            )
            background_mask = background_mask * [0, 0, 255]
            final_image = masked_image + background_mask

            image_name_saved.append(f"image_{index}.png")
            print(image_name_saved)
            cv.imwrite(
                f"removed_background_images/{image_name_saved[index]}", final_image
            )

            index += 1
            ###############

        # row = image_name_saved

        with open("final_outout.csv", mode="w", newline="") as file:
            writter = csv.writer(file)
            for rows in image_name_saved:
                writter.writerow([rows])
