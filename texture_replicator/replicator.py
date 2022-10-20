from genericpath import isfile
import os
import shutil
from PIL import Image


def replicate(image: str, destination: str, imageoverride:str = None):
    """
    Copy an image to a designated destination folder
    Args:
        image (str) : path of the image to copy
        destination (str) : directory where the image should be copied
    Returns:
        None
    """
    # Verify image points to a file
    image_abs_path = os.path.abspath(image)
    if os.path.isfile(image_abs_path) != True:
        raise FileNotFoundError("image must point to a valid file: " + image_abs_path)

    # Verify destination points to a folder
    destination_abs_path = os.path.abspath(destination)
    if os.path.isdir(destination_abs_path) != True:
        raise NotADirectoryError("destination must point to a valid directory folder: " + destination_abs_path)

    # If imageOverride is not none, verify override is an Image
    if imageoverride != None:
        imgoverride_abs_path = os.path.abspath(imageoverride)
        if os.path.isfile(imgoverride_abs_path) != True:
            raise FileNotFoundError("imageoverride must point to a valid file: " + imgoverride_abs_path)

    # Verify image does not exist in destination folder
    image_file_name = image.split("/")[-1]
    new_image_path = os.path.join(destination_abs_path, image_file_name)
    if os.path.exists(new_image_path):
        raise FileExistsError(
            "File with name "
            + image_file_name
            + " already exists in "
            + destination
        ) 
    
    # Verify image is an Image
    try:
        img = Image.open(image_abs_path)
    except Exception as e:
        raise ValueError(image + "is not a valid image: " + image_abs_path)

    # Verify override is an image
    if imageoverride != None:
        try:
            img_override = Image.open(imgoverride_abs_path)
        except Exception as e:
            raise ValueError(imageoverride + "is not a valid image: " + imgoverride_abs_path)
    

    print("Copying ", image_abs_path, " to ", destination_abs_path)

    # Copy Image to new path
    if (imageoverride == None):
        output = img
        output.save(new_image_path)
        print(image, "has been successfully replicated in", destination)
    else:
        output = img_override
        output = output.resize(img.size)
        output.save(new_image_path)
        print(image, "has been successfully replicated in", destination, "and has been overriden by", imageoverride)

    # Close open images
    img.close()
    output.close()