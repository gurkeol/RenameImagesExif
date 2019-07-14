import argparse
import exifread
import os

MAKETRANS = str.maketrans({":": "", " ": ""})


def get_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", "--type", type=str, required=True, help="file type - e.g. jpg")
    arg_parser.add_argument("-d", "--directory", type=str, required=True, help="working directory - e.g. /home/user")
    return arg_parser.parse_args()


def process_directory(directory):
    print("process directory \"{}\"".format(directory))
    for item in os.listdir(directory):
        if os.path.isdir(item):
            process_directory(item)
        else:
            filename = os.path.join(directory, item)
            if filename.lower().endswith(args.type):
                rename_file(filename)
            else:
                print("ignore file \"{}\"".format(filename))


def get_exif_datetimeoriginal_as_str(filename):
    with open(filename, "rb") as file:
        tags = exifread.process_file(file, stop_tag="DateTimeOriginal", details=False)
    return str(tags["EXIF DateTimeOriginal"])


def get_new_filename(filename):
    creation_date = get_exif_datetimeoriginal_as_str(filename)
    new_filename = creation_date.translate(MAKETRANS) + "." + args.type
    return os.path.join(os.path.dirname(filename), new_filename)


def rename_file(old_filename):
    try:
        new_filename = get_new_filename(old_filename)
        if new_filename == old_filename:
            print("file \"{}\" already renamed".format(old_filename))
        else:
            os.rename(old_filename, new_filename)
            print("file \"{}\" renamed to \"{}\"".format(old_filename, new_filename))
    except Exception as e:
        print("error processing file \"{}\": {}".format(old_filename, e))


args = get_arguments()
process_directory(args.directory)
