"""Tests for 'texture-replicator'"""
from pickle import NONE
from black import out
import pytest
import os
from PIL import Image
from PIL import ImageChops
from texture_replicator import replicator as texture_replicator

DUPLICATES_FOLDER = "./tests/duplicates/"


def clear_duplicates():
    """Delete all files in the duplicates test folder"""
    DUPLICATES_FOLDER_ABS = os.path.abspath(DUPLICATES_FOLDER)
    for file in os.listdir(DUPLICATES_FOLDER_ABS):
        file_path = os.path.join(DUPLICATES_FOLDER_ABS, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))    

def are_image_contents_equal(img1: Image.Image, img2: Image.Image) -> bool:
    """Compares alpha values if necessary, then converts both images to 'RGB' mode and checks for content equivilency"""
    
    # Check alpha values
    if img1.mode == img2.mode == "RGBA":
        img1_alphas = [pixel[3] for pixel in img1.getdata()]
        img2_alphas = [pixel[3] for pixel in img2.getdata()]
        equal_alphas = img1_alphas == img2_alphas
    else:
        equal_alphas = True

    # Check pixel differences
    dif = ImageChops.difference(img1.convert("RGB"), img2.convert("RGB"))
    equal_pixels = (dif.getbbox() == None)

    return equal_alphas and equal_pixels


@pytest.mark.parametrize(
    "image_path, destination_path",
    [
        ("tests/image.jpg", "tests/duplicates/"),
        ("./tests/image.jpg", "./tests/duplicates/"),
    ],
)
def test_replicate_replicatesImageInDefinedDirectory(image_path, destination_path):
    """Correctly replicates image in defined directory"""

    ### Set Up
    clear_duplicates()

    image_abs_path = os.path.abspath(image_path)
    destination_abs_path = os.path.abspath(destination_path)

    file_name = image_abs_path.split("\\")[-1]
    expected_image_path = os.path.join(destination_abs_path, file_name)

    assert os.path.isfile(expected_image_path) is False

    ### Act
    texture_replicator.replicate(image_path, destination_path)

    ### Assert
    print(expected_image_path, os.path.isfile(expected_image_path))
    assert os.path.isfile(expected_image_path) is True

    ### Tear Down
    clear_duplicates()


@pytest.mark.parametrize(
    "image_path, destination_path",
    [
        ("tests/image.jpg", "tests/duplicates/"),
        ("./tests/image.jpg", "./tests/duplicates/"),
    ],
)
def test_replicate_replicatesCorrectImageInDefinedDirectory(image_path, destination_path):
    """Correctly replicates image in defined directory"""

    ### Set Up
    clear_duplicates()

    image_abs_path = os.path.abspath(image_path)
    destination_abs_path = os.path.abspath(destination_path)

    file_name = image_abs_path.split("\\")[-1]
    expected_image_path = os.path.join(destination_abs_path, file_name)

    ### Act
    texture_replicator.replicate(image_path, destination_path)

    ### Assert
    expected = Image.open(image_abs_path)
    output = Image.open(expected_image_path)

    assert expected.size == output.size
    assert expected.format == expected.format
    assert are_image_contents_equal(expected, output)

    ### Tear Down
    clear_duplicates()


@pytest.mark.parametrize(
    "image_path, destination_path",
    [
        ("image.tiff", "tests/duplicates/"),
        ("./tests/image.png", ".tests/duplicates/"),
    ],
)
def test_replicate_image_notAFile_raiseFileNotFoundError(
    image_path, destination_path
):
    """If image_path does not point to a folder, raise File Not Found error"""

    ### Set Up
    clear_duplicates()

    ### Act, Assert
    with pytest.raises(FileNotFoundError):
        texture_replicator.replicate(image_path, destination_path)

    ### Tear down
    clear_duplicates()

    
@pytest.mark.parametrize(
    "image_path, destination_path",
    [
        ("tests/image.jpg", "tests/override.txt"),
        ("./tests/image.jpg", ".tests/override.jpg"),
    ],
)
def test_replicate_destination_notAFolder_raiseNotADirectoryError(
    image_path, destination_path
):
    """If destination_path does not point to a folder, raise Not A Directory error"""

    ### Set Up
    clear_duplicates()

    with pytest.raises(NotADirectoryError):
        texture_replicator.replicate(image_path, destination_path)
        
    ### Tear down
    clear_duplicates()


@pytest.mark.parametrize(
    "image_path, destination_path",
    [
        ("tests/image.jpg", "tests/duplicates/"),
        ("./tests/image.jpg", "./tests/duplicates/"),
    ],
)
def test_replicate_destination_folderContainsFileWithImageName_raiseFileExistsError(
    image_path, destination_path
):
    """If image file already exists in destination folder, raise a File Exists Error"""

    ### Set Up
    clear_duplicates()
    image_abs_path = os.path.abspath(image_path)
    destination_abs_path = os.path.abspath(destination_path)

    image_file_name = image_abs_path.split("\\")[-1]
    expected_image_path = os.path.join(destination_abs_path, image_file_name)

    texture_replicator.replicate(image_path, destination_path)

    with pytest.raises(FileExistsError):
        texture_replicator.replicate(image_path, destination_path)
        
    ### Tear down
    clear_duplicates()


@pytest.mark.parametrize(
    "image_path, destination_path, imageoverride_path",
    [
        ("tests/image.jpg", "tests/duplicates/","override.jpg"),
        ("./tests/image.jpg", "./tests/duplicates/", ""),
    ],
)
def test_replicate_imageoverride_createsAReplicaOfImageWithContentsOverridenByImageOverride(
    image_path, destination_path, imageoverride_path):
    """Creates a replica of the base 'image' at 'destination' but replaces the 'image' with 'imageoverride'"""
    ### Set Up
    clear_duplicates()

    image_abs_path = os.path.abspath(image_path)
    destination_abs_path = os.path.abspath(destination_path)
    imageoverride_abs_path = os.path.abspath(imageoverride_path)

    file_name = image_abs_path.split("\\")[-1]
    expected_output_path = os.path.join(destination_abs_path, file_name)

    assert os.path.isfile(expected_output_path) is False

    ### Act
    texture_replicator.replicate(image_path, destination_path)

    ### Assert

    ###### Check expected file exists
    print(expected_output_path, os.path.isfile(expected_output_path))
    assert os.path.isfile(expected_output_path) is True

    baseImage = Image.open(image_abs_path)
    overrideImage = Image.open(imageoverride_abs_path)
    outputImage = Image.open(expected_output_path)

    ###### Check format and size
    assert baseImage.format == outputImage.format
    assert baseImage.size == outputImage.size

    ###### Check contents are not equal to base image
    assert not are_image_contents_equal(baseImage, outputImage)

    ###### Check output content is equal to overrideImage
    overrideResized = overrideImage.resize(baseImage.size)
    assert are_image_contents_equal(overrideResized, outputImage)

    ### Tear Down
    clear_duplicates()

@pytest.mark.parametrize(
    "image_path, destination_path, imageoverride_path",
    [
        ("tests/image.jpg", "tests/duplicates/","override.jpg"),
        ("./tests/image.jpg", ".tests/duplicates/", ""),
    ],
)
def test_replicate_overrideimage_notAFile_raiseFileNotFoundError(
image_path, destination_path, imageoverride_path
):
    """If imageoverride_path does not point to a folder, raise File Not Found error"""

    ### Set Up
    clear_duplicates()

    ### Act, Assert
    with pytest.raises(FileNotFoundError):
        texture_replicator.replicate(image_path, destination_path, imageoverride_path)

    ### Tear down
    clear_duplicates()