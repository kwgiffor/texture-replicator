"""Tests for 'texture-replicator'"""
import pytest
import os
from texture_replicator import texture_replicator

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
