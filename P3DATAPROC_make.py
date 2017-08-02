'''
This script compiles the US Power Plants NAIP/LANDSAT8 Dataset.
To complete construction, a few simple steps need to be followed:

1. Have NAIP data in the "uspp_naip" folder, with unprocessed images' names being ID.tif;
   Have the "egrid_2014_subset.xslx" file which is the original dataset from which we croped those power plants out;
   Have the "accepted_ann_json.txt" file which has annotations from the MTurkers.
Items mentioned above should be directly under the root directory and named exactly as quoted. Otherwise the construction will fail.

2. (Optional, but strongly recommended!) Have Landsat8 data in the "uspp_landsat" folder, unprocessed images' names being ID.tif.
If you do not have this folder, annotations will still be generated.

3. Run this script.

4. After the program finishes, you should find a new folder called "annotations" with all annotated polygons merged by max voting,
in a binary png image format. They are ought to be the labels to use in classifying a power plant. Note that the binary values are
0 and 255, therefore you should normalize it to 0 and 1 at the actual practice.

   In addition, images in "uspp_naip" (and "uspp_landsat" if applicable) that can be corresponded to the "accepted_ann_json.txt"
are renamed (if annotations are found valid) or moved to "exceptions" (if annotations are missing or invalid). Detailed information
is added to the title. (Naming convention:"DataType_egridUniqueID_State_Type")

   Finally, a new file named "uspp_metadata.geojson" containing all power plants with valid annotations and their info from the
original sheet is generated.

5. In case that the process is interrupted, you can re-run it at the spot. All images that are already processed will be intouched,
and new power plants will be added to the end of the metadata.

6. For any problem displaying landsat data, run "fixLs.m".

Author: Boning Li
Email: boning.li@duke.edu

Developed for Duke Data+ 2017: Electricity Access
Jul 30, 2017
'''

=======
Duke Data+ 2017: Electricity Access
Jul 30, 2017


import os
import sys
import json
import numpy as np
from PIL import Image, ImageDraw
from xlrd import open_workbook

class USPP:
    def __init__(self,rdir):
        self.setflag = 1 # default: use both naip and landsat data
        self.valid = []
        self.invalid=[]

