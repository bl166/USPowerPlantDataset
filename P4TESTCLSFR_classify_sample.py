'''
classify_sample.py

This script runs a simple machine learning test on the dataset.

General flow: in a loop,
1. Parse a line to get a unique id from metadata (uspp_metadata.geojson);
2. Use the id to find corresponding files from both landsat folder and annotation folder;
3. For the image, extract features from the window centered at each pixel to form X;
(features = means and variances of r, g, and b channels -> length = 6);
4. In the same order, flatten the binary annotation image to form y;
5. Send [X,y] to any clalssifer (here LDA) for either cross validation or specific case test.

Author: Boning Li
Email: boning.li@duke.edu
Developed for Duke Data+ 2017: Electricity Access
Jul 26, 2017
'''

<<<<<<< HEAD
=======

>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda
from sklearn.ensemble import RandomForestClassifier as rfc
from matplotlib import pyplot as plt
from sklearn import metrics
from scipy import signal
from PIL import Image
import numpy as np
import json
import sys
import os
import re

<<<<<<< HEAD
class Curve: # ROC
    auc = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
=======

class Curve:  # ROC
    auc = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
    def plot(self, subfig):
        subfig.grid()
        subfig.plot(self.x, self.y, lw=2)
        subfig.plot([0, 1], [0, 1], 'k--')
        subfig.set_xlim([0.0, 1.0])
        subfig.set_ylim([0.0, 1.0])
        subfig.set_xlabel('False Positive Rate', fontsize=12)
        subfig.set_ylabel('True Positive Rate', fontsize=12)
        subfig.set_title('AUC = %f' % (self.auc))
<<<<<<< HEAD
        x0,x1 = subfig.get_xlim()
        y0,y1 = subfig.get_ylim()
        subfig.set_aspect((x1-x0)/(y1-y0))


class Observations:
    targets={
        'root_dir': os.path.dirname(os.path.realpath(__file__)),
        'img_dir':  os.path.join(os.path.dirname(os.path.realpath(__file__)),'uspp_landsat'),
        'lab_dir':  os.path.join(os.path.dirname(os.path.realpath(__file__)),'annotations'),
        'feat_file': os.path.join(os.path.dirname(os.path.realpath(__file__)),'uspp_metadata.geojson')
    }
    X=[]
    y=[]
    id_list = []
    nElementsEach = []
    existence = [True,[]]
=======
        x0, x1 = subfig.get_xlim()
        y0, y1 = subfig.get_ylim()
        subfig.set_aspect((x1 - x0) / (y1 - y0))


class Observations:
    targets = {
        'root_dir': os.path.dirname(os.path.realpath(__file__)),
        'img_dir':  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uspp_landsat'),
        'lab_dir':  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotations'),
        'feat_file': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uspp_metadata.geojson')
    }
    X = []
    y = []
    id_list = []
    nElementsEach = []
    existence = [True, []]
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
    idx_all = []
    idx_tr = []
    idx_ts = []
    scr = []
    sizes = []
    method = 'lda'

<<<<<<< HEAD

    def __init__(self,*args):
        # check if everything exist to proceed
        self.checkExist()
        if not self.existence[0]:
            print('Cannot find the following item(s), please check:\n%s'%'\n'.join(map(str,self.existence[1])))
=======
    def __init__(self, *args):
        # check if everything exist to proceed
        self.checkExist()
        if not self.existence[0]:
            print('Cannot find the following item(s), please check:\n%s' %
                  '\n'.join(map(str, self.existence[1])))
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
            sys.exit()

        self.windowSize = args[0]
        self.loadObservations()

<<<<<<< HEAD

=======
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
    def checkExist(self):
        if not os.path.exists(self.targets['root_dir']):
            self.existence[1].append(self.targets['root_dir'])
            self.existence[0] = False
