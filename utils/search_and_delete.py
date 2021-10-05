import ee
ee.Initialize()

# todo: add filter by metadata


def search_by_time(imgcol: ee.ImageCollection, start: str, end: str) -> ee.ImageCollection:
    start = ee.Date(start)
    end = ee.Date(end)

    imgcol = imgcol.filterDate(start, end)

    client_size = imgcol.size().getInfo()
    assert client_size > 0, f"no images found \n size : {client_size}"

    return imgcol, client_size


def delete_imgs(imgcol: ee.ImageCollection, asset_base: str, dry_run: bool = True, size: int = 1000) -> None:
    # todo see if theres a workaround to get full id from img collection
    listcol = imgcol.toList(size)
    listcolids = listcol.map(lambda i: ee.Image(i).id()).getInfo()
    asset_base = asset_base.strip('/')

    assert isinstance(dry_run, bool), "dry_run must be a bool"

    if dry_run:
        for i in range(0, len(listcolids)):
            print(f"DRY RUN DELETE {asset_base}/{listcolids[i]}")
    elif dry_run == False:
        for i in range(0, len(listcolids)):
            ee.data.deleteAsset(f"{asset_base}/{listcolids[i]}")
            print(f"DELETED {asset_base}/{listcolids[i]}")
        return 0


if __name__ == "__main__":
    raw_string = r"projects/some_project/assets/some_image_collection"

    img_collection = ee.ImageCollection(raw_string)

    start = '2009-01-06'
    end = '2021-01-01'

    filtered_col, size = search_by_time(img_collection, start, end)

    delete_imgs(filtered_col, raw_string, size=size, dry_run=True)
