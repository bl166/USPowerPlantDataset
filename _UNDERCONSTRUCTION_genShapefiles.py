import rasterio
from rasterio.features import shapes
mask = None
with rasterio.drivers():
    with rasterio.open('./binary/bilabels_300.png') as src:
        image = src.read(1) # first band
        results = (
            {'properties': {'raster_val': v}, 'geometry': s} for i, (s, v) in
            enumerate(
                shapes(image, mask=mask, transform=src.affine)
            )
        )
poly = list(results)[0]
print(poly)