<<<<<<< HEAD
        if not os.path.exists(os.path.join(self.targets['root_dir'],self.targets['img_dir'])):
            self.existence[1].append(self.targets['img_dir'])
            self.existence[0] = False
        if not os.path.exists(os.path.join(self.targets['root_dir'],self.targets['lab_dir'])):
            self.existence[1].append(self.targets['lab_dir'])
            self.existence[0] = False
        if not os.path.isfile(os.path.join(self.targets['root_dir'],self.targets['feat_file'])):
            self.existence[1].append(self.targets['feat_file'])
            self.existence[0] = False


=======
        if not os.path.exists(os.path.join(self.targets['root_dir'], self.targets['img_dir'])):
            self.existence[1].append(self.targets['img_dir'])
            self.existence[0] = False
        if not os.path.exists(os.path.join(self.targets['root_dir'], self.targets['lab_dir'])):
            self.existence[1].append(self.targets['lab_dir'])
            self.existence[0] = False
        if not os.path.isfile(os.path.join(self.targets['root_dir'], self.targets['feat_file'])):
            self.existence[1].append(self.targets['feat_file'])
            self.existence[0] = False

>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
    def loadObservations(self):
        # from compiled geojson
        with open(self.targets['feat_file']) as f:
            self.obs = json.load(f)['features']
<<<<<<< HEAD
        print('%d observations are loaded.'%(len(self.obs)))
        print('**** Feature Extraction ****')

        # a few computational parameters
        self.nFeatures = 6;
=======
        print('%d observations are loaded.' % (len(self.obs)))
        print('**** Feature Extraction ****')

        # a few computational parameters
        self.nFeatures = 6
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
        windowDiameter = 2 * self.windowSize - 1
        nPixelsInWindow = pow(windowDiameter, 2)
        convMask = np.ones([windowDiameter] * 2)

        # initialize X and y
<<<<<<< HEAD
        self.X=np.array([]).reshape(0,self.nFeatures)
        self.y=np.array([]).reshape(0,1)

        for i in range(0,len(self.obs)):
=======
        self.X = np.array([]).reshape(0, self.nFeatures)
        self.y = np.array([]).reshape(0, 1)

        for i in range(0, len(self.obs)):
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
            # if id is not found in the training list, skip
            ob_temp = self.obs[i]
            self.id_list.append(ob_temp['properties']['egrid_ID'])

            # construct file names and load
<<<<<<< HEAD
            img_name = 'ls8_'+self.id_list[-1]+'_'+ob_temp['properties']['state_name']+'_'+ob_temp['properties']['primary_fuel']+'.tif'
            lab_name = 'labels'+self.id_list[-1]+'.png'
            img = np.array(Image.open(os.path.join(self.targets['img_dir'],img_name)))
            lab = np.array(np.array(Image.open(os.path.join(self.targets['lab_dir'],lab_name)).resize(img.shape[:2][::-1]))>0)
=======
            img_name = 'ls8_' + self.id_list[-1] + '_' + ob_temp['properties']['state_name'] + \
                '_' + ob_temp['properties']['primary_fuel'] + '.tif'
            lab_name = 'labels' + self.id_list[-1] + '.png'
            img = np.array(Image.open(os.path.join(
                self.targets['img_dir'], img_name)))
            lab = np.array(np.array(Image.open(os.path.join(
                self.targets['lab_dir'], lab_name)).resize(img.shape[:2][::-1])) > 0)
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c

            self.sizes.append(lab.shape)

            # extract features
<<<<<<< HEAD
            nPixels = np.multiply(lab.shape[0],lab.shape[1]) # number of pixels in the whole image
            features = np.empty((nPixels, self.nFeatures))  # Initialize feature vector
            features[:] = np.nan

            for iChannel in range(0,img.shape[2]):
                cChannel = np.squeeze(img[:, :, iChannel])

                cChannelMean = (1 / nPixelsInWindow) * signal.convolve2d(cChannel, convMask, mode='same')
                cChannelMeanSquare = (1 / nPixelsInWindow) * signal.convolve2d(np.square(cChannel), convMask, mode='same')
                cChannelVariance = cChannelMeanSquare - np.square(cChannelMean)

                # Store the features
                features[:, iChannel] = cChannelMean.reshape(nPixels, order='C') - np.mean(cChannelMean)       # RGB means: [1,2,3]
                features[:, iChannel+img.shape[2]] = cChannelVariance.reshape(nPixels, order='C') - np.mean(cChannelVariance)   # RGB variances: [4,5,6]

            self.X = np.vstack((self.X, features))
            self.y = np.vstack((self.y, lab.reshape((nPixels,1), order='C')))