class USPP:
    def __init__(self, rdir):
        self.setflag = 1  # default: use both naip and landsat data
        self.valid = []
        self.invalid = []

        self.targets = {
            'root_dir': rdir,
            'naip_dir': 'uspp_naip',
            'landsat_dir': 'uspp_landsat',
            'ann_dir': 'annotations',
            'bi_dir': 'binary',
            'conf_dir': 'confidence',
            'no_ann_dir':'exceptions',
            'no_ann_dir': 'exceptions',
            'ann_json_file': 'accepted_ann_json.txt',
            'egrid_file': 'egrid2014_data_v2_PLNT14.xlsx',
            'update_file': 'uspp_metadata.geojson'
        }
        self.names = {}

        # check folders and files
        print('Checking directory, files, and data.....')
        if not self._checkExistence():
            sys.exit()
        else:
            print('Directory checked')

        # make folder for annotation binary masks
        ann_path_temp = os.path.join(self.targets['root_dir'],self.targets['ann_dir'])
        ann_path_temp_bi = os.path.join(ann_path_temp,self.targets['bi_dir'])
        ann_path_temp_conf = os.path.join(ann_path_temp,self.targets['conf_dir'])
        ann_path_temp = os.path.join(
            self.targets['root_dir'], self.targets['ann_dir'])
        ann_path_temp_bi = os.path.join(ann_path_temp, self.targets['bi_dir'])
        ann_path_temp_conf = os.path.join(
            ann_path_temp, self.targets['conf_dir'])
        if not os.path.exists(ann_path_temp):
            os.mkdir(ann_path_temp)
        if not os.path.exists(ann_path_temp_bi):
            os.mkdir(ann_path_temp_bi)
        if not os.path.exists(ann_path_temp_conf):
            os.mkdir(ann_path_temp_conf)
        # process annotations into masks and save them
        if os.path.isfile(self.targets['update_file']):
            with open(self.targets['update_file']) as f:
                self.ann_list = json.load(f)['features']
        else:
            self.ann_list = []

        self.processAnn()


    # add detailed info to image data names
    def _rename(self):
        os.rename(os.path.join(self.targets['root_dir'],self.targets['naip_dir'],self.names['old_name_n']),
                  os.path.join(self.targets['root_dir'],self.targets['naip_dir'],self.names['new_name_n']))
        if self.setflag:
            os.rename(os.path.join(self.targets['root_dir'],self.targets['landsat_dir'],self.names['old_name_l']),
                      os.path.join(self.targets['root_dir'],self.targets['landsat_dir'],self.names['new_name_l']))


    # preparation for rename
    def _constructNames(self,pid):
        try:
            pid_int=int(pid)
        except:
            print('Warning: %s is not a valid egrid ID!'%(pid))
            return -1 # no valid od

        row = self.egrid.col_values(0).index(pid_int)
        _sname = self.egrid.cell_value(row,1)
        # _pname = ''.join(self.egrid.cell_value(row,4).split())
        _type = self.egrid.cell_value(row,6)

        self.names['old_name_n'] = pid +'.tif'
        self.names['old_name_l'] = pid +'.tif'
        self.names['new_name_n'] = 'naip_'+ pid +'_'+ _sname +'_'+ _type +'.tif'
        self.names['new_name_l'] = 'ls8_'+ pid +'_'+ _sname +'_'+ _type +'.tif'

        if not os.path.isfile(os.path.join(self.targets['root_dir'],
                                            self.targets['naip_dir'],
                                            self.names['old_name_n'])) or\
                (self.setflag and not os.path.isfile(os.path.join(self.targets['root_dir'],
                                                                self.targets['landsat_dir'],
                                                                self.names['old_name_l']))):
            print('Warning: ID='+ pid +' missing in landsat data!')
            self.invalid.append((pid,0)) # because of no image

    # add detailed info to image data names
    def _rename(self):
        os.rename(os.path.join(self.targets['root_dir'], self.targets['naip_dir'], self.names['old_name_n']),
                  os.path.join(self.targets['root_dir'], self.targets['naip_dir'], self.names['new_name_n']))
        if self.setflag:
            os.rename(os.path.join(self.targets['root_dir'], self.targets['landsat_dir'], self.names['old_name_l']),
                      os.path.join(self.targets['root_dir'], self.targets['landsat_dir'], self.names['new_name_l']))

    # preparation for rename
    def _constructNames(self, pid):
        try:
            pid_int = int(pid)
        except:
            print('Warning: %s is not a valid egrid ID!' % (pid))
            return -1  # no valid od

        row = self.egrid.col_values(0).index(pid_int)
        _sname = self.egrid.cell_value(row, 1)
        # _pname = ''.join(self.egrid.cell_value(row,4).split())
        _type = self.egrid.cell_value(row, 6)

        self.names['old_name_n'] = pid + '.tif'
        self.names['old_name_l'] = pid + '.tif'
        self.names['new_name_n'] = 'naip_' + pid + '_' + _sname + '_' + _type + '.tif'
        self.names['new_name_l'] = 'ls8_' + pid + '_' + _sname + '_' + _type + '.tif'

        if not os.path.isfile(os.path.join(self.targets['root_dir'],
                                           self.targets['naip_dir'],
                                           self.names['old_name_n'])) or\
                (self.setflag and not os.path.isfile(os.path.join(self.targets['root_dir'],
                                                                  self.targets['landsat_dir'],
                                                                  self.names['old_name_l']))):
            print('Warning: ID=' + pid + ' missing in landsat data!')
            self.invalid.append((pid, 0))  # because of no image

            self._clearData('rm')
            return 0     # image does not exist
        else:
            return 1     # everything fine

    # (re)move images without annotations

    def _clearData(self,*option):
        no_ann_fpath=os.path.join(self.targets['root_dir'],self.targets['no_ann_dir'])
        no_ann_naip_fpath = os.path.join(no_ann_fpath,self.targets['naip_dir'])
        no_ann_ls_fpath = os.path.join(no_ann_fpath,self.targets['landsat_dir'])

        old_path_naip=os.path.join(self.targets['root_dir'],self.targets['naip_dir'],self.names['old_name_n'])
        new_path_naip=os.path.join(no_ann_fpath,self.targets['naip_dir'],self.names['old_name_n'])

        old_path_ls=os.path.join(self.targets['root_dir'],self.targets['landsat_dir'],self.names['old_name_l'])
        new_path_ls=os.path.join(no_ann_fpath,self.targets['landsat_dir'],self.names['old_name_l'])

        if not os.path.exists(no_ann_fpath): os.mkdir(no_ann_fpath)
        if not os.path.exists(no_ann_naip_fpath): os.mkdir(no_ann_naip_fpath)
        if not os.path.exists(no_ann_ls_fpath): os.mkdir(no_ann_ls_fpath)

        if option[0]=='mv':        # move those with no annotations in another folder
            try:
                os.rename(old_path_naip, new_path_naip)
            except: pass
            if self.setflag:
                try:
                    os.rename(old_path_ls, new_path_ls)
                except: pass
        else:
            try:
                os.remove(old_path_naip)
            except: pass
            if self.setflag:
                try:
                    os.remove(old_path_ls)
                except: pass

    def _clearData(self, *option):
        no_ann_fpath = os.path.join(
            self.targets['root_dir'], self.targets['no_ann_dir'])
        no_ann_naip_fpath = os.path.join(
            no_ann_fpath, self.targets['naip_dir'])
        no_ann_ls_fpath = os.path.join(
            no_ann_fpath, self.targets['landsat_dir'])

        old_path_naip = os.path.join(
            self.targets['root_dir'], self.targets['naip_dir'], self.names['old_name_n'])
        new_path_naip = os.path.join(
            no_ann_fpath, self.targets['naip_dir'], self.names['old_name_n'])

        old_path_ls = os.path.join(
            self.targets['root_dir'], self.targets['landsat_dir'], self.names['old_name_l'])
        new_path_ls = os.path.join(
            no_ann_fpath, self.targets['landsat_dir'], self.names['old_name_l'])

        if not os.path.exists(no_ann_fpath):
            os.mkdir(no_ann_fpath)
        if not os.path.exists(no_ann_naip_fpath):
            os.mkdir(no_ann_naip_fpath)
        if not os.path.exists(no_ann_ls_fpath):
            os.mkdir(no_ann_ls_fpath)

        if option[0] == 'mv':
        # move the specified files to another folder
            try:
                os.rename(old_path_naip, new_path_naip)
            except:
                pass
            if self.setflag:
                try:
                    os.rename(old_path_ls, new_path_ls)
                except:
                    pass
        else:
        # remove the specified files
            try:
                os.remove(old_path_naip)
            except:
                pass
            if self.setflag:
                try:
                    os.remove(old_path_ls)
                except:
                    pass


    # check if all required data exists
    def _checkExistence(self):
        ret = 0
        # check root / files
        if not os.path.exists(self.targets['root_dir']):
            print('Root directory does not exist!')
            ret-=1
        else:
            if not os.path.isfile(os.path.join(self.targets['root_dir'],self.targets['ann_json_file'])):
                print('Cannot find annotation text!')
                ret-=1
            if not os.path.isfile(os.path.join(self.targets['root_dir'],self.targets['egrid_file'])):
                print('Cannot find egrid sheet!')
                ret-=1
            # check naip data
            if not os.path.exists(os.path.join(self.targets['root_dir'],self.targets['naip_dir'])):
                print('NAIP data directory missing or false named! If you do have NAIP data, please put them in a and make sure it\'s named \"uspp_naip\".')
                ret-=1
            # check landsat data
            if not os.path.exists(os.path.join(self.targets['root_dir'],self.targets['landsat_dir'])):
                print('Warning! Landsat data missing or falsely named. They will not be used during the following process. If you do have Landsat data and want to use it, please put them in a folder directly under the root and make sure it\'s named \"uspp_landsat\" and run it again.')
                self.setflag = 0 # use naip only
                return ret==0

            ret -= 1
        else:
            if not os.path.isfile(os.path.join(self.targets['root_dir'], self.targets['ann_json_file'])):
                print('Cannot find annotation text!')
                ret -= 1
            if not os.path.isfile(os.path.join(self.targets['root_dir'], self.targets['egrid_file'])):
                print('Cannot find egrid sheet!')
                ret -= 1
            # check naip data
            if not os.path.exists(os.path.join(self.targets['root_dir'], self.targets['naip_dir'])):
                print('NAIP data directory missing or false named! If you do have NAIP data, please put them in a and make sure it\'s named \"uspp_naip\".')
                ret -= 1
            # check landsat data
            if not os.path.exists(os.path.join(self.targets['root_dir'], self.targets['landsat_dir'])):
                print('Warning! Landsat data missing or falsely named. They will not be used during the following process. If you do have Landsat data and want to use it, please put them in a folder directly under the root and make sure it\'s named \"uspp_landsat\" and run it again.')
                self.setflag = 0  # use naip only
        return ret == 0


    # generate a geojson file which contains the info of all validated power plants
    def saveUpdates(self):
        compiled = {
            "type": "FeatureCollection",
            "features": self.ann_list
        }
        with open(self.targets['update_file'], 'w') as output:
            json.dump(compiled,output,sort_keys=False,indent=4)
            json.dump(compiled, output, sort_keys=False, indent=4)


    # parse json text files
    def processAnn(self):
        # open annotation json text file
        self.anntext=open(os.path.join(self.targets['root_dir'],
                                       self.targets['ann_json_file']), 'r')
        # load egrid file
        self.egrid = open_workbook(os.path.join(self.targets['root_dir'],
                                                self.targets['egrid_file'])).sheet_by_index(0)
        self.anntext = open(os.path.join(self.targets['root_dir'],
                                         self.targets['ann_json_file']), 'r')
        # load egrid file
        self.egrid = open_workbook(os.path.join(self.targets['root_dir'],
                                                self.targets['egrid_file'])).sheet_by_index(0)
        count = 0
        while 1:
            try:
                json_text = self.anntext.readline()
                ann_temp = json.loads(json_text)

                pid = ann_temp['fileName'].rsplit('/',1)[1][:-4]
                cn=self._constructNames(pid)
                if cn!=1:
                    # did not find the file with this id
                    count+=1*(cn!=-1)

                pid = ann_temp['fileName'].rsplit('/', 1)[1][:-4]
                cn = self._constructNames(pid)
                if cn != 1:
                    # did not find the file with this id
                    count += 1 * (cn != -1)
                    continue

                with Image.open(os.path.join(self.targets['root_dir'],
                                             self.targets['naip_dir'],
                                             self.names['old_name_n'])) as img_temp:
                    ann_temp['img_size']=img_temp.size # (width,height)

                mask = np.zeros(ann_temp['img_size'],dtype=np.uint8)
                poly_verts = ann_temp['objs'][0]['data'] # polygon verticle coordinates

                for ipoly in range(0,len(poly_verts[0])):
                    xys = [poly_verts[0][ipoly],poly_verts[1][ipoly]]
                    poly_xys_temp=[(xys[0][i], xys[1][i]) for i in range(0,len(xys[0]))]

                    img=Image.new('L',ann_temp['img_size'][::-1],0)
                    ImageDraw.Draw(img).polygon(poly_xys_temp, outline=1, fill=1)
                    mask = mask + np.array(img,dtype=np.uint8)

                mask_conf = np.array(mask)
                # binarize the mask
                if not sorted(np.unique(mask)) == sorted([0,1]):
                    mask[mask<2]=0
                    mask[mask>0]=1
                mask*=255

                if np.sum(mask)==0:
                    print('Warning: No annotations for ID'+pid)
                    self.invalid.append((pid,1)) # because of no annotation
                    self._clearData('mv')
                    count+=1
                    ann_temp['img_size'] = img_temp.size  # (width,height)

                mask = np.zeros(ann_temp['img_size'], dtype=np.uint8)
                # polygon verticle coordinates
                poly_verts = ann_temp['objs'][0]['data']

                for ipoly in range(0, len(poly_verts[0])):
                    xys = [poly_verts[0][ipoly], poly_verts[1][ipoly]]
                    poly_xys_temp = [(xys[0][i], xys[1][i])
                                     for i in range(0, len(xys[0]))]

                    img = Image.new('L', ann_temp['img_size'][::-1], 0)
                    ImageDraw.Draw(img).polygon(
                        poly_xys_temp, outline=1, fill=1)
                    mask = mask + np.array(img, dtype=np.uint8)

                mask_conf = np.array(mask)
                # binarize the mask
                if not sorted(np.unique(mask)) == sorted([0, 1]):
                    mask[mask < 2] = 0
                    mask[mask > 0] = 1
                mask *= 255

                if np.sum(mask) == 0:
                    print('Warning: No annotations for ID' + pid)
                    self.invalid.append((pid, 1))  # because of no annotation
                    self._clearData('mv')
                    count += 1
                    continue

                # rename the original images
                self._rename()

                # save mask file
                Image.fromarray(mask).save(os.path.join(self.targets['root_dir'],self.targets['ann_dir'],self.targets['bi_dir'],'bilabels_'+pid+'.png'))
                Image.fromarray(mask_conf).save(os.path.join(self.targets['root_dir'],self.targets['ann_dir'],self.targets['conf_dir'],'conflabels_'+pid+'.png'))

                Image.fromarray(mask).save(os.path.join(
                    self.targets['root_dir'], self.targets['ann_dir'], self.targets['bi_dir'], 'bilabels_' + pid + '.png'))
                Image.fromarray(mask_conf).save(os.path.join(
                    self.targets['root_dir'], self.targets['ann_dir'], self.targets['conf_dir'], 'conflabels_' + pid + '.png'))
                self.valid.append(pid)

                # generate geojson
                if not any(ann_item['properties']['egrid_ID'] == pid for ann_item in self.ann_list):
                    row = self.egrid.col_values(0).index(int(pid))
                    if self.setflag:
                        available_data_flag='NAIP&LANDSAT'
                    else:
                        available_data_flag='NAIP'
                    geodict = {
                            'type':'Feature',
                            'geometry':{
                                    'type':'Point',
                                    'coordinates':(np.float(self.egrid.cell_value(row,5)), # longitude
                                                   np.float(self.egrid.cell_value(row,4))) # latidtude
                                    },
                            'properties':{
                                    'egrid_ID':pid,
                                    'plant_name':self.egrid.cell_value(row,2),
                                    'state_name':self.egrid.cell_value(row,1),
                                    'county_name':self.egrid.cell_value(row,3),
                                    'primary_fuel':self.egrid.cell_value(row,6),
                                    'fossil_fuel':self.egrid.cell_value(row,7),
                                    'capacity_factor':self.egrid.cell_value(row,8),
                                    'nameplate_cap_MW':self.egrid.cell_value(row,9),
                                    'co2_emission':self.egrid.cell_value(row,10),
                                    'availability':available_data_flag
                                    }
                            }
                    self.ann_list.append(geodict)
                count+=1

            except:
                # save ann_list
                self.saveUpdates()
                summary = '''
*************************** Summary ***************************
A total of %d annotation lines with valid egrid IDs were read,
%d of which are valid powerplants and thus processed;
%d don\'t have image/annotation at all and thus abandoned.
For further investigation, please find the void ones in "\exceptions",
with the following indecies:\n'''%(count,len(self.valid),len(self.invalid))

with the following indecies:
                print(summary)
                print('%s' %
                      (', '.join(map(str, [item[0] for item in self.invalid]))))
                break


if __name__ == '__main__':
    rdir = os.path.dirname(os.path.realpath(__file__))
    pDataSet = USPP(rdir)
