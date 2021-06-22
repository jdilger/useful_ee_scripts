import os

# EE cli simple upload with startdate
# 
# Assumes:
#   python3 
#   earthengine cli installed and callable
#   gsutil installed and callable
#   uploading images - not tables
#   images are located in a google storage bucket

# to upload images to bucket use a similar command as below
# gsutil -m cp source destination 


# destination GEE image collection or folder
asset_path = 'projects/path/to/gee/image_collection'


# dictionary of where images are and a date. discard if this doesn't work with your format.
coldict = {
    'year_2020' : {
        # single date of all images
        'date' : '2020-01-01',
        # folder with some images
        'cloud' : 'gs://gcs/date_1/folder_of_images/'
    },

}

# which images to upload
choice = 'year_2020'
# start date (can be in YYYY-MM-DD srting)
datestr = coldict[choice]['date']

# gets list of files from cloud (loads ALL files)
imglist = os.popen(f'gsutil ls {coldict[choice]["cloud"]}').read().split("\n")

# print commands if True, runs commands if False
dryrun = True


for img in imglist:
    # img is full bucket path
    # e.g. gs://folder1/folder2/img.tiff

    # get image name by parsing the full location
    image_name= img.split('/')[-1]
    # remove the .tif from the image name
    image_name = image_name.split('.tif')[0]

    # name of the EE asset
    asset_name = f"{image_name}-{datestr}"

    # skip things that dont match our format or are blank
    if len(image_name) == 0 or img == "":
        continue

    if dryrun:
        print(f"earthengine upload image --asset_id={asset_path}/{asset_name}  -ts {datestr}  {img}")
    else:
        # upload image
        os.system(f"earthengine upload image --asset_id={asset_path}/{asset_name} -ts {datestr} {img}")