=======
            # number of pixels in the whole image
            nPixels = np.multiply(lab.shape[0], lab.shape[1])
            # Initialize feature vector
            features = np.empty((nPixels, self.nFeatures))
            features[:] = np.nan

            for iChannel in range(0, img.shape[2]):
                cChannel = np.squeeze(img[:, :, iChannel])

                cChannelMean = (1 / nPixelsInWindow) * \
                    signal.convolve2d(cChannel, convMask, mode='same')
                cChannelMeanSquare = (
                    1 / nPixelsInWindow) * signal.convolve2d(np.square(cChannel), convMask, mode='same')
                cChannelVariance = cChannelMeanSquare - np.square(cChannelMean)

                # Store the features
                features[:, iChannel] = cChannelMean.reshape(
                    nPixels, order='C') - np.mean(cChannelMean)       # RGB means: [1,2,3]
                features[:, iChannel + img.shape[2]] = cChannelVariance.reshape(
                    nPixels, order='C') - np.mean(cChannelVariance)   # RGB variances: [4,5,6]

            self.X = np.vstack((self.X, features))
            self.y = np.vstack((self.y, lab.reshape((nPixels, 1), order='C')))
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c

            self.nElementsEach.append(nPixels)

        self.y = self.y.reshape(self.y.shape[0])
        self.idx_all = np.random.permutation(len(self.y))
<<<<<<< HEAD
        print('X: '+str(self.X.shape))
        print('y: '+str(self.y.shape))
        print(('Loading finished with %d instances in total.')%(len(self.y)))


    def crossValidate(self,*args):
        print('**** Cross Validation ****')
        score=np.zeros(len(self.y))
=======
        print('X: ' + str(self.X.shape))
        print('y: ' + str(self.y.shape))
        print(('Loading finished with %d instances in total.') % (len(self.y)))

    def crossValidate(self, *args):
        print('**** Cross Validation ****')
        score = np.zeros(len(self.y))
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
        self.method = args[1]

        # Split features into training and validation subsets
        nfolder = args[0]
<<<<<<< HEAD
        fz = len(self.X)/nfolder
        for ff in range(0, nfolder):
            print('Working on the %d of %d folders...'%(ff+1,nfolder),end='\r')
            self.idx_ts=self.idx_all[int(fz*ff):int(fz*(ff+1))]
            self.idx_tr=np.setdiff1d(self.idx_all,self.idx_ts)
=======
        fz = len(self.X) / nfolder
        for ff in range(0, nfolder):
            print('Working on the %d of %d folders...' %
                  (ff + 1, nfolder), end='\r')
            self.idx_ts = self.idx_all[int(fz * ff):int(fz * (ff + 1))]
            self.idx_tr = np.setdiff1d(self.idx_all, self.idx_ts)
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c

            self.trainAndPredict()
            score[self.idx_ts] = np.array([item[1] for item in self.scr])

        # calculate roc
        pf, pd, _ = metrics.roc_curve(self.y, score)
        self.cross_roc = Curve(pf, pd)
        self.cross_roc.auc = metrics.roc_auc_score(self.y, score)

        # plot roc
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        self.cross_roc.plot(ax1)
        plt.show()

    def trainAndPredict(self):
        # train on training subset
        if self.method == 'lda':
            mdl = lda().fit(self.X[self.idx_tr, :], self.y[self.idx_tr])
        elif self.method == 'rf':
<<<<<<< HEAD
            mdl = rfc(n_estimators=100).fit(self.X[self.idx_tr, :], self.y[self.idx_tr])

        # test on testing subset
        self.scr=mdl.predict_proba(self.X[self.idx_ts, :])


    def test(self,test_list,*med_opt):
        print('**** Test ****')
        if len(med_opt): self.method = med_opt[0]
