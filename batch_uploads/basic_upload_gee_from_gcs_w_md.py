import os

# EE cli simple upload with metadata, band names, and startdate
# 
# Assumes:
#   python3 
#   earthengine cli installed and callable
#   gsutil installed and callable
#   uploading images - not tables
#   images are located in a google storage bucket


# string of band names of imagery. Must match number of bands.
bandnames = 'red,green,blue,alpha'
# destination GEE image collection or folder
asset_path = 'projects/path/to/gee/image_collection'


# dictionary of where images are and a date. discard if this doesn't work with your format.
coldict = {
    'june_2020' : {
        # single date of all images in gcs folder
        'date' : '2020-06-01',
        # folder with some images
        'cloud' : 'gs://gcs/date_1/folder_of_images/'
    },
    'december_2020' : {
        'date' : '2020-12-01',
        'cloud' : 'gs://gcs/date_2/folder_of_images/'
    }
}

# which images to upload
choice = 'december_2020'
# start date (can be in YYYY-MM-DD srting)
datestr = coldict[choice]['date']

# gets list of files from cloud (loads ALL files)
imglist = os.popen(f'gsutil ls {coldict[choice]["cloud"]}').read().split("\n")

# print commands if True, runs commands if False
dryrun = True


for img in imglist:
    # img is full bucket path
    # e.g. gs://folder1/folder2/img.tiff

    # get image name by removing .tif
    image_name= img.split('/')[-1]

    # specific metadata/ image name
    quad_number = image_name.split('.')[0]

    # metadata is set with: property=yourMetaData
    md = f'quad_number={quad_number}'

    # name of the EE asset
    asset_name = f"{quad_number}-{datestr}"

    # skip things that dont have a quad number or are blank
    if len(quad_number) == 0 or img == "":
        continue

    if dryrun:
        print(f"earthengine upload image --asset_id={asset_path}/{asset_name} --bands {bandnames} -ts {datestr} -p {md} {img}")
    else:
        # upload image
        os.system(f"earthengine upload image --asset_id={asset_path}/{asset_name} --bands {bandnames} -ts {datestr} -p {md} {img}")
