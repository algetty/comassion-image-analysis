import argparse
from os import listdir
from os.path import isfile, splitext
import PIL
from PIL import Image
import re
import boto3
from timeit import default_timer as timer

def print_duplicate_pictures(pictures):
    total_duplicates = 0
    for (block, file_list) in pictures.items():
        if len(file_list) > 1:
            print("Possible duplicate found: ")
            print("Block: " + block)
            print("Possible files: " + str(file_list))
            print("")
            total_duplicates += 1
    print("Total duplicates: " + str(total_duplicates))

def print_picture_list(pictures):
    total_blocks = 0
    for (block, file_list) in pictures.items():
        print(file_list[0])
        total_blocks += 1

    print("Total Blocks: " + str(total_blocks))

def list_duplicate_pictures(pictures):
    duplicates = {}
    for (block, file_list) in pictures.items():
        if len(file_list) > 1:
             duplicates[block] = file_list

    return duplicates

def list_misnamed_pictures(pictures):
    pictures_to_ignore = list_duplicate_pictures(pictures).keys()
    print(pictures_to_ignore)
    for (block, file_list) in pictures.items():
        filename, file_extension = splitext(file_list[0])

        if block in pictures_to_ignore:
            print("Ignoring block " + block + " because duplicate files exist")
            continue
        try:
            int(filename)
        except:
            print(file_list[0], " is not named correctly")
            continue
    
def list_png(pictures):
    png_list = []
    for (block, file_list) in pictures.items():
        filename, file_extension = splitext(file_list[0])
        if ("png" in file_list[0].lower()):
            print(file_list[0])
            png_list.append(file_list[0])
    return png_list


def resize_picture(picture, input_folder, output_folder):
    img = Image.open(input_folder + picture)
    if int(img.size[0]) == int(img.size[1]):
        filename, file_extension = splitext(picture)
        if filename + "-sm.jpg" in listdir(output_folder):
            pass
            #print(filename, "is already resized")
        else:
            small = img.resize((250, 250), PIL.Image.ANTIALIAS)
            large = img.resize((500, 500), PIL.Image.ANTIALIAS)
            #small.save(output_folder + filename + '-sm.jpg')
            large.save(output_folder + filename + '.jpg')#'-lg.jpg')
        return (output_folder + filename + '-sm.jpg', output_folder + filename + '-lg.jpg')
    

def resize_all_images(pictures, input_folder, output_folder):
    images_to_ignore = list_misnamed_pictures(pictures)
    resized_images = []
    for block, file_list in pictures.items():
        if images_to_ignore is None or block not in images_to_ignore:
            resized_image = resize_picture(file_list[0], input_folder, output_folder)
            if resized_image is not None:
                resized_images.append(resized_image)
            else:
                print(file_list[0], "is not square")
    return resized_images 

def load_pictures(input_folder):
    print("Looking in folder " + input_folder)
    pictures = {}
    for file in listdir(input_folder):
        if "insync" in file:
            continue
        if isfile(input_folder + file):
            filename, file_extension = splitext(file)
            groups = re.search(r"(\d\B\d+)[\s]?\.{0}", file)
            if not groups:
                groups = re.search(r"^(\d)\.{1}", file)
            if groups is None:
                continue
            block_id = groups.group(0).strip()
            #print("filename:" + filename + "\next: " + file_extension)
            if block_id not in pictures:
                pictures[block_id] = []
            pictures[block_id].append(file)
    return pictures 

def upload_folder_to_aws(input_folder, output_folder):
    s3 = boto3.client('s3')
        
    print("Uploading all images in folder: ", input_folder)
    pictures = load_pictures(input_folder)
    print("Resizing images")
    valid_pictures = resize_all_images(pictures, input_folder, output_folder)
    beginning_time = timer() 
    for picture in valid_pictures:
        print(picture[0], picture[1])
        groups = re.search(r"\/(\d+)[\s]?\.{0}", picture[0])
        if not groups or groups is None:
            continue
        block_id = groups.group(0).strip()
        if "\(" in block_id:
            print("errrorrrrr")
        print(block_id)
        filename, file_extension = splitext(picture[0])
        continue
        print("s3.upload_file(" + picture[0], "block-thumbnails", "public" + str(block_id) + "-sm.jpg)")
        print("s3.upload_file(" + picture[1], "block-thumbnails", "public" + str(block_id) + "-lg.jpg)")
        s3.upload_file(picture[0], "block-thumbnails", "public" + str(block_id) + "-sm.jpg")
        s3.upload_file(picture[1], "block-thumbnails", "public" + str(block_id) + "-lg.jpg")
    ending_time = timer()
    print("Uploading pictures took: ", ending_time - beginning_time)

def main(input_folder, output_folder):
    pictures = load_pictures(input_folder)
    #print_picture_list(pictures)
    #print_duplicate_pictures(list_duplicate_pictures(pictures))
    #list_png(pictures)
    upload_folder_to_aws(input_folder, output_folder) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-idir', '--idirectory', help='directory of input images',
                        required=False, default="./")
    parser.add_argument('-odir', '--odirectory', help='directory of output images',
                        required=False, default="./")
    args = parser.parse_args()
    main(args.idirectory, args.odirectory)