=======
            mdl = rfc(n_estimators=100).fit(
                self.X[self.idx_tr, :], self.y[self.idx_tr])

        # test on testing subset
        self.scr = mdl.predict_proba(self.X[self.idx_ts, :])

    def test(self, test_list, *med_opt):
        print('**** Test ****')
        if len(med_opt):
            self.method = med_opt[0]
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c

        for test_item in test_list:
            # confirm that test_item is in range
            if str(test_item) not in self.id_list:
                print('Test case not found')
                continue

            # find which one is to be tested
            test_img_idx = self.id_list.index(str(test_item))

            # find pixel-wise indecies
            ts_start = np.array(self.nElementsEach[:test_img_idx]).sum()
<<<<<<< HEAD
            ts_end = ts_start+self.nElementsEach[test_img_idx]
            self.idx_ts = list(range(int(ts_start),int(ts_end)))
            self.idx_tr = np.setdiff1d(self.idx_all,self.idx_ts)
=======
            ts_end = ts_start + self.nElementsEach[test_img_idx]
            self.idx_ts = list(range(int(ts_start), int(ts_end)))
            self.idx_tr = np.setdiff1d(self.idx_all, self.idx_ts)
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c

            # train and predict
            self.trainAndPredict()

            # make confidence map
<<<<<<< HEAD
            self.genConfMap(test_img_idx,test_item)


    def genConfMap(self,test_img_idx,test_item):
            fig = plt.figure()

            # display cmap
            ax1 = fig.add_subplot(133)
            ax1.imshow(np.reshape([item[1] for item in self.scr],self.sizes[test_img_idx], order='C'))
            ax1.set_title('Prediction confidence map - '+self.method)

            # display true annotation
            ax2 = fig.add_subplot(132)
            ax2.imshow(np.reshape(self.y[self.idx_ts],self.sizes[test_img_idx], order='C'))
            ax2.set_title('True annotation(s)')

            # display original image
            ax3 = fig.add_subplot(131)
            ob = next((item for item in self.obs if item['properties']['egrid_ID'] == str(test_item)))
            fname = 'ls8_'+ob['properties']['egrid_ID']+'_'+ob['properties']['state_name']+'_'+ob['properties']['primary_fuel']+'.tif'
            orig_img = Image.open(os.path.join(self.targets['root_dir'],self.targets['img_dir'],fname))
            ax3.imshow(np.array(orig_img))
            ax3.set_title('Orignial image, ID='+ob['properties']['egrid_ID'])

            plt.show()
=======
            self.genConfMap(test_img_idx, test_item)

    def genConfMap(self, test_img_idx, test_item):
        fig = plt.figure()

        # display cmap
        ax1 = fig.add_subplot(133)
        ax1.imshow(np.reshape([item[1] for item in self.scr],
                              self.sizes[test_img_idx], order='C'))
        ax1.set_title('Prediction confidence map - ' + self.method)

        # display true annotation
        ax2 = fig.add_subplot(132)
        ax2.imshow(np.reshape(self.y[self.idx_ts],
                              self.sizes[test_img_idx], order='C'))
        ax2.set_title('True annotation(s)')

        # display original image
        ax3 = fig.add_subplot(131)
        ob = next(
            (item for item in self.obs if item['properties']['egrid_ID'] == str(test_item)))
        fname = 'ls8_' + ob['properties']['egrid_ID'] + '_' + \
            ob['properties']['state_name'] + '_' + \
            ob['properties']['primary_fuel'] + '.tif'
        orig_img = Image.open(os.path.join(
            self.targets['root_dir'], self.targets['img_dir'], fname))
        ax3.imshow(np.array(orig_img))
        ax3.set_title('Orignial image, ID=' + ob['properties']['egrid_ID'])

        plt.show()
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c


if __name__ == '__main__':
    obs_class = Observations(15)
<<<<<<< HEAD
    obs_class.crossValidate(4,'lda')
    obs_class.test([300],'lda')
=======
    obs_class.crossValidate(4, 'lda')
    obs_class.test([300], 'lda')
>>>>>>> f794a9cc33734a559212be121fe88bc94f6d3d9c
