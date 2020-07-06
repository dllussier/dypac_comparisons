#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:02:33 2019
@author: lussier
"""

import os
import numpy as np
from tqdm import tqdm
from nilearn import image 
from nilearn import plotting 
from nilearn import decomposition
from nilearn.regions import RegionExtractor
from nilearn.connectome import ConnectivityMeasure

path_base = '/home/lussier/Projects/data/abide/'
path_func = 'func/'
path_conf = 'func/'

# A text file in the functional folder containing the names of the functional files in a single column is used to generate the list for the dypac model.
func = []
func_file = open((os.path.join(path_base,path_func, 'functional_batch.txt')),'r')
for line in func_file:
    func.append(os.path.join(path_base,path_func, (line.strip())))
func_file.close()
print (func)

# A similar text file with the names of the confounds files in the same order as the functional is used to create the confounds file list for the model.
conf = []
conf_file = open((os.path.join(path_base,path_conf, 'confounds_batch.txt')),'r')
for line in conf_file:
    conf.append(os.path.join(path_base,path_conf, (line.strip())))
conf_file.close()
print (conf)

#canica decomposition for sample
canica = decomposition.CanICA(n_components=50, smoothing_fwhm=6.,
                memory="nilearn_cache", memory_level=2,
                threshold=3., verbose=10, random_state=0,
                standardize=True, detrend=True,
                mask_strategy='template')
canica.fit(func, confounds=conf)

#retrieve components and project back into 3D space then save as nifti
components = canica.components_
components_img = canica.masker_.inverse_transform(components)
components_img.to_filename('canica_50.nii.gz')

#visualize components on map
plotting.plot_prob_atlas(components_img, view_type='filled_contours',
                         title='CanICA components')


for i, cur_img in enumerate(image.iter_img(components_img)):
    plotting.plot_stat_map(cur_img, title="IC %d" % i, #display_mode="z", cut_coords=1,
                   colorbar=False)
plotting.show()

#region extraction from component map
extractor = RegionExtractor(components_img, threshold=0.5,
                            thresholding_strategy='ratio_n_voxels',
                            extractor='local_regions',
                            standardize=True, min_region_size=1350)
extractor.fit()

regions_extracted_img = extractor.regions_img_ # extracted regions
regions_index = extractor.index_ #region index
n_regions_extracted = regions_extracted_img.shape[-1] #total regions extracted

#visualize extracted regions
title = ('%d regions are extracted from %d components.'
         '\nEach separate color of region indicates extracted region'
         % (n_regions_extracted, 20))
plotting.plot_prob_atlas(regions_extracted_img, view_type='filled_contours',
                         title=title)

#validate results by comparing original and network region side by side
img = image.index_img(components_img, 4)
coords = plotting.find_xyz_cut_coords(img)
display = plotting.plot_stat_map(img, cut_coords=coords, colorbar=False,
                                 title='Single network')

regions_indices_of_map3 = np.where(np.array(regions_index) == 4)

display = plotting.plot_anat(cut_coords=coords,
                             title='Network regions')

colors = 'rgbcmyk'
for each_index_of_map3, color in zip(regions_indices_of_map3[0], colors):
    display.add_overlay(image.index_img(regions_extracted_img, each_index_of_map3),
                        cmap=plotting.cm.alpha_cmap(color))

plotting.show()

#compute functional connectivity matrices
correlations = []
connectome_measure = ConnectivityMeasure(kind='correlation')
for filename in func:
    timeseries_each_subject = extractor.transform(filename)
    correlation = connectome_measure.fit_transform([timeseries_each_subject])
    correlations.append(correlation)

mean_correlations = np.mean(correlations, axis=0).reshape(n_regions_extracted,
                                                          n_regions_extracted)

#visualization of matrices
title = 'Correlations between %d regions' % n_regions_extracted
display = plotting.plot_matrix(mean_correlations, vmax=1, vmin=-1,
                               colorbar=True, title=title)

#find the center of the regions and plot the connectome
regions_img = regions_extracted_img
coords_connectome = plotting.find_probabilistic_atlas_cut_coords(regions_img)

plotting.plot_connectome(mean_correlations, coords_connectome,
                         edge_threshold='90%', title=title)
