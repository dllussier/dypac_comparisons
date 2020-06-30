#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 13:51:01 2020

@author: desiree lussier

This script loads the previously run dypac embeddings model for abide and 
generates the R2 mappings, which quantifies the quality of an embedding,  
for each subject, saving them as nifti files for later use with Nistats.
"""

#import libraries
import os
import pickle
from dypac import Dypac
from tqdm import tqdm

#paths to data
path_base = '/home/lussier/Projects/data/abide/'
path_func = 'func/'
path_r2 = 'r2maps/'

#this takes the same list as the original model
func = []
func_file = open((os.path.join(path_base,path_func, 'functional_batch.txt')),'r')
for line in func_file:
    func.append(os.path.join(path_base,path_func, (line.strip())))
func_file.close()
print (func)

#open the model
file = open("Dypac_abide_pass_sub30clu50sta150bat4smo5thr02.pickle", "rb")
model = pickle.load(file)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    score = model.score(img)
    saving_name = os.path.join(path_base,path_r2,f'sub_{idx}.nii.gz')
    score.to_filename(saving_name)
