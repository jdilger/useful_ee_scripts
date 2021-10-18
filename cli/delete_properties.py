import subprocess

# example removing unwanted properties from images in a image collection or folder
# note: this will work on a single image as well, but you should use the regular EE CLI rather than looping over it :)
folder_or_imgcol = r'projects/sig-ee/Philippines/forest_forest_30p_tcc'
assets = subprocess.run(['earthengine','ls',folder_or_imgcol],capture_output=True, text=True).stdout.splitlines()

prop_to_remove_a = 'lol'
prop_to_remove_b = 'accidental_prop'

dry_run = True
for i in assets:
    asset_name = i.split("/")[-1]
    command = ['earthengine', 'asset', 'set','--property ',f'{prop_to_remove_a}=null','--property',f'{prop_to_remove_b}=null']
    if dry_run:
        print('DRY RUN '," ".join(command))
    else:
        subprocess.run(command)
