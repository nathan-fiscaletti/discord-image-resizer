from PIL import Image, ImageGrab
import win32clipboard

import time
import os
from io import BytesIO

from argparse import ArgumentParser

class ResizedImage:
    def __init__(self, img):
        self.__img = img
        self.__bio = None
        output = BytesIO()
        self.__img.save(output, "BMP")
        self.__original_file_size_bytes = output.getbuffer().nbytes
        output.close()
        self.__original_dimensions = self.__img.size
        self.__dimensions = (0,0)
        self.__file_size_bytes = 0
        self.__update_details()

    def resize(self, desired_file_size_bytes, increment_percentage):
        """
        Resize the image until it meets the desired maximum file size in bytes. Each pass will remove
        increment_percentage of the image.
        """
        rw = int(increment_percentage * self.__original_dimensions[0] / 100)
        rh = int(increment_percentage * self.__original_dimensions[1] / 100)
        
        # attempt at some optimization by determining how much memory was removed after a single
        # iteration and applying that same iteration the amount of time would be required to
        # get the desired size. since not all images are the same, this will almost never work
        # as intended, but it will cut down significantly on the number of passes required.
        self.__perform_downsize(rw, rh)

        removed_total_for_one_iteration = self.__original_file_size_bytes - self.__file_size_bytes
        required_amount_to_remove = self.__original_file_size_bytes - desired_file_size_bytes
        number_of_times_to_run = int((required_amount_to_remove / removed_total_for_one_iteration) - 1)

        self.__perform_downsize(rw * number_of_times_to_run, rh * number_of_times_to_run)

        # finish up with any required passes that are remaining.
        while self.__file_size_bytes > desired_file_size_bytes:
            self.__perform_downsize(rw, rh)

        return self.__img

    def needs_resize(self, desired_file_size_bytes):
        """
        Check if the image requires a resize in order to meet the desired file size.
        """
        return self.__file_size_bytes > desired_file_size_bytes

    def __perform_downsize(self, rw, rh):
        new_size = (self.__dimensions[0] - rw, self.__dimensions[1] - rh)
        self.__img = self.__img.resize(new_size)
        self.__update_details()
        pass

    def __update_details(self):
        output = BytesIO()
        self.__img.save(output, "BMP")
        self.__dimensions = self.__img.size
        self.__file_size_bytes = output.getbuffer().nbytes
        output.close()

    def get_file_size(self):
        """
        Retrieve the current file size in bytes.
        """
        return self.__file_size_bytes

    def store_in_clipboard(self):
        """
        Store the resized image in the clipboard.
        """
        output = BytesIO()
        self.__img.save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def store_in_file(self, path):
        """
        Store the resized image in a file at the specified path.
        """
        self.__img.save(path)

def cli_entry_point():
    parser = ArgumentParser()
    parser.add_argument("-s", "--size", dest="size_bytes",
                        help="the desired size in bytes for the image, default 8000000", metavar="SIZE")
    parser.add_argument("-i", "--inc", dest="increment",
                        help="the percentage of the starting dimensions to remove on each pass, default 5", metavar="INC")
    parser.add_argument("-n", "--in", dest="image",
                        help="a path to an image to process, defaults to the contents of the clipboard", metavar="PATH")
    parser.add_argument("-o", "--out", dest="output",
                        help="the output path for the processed image, defaults to the clipboard", metavar="PATH")
    args = parser.parse_args()

    im = None
    if args.image is None:
        im = ImageGrab.grabclipboard()
        if im is None:
            print("No image found in clipboard.")
            quit()
        if type(im) is list:
            args.image = im[0]
            im = Image.open(args.image)
    else:
        im = Image.open(args.image)

    if im is None:
        print("Invalid image provided or no image found.")
        quit()

    r = ResizedImage(im)

    desired_size = args.size_bytes
    if desired_size is None:
        desired_size = 8000000
    else:
        desired_size = int(desired_size)

    increment = args.increment
    if increment is None:
        increment = 5
    else:
        increment = int(increment)

    if not r.needs_resize(desired_size):
        print(f"Image did not require resize ({r.get_file_size()} bytes)")
        quit()

    print(f"Resizing image... ({r.get_file_size()} bytes)")
    start = time.time()   
    r.resize(desired_size, increment)
    duration = time.time() - start
    print(f"Resized Image!    ({r.get_file_size()} bytes) in {duration} seconds")
    print("")

    if args.output is None:
        r.store_in_clipboard()
        print(f"Clipboard Image Updated!")
    else:
        r.store_in_file(args.output)