import os
import json
import re
from datetime import datetime

class mosaic_manifest(object):
  def __init__(self,bucket,ee_dest, sub_dir=None):
    self.bucket = bucket
    self.ee_dest = ee_dest
    self.sub_dir = sub_dir

    self.MANIFEST = None
    self.FULL_PATH = None
    self.check_bucket()

  def get_cloud_files(self):
    if self.sub_dir is None:
      cloud_files = os.popen(f"gsutil ls {self.bucket}/*.tif").read().split("\n")[:-1]
    else:
      cloud_files = os.popen(f"gsutil ls {self.bucket}/{self.sub_dir}/*.tif").read().split("\n")[:-1]
    return cloud_files
  
  def check_json_name(self,file_name):
    search = re.search('.json$', file_name)
    if search is None:
      return f"{file_name}.json"
    else:
      return file_name

  def save(self,location,file_name=None):
    assert self.MANIFEST is not None, "Manifest has not been created. Try running mosaic_manifest(bucket,ee_dest).make()"
    
    if file_name is None:
      file_name = "manifest.json"
    else:
      file_name = self.check_json_name(file_name)

    full_path = f'{location}/{file_name}'
    self.FULL_PATH = full_path
    with open(full_path, 'w') as f:
      json.dump(self.MANIFEST, f, indent=2)

  def check_bucket(self):
      bucket_check = self.bucket.split('/')

      if len(bucket_check) > 3:

        self.sub_dir = "/".join(bucket_check[3:])
        self.bucket = "/".join(bucket_check[:3])

  def parse_time_from_folder(self):
    # todo: make this optional and add in sd/ed as cli inputs
    date_dir = self.sub_dir.split("/")[-1]
    
    search = re.search('^(\d{4}-\d{2}-\d{2})-(\d{4}-\d{2}-\d{2})$', date_dir)
    groups = search.groups()
    start_time = f"{datetime.strptime(groups[0],'%Y-%m-%d').isoformat()}Z"
    end_time = f"{datetime.strptime(groups[1],'%Y-%m-%d').isoformat()}Z"

    return start_time, end_time

  def make(self):
    # Get the list of source URIs from the gsutil output.
    cloud_files = self.get_cloud_files()
    sources_uris = [{'uris': [f]} for f in cloud_files]

    asset_name = self.ee_dest
    start_time, end_time = self.parse_time_from_folder()
    # The enclosing object for the asset.
    asset = {
      'name': asset_name,
      'tilesets': [
        {
          'id': 'dunno',
          'sources': sources_uris
        }
      ],
      'bands': [
        {
          'id': 'blue',
          'tileset_band_index':0,
          'tileset_id': 'dunno'
        },
        {
          'id':'green',
          'tileset_band_index':1,
          'tileset_id':'dunno'
        },
        {
          'id':'red',
          'tileset_band_index':2,
          'tileset_id':'dunno'
        },
        {
          'id':'nir',
          'tileset_band_index':3,
          'tileset_id':'dunno'
        },
        {
          'id':'alpha',
          'tileset_band_index':4,
          'tileset_id':'dunno'
        },
      ],
      'start_time':start_time,
      'end_time':end_time
    }
    self.MANIFEST = asset
    return asset

  def upload(self, manifest=None):

    if manifest is None:
      manifest = self.FULL_PATH

    os.system(f"earthengine upload image --manifest {manifest}")


if __name__ == "__main__":
  import argparse
  import textwrap

  # Initiate the parser
  desc = """CLI for making and uploading Planet 4-Band quad imagery stored in a Google Storage Bucket
  
      e.x. making a mosaic and using the current path to save the manifest.json
           mosaic_manifest.py gs://bucket/subdir projects/ee/imagecollection/newImageName .
  """
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent(desc))
  parser.add_argument("bucket",help='-The URI where images are stored (e.g. gs://myBucket or gs://myBucket/subDir )')
  parser.add_argument("ee_dst",help='-The earthengine location to save the mosaic')
  parser.add_argument("manifest_dst",help='-The location to locally save the manifest.json')
  args = parser.parse_args()


  m = mosaic_manifest(args.bucket, args.ee_dst)
  m.make()
  m.save(args.manifest_dst)
  m.upload()
