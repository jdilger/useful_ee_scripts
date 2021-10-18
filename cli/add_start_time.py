import subprocess


# example adding or updating a system time start using a single date
# note: this will work on a single image as well, but you should use the regular EE CLI rather than looping over it :)
folder_or_imgcol = r'projects/sig-ee/Philippines/forest_forest_30p_tcc'
assets = subprocess.run(['earthengine','ls',folder_or_imgcol],capture_output=True, text=True).stdout.splitlines()

date = '2018-01-01'
dry_run = True

for i in assets:
    command = ['earthengine', 'asset', 'set','--time_start',date]
    if dry_run:
        print('DRY RUN '," ".join(command))
    else:
        subprocess.run(command)

