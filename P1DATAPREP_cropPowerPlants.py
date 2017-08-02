'''
cropPowerPlants.py

This script works on the Google Earth Engine (Python API). It reads geographic coordinates of US power plants
in 2014 egrid document, and gets the recanglular region (.005 degrees on each span) centered at it. It primarily
works on NAIP and Landsat8 data, but will take whatever imagery that is correctly imported.

Authors: Boning Li
Email: boning.li@duke.edu
Developed for Duke Data+ 2017: Electricity Access
Jul 30, 2017
'''
<<<<<<< HEAD
=======

>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
# Before everything: source activate py27
# Import the Earth Engine Python Package
import ee
import numpy as np
from xlrd import open_workbook

ee.Initialize()
# Function to download powerplant pictures
# takes 2~4 arguments: id_start, id_end, order, collection
<<<<<<< HEAD
def download_ppt_pic(id_start,id_end,*args, **kwargs):
	# set default options
	collection = kwargs.get('collection', 'naip')
	order = kwargs.get('order', 'normal')
	# open the document with coordinates of US power plants
	egrid = open_workbook("egrid2014_data_v2_PLNT14.xlsx").sheet_by_index(0) # if your data is on sheet 1

	# DEFINE YOUR IMAGE COLLECTION HERE
	#************** NAIP imagery **************
	if collection=='naip':
		collection_naip = ee.ImageCollection('USDA/NAIP/DOQQ').filter(ee.Filter.date('2012-01-01', '2014-12-31'))
		# reduce the image stack to one image
		image = collection_naip.mosaic()
		# resolution = 1m
		res = 1

	#********** Pan-sharpened Landsat **********
	elif collection=='ls8':
		collection_ls8 = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').filterDate('2014-01-01', '2014-12-30')
		# reduce the image stack to every pixel's median value
		img_red = collection_ls8.reduce(ee.Reducer.median())
		# pan sharpening by hsv & panchromatic band
		rgb = img_red.select('B4_median', 'B3_median', 'B2_median')
		gray = img_red.select('B8_median')
		huesat = rgb.rgbToHsv().select('hue', 'saturation')
		image = ee.Image.cat(huesat, gray).hsvToRgb()
		# resolution = 15m
		res = 15

	else:
		print('I couldn\'t find the '+collection+' collection. Please choose between \'naip\'(default) and \'ls8\'.')
		return

	# the span to crop
	deg = .0075
	# if the order is defined as 'reverse'
	if order == 'descend':
		rg = list(reversed(range(id_start, id_end)))
	elif order == 'ascend':
		rg = range(id_start, id_end)
	else:
		print('I couldn\'t understand the download order '+order+'. Please choose between \'ascend\'(default) and \'descend\'.')
		return

	# Each ID defines a unique power plant in egrid document
	for pid_int in rg:
		# find which one it is
		row = egrid.col_values(0).index(pid_int)
		try:
			# set the region to crop
			lat_center = float(egrid.cell_value(row,4))
			long_center = float(egrid.cell_value(row,5))
			scale = np.cos(lat_center/180*np.pi) # because 1 longt ~ 1 lat / cos(lat)
			geometry = ee.Geometry.Rectangle([
				long_center-deg/scale, # longtitude lower bound
				lat_center-deg, # latitude lower bound
				long_center+deg/scale, # longtitude upper bound
				lat_center+deg  # latitude upper bound
			]);
			roi=image.clip(geometry)

			# configurations for export
			config_d = {
				'scale': res,					 # resolution
				'skipEmptyTiles': True,		 	 # action flag
				'maxPixels':1E13,				 # max: 1E13
				'folder': 'PowerPlants_'+collection  # destination
			}

			# define and start the task
			task = ee.batch.Export.image(roi, str(pid_int), config=config_d)
			task.start()

			print(str(pid_int)+':'+collection)

		except ValueError:
			print(-1)


if __name__ == '__main__':
	id_start,id_end = (300,500) # include id_start, exclude id_end
	download_ppt_pic(id_start,id_end,order='descend',collection='ls8')
=======


def download_ppt_pic(id_start, id_end, *args, **kwargs):
    # set default options
    collection = kwargs.get('collection', 'naip')
    order = kwargs.get('order', 'normal')
    # open the document with coordinates of US power plants
    egrid = open_workbook("egrid2014_data_v2_PLNT14.xlsx").sheet_by_index(
        0)  # if your data is on sheet 1

    # DEFINE YOUR IMAGE COLLECTION HERE
    #************** NAIP imagery **************
    if collection == 'naip':
        collection_naip = ee.ImageCollection(
            'USDA/NAIP/DOQQ').filter(ee.Filter.date('2012-01-01', '2014-12-31'))
        # reduce the image stack to one image
        image = collection_naip.mosaic()
        # resolution = 1m
        res = 1

    #********** Pan-sharpened Landsat **********
    elif collection == 'ls8':
        collection_ls8 = ee.ImageCollection(
            'LANDSAT/LC8_L1T_TOA').filterDate('2014-01-01', '2014-12-30')
        # reduce the image stack to every pixel's median value
        img_red = collection_ls8.reduce(ee.Reducer.median())
        # pan sharpening by hsv & panchromatic band
        rgb = img_red.select('B4_median', 'B3_median', 'B2_median')
        gray = img_red.select('B8_median')
        huesat = rgb.rgbToHsv().select('hue', 'saturation')
        image = ee.Image.cat(huesat, gray).hsvToRgb()
        # resolution = 15m
        res = 15

    else:
        print('I couldn\'t find the ' + collection +
              ' collection. Please choose between \'naip\'(default) and \'ls8\'.')
        return

    # the span to crop
    deg = .0075
    # if the order is defined as 'reverse'
    if order == 'descend':
        rg = list(reversed(range(id_start, id_end)))
    elif order == 'ascend':
        rg = range(id_start, id_end)
    else:
        print('I couldn\'t understand the download order ' + order +
              '. Please choose between \'ascend\'(default) and \'descend\'.')
        return

    # Each ID defines a unique power plant in egrid document
    for pid_int in rg:
        # find which one it is
        row = egrid.col_values(0).index(pid_int)
        try:
            # set the region to crop
            lat_center = float(egrid.cell_value(row, 4))
            long_center = float(egrid.cell_value(row, 5))
            # because 1 longt ~ 1 lat / cos(lat)
            scale = np.cos(lat_center / 180 * np.pi)
            geometry = ee.Geometry.Rectangle([
                long_center - deg / scale,  # longtitude lower bound
                lat_center - deg,  # latitude lower bound
                long_center + deg / scale,  # longtitude upper bound
                lat_center + deg  # latitude upper bound
            ])
            roi = image.clip(geometry)

            # configurations for export
            config_d = {
                'scale': res,					 # resolution
                'skipEmptyTiles': True,		 	 # action flag
                'maxPixels': 1E13,				 # max: 1E13
                'folder': 'PowerPlants_' + collection  # destination
            }

            # define and start the task
            task = ee.batch.Export.image(roi, str(pid_int), config=config_d)
            task.start()

            print(str(pid_int) + ':' + collection)

        except ValueError:
            print(-1)


if __name__ == '__main__':
    id_start, id_end = (300, 500)  # include id_start, exclude id_end
    download_ppt_pic(id_start, id_end, order='descend', collection='ls8')
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
