#!/usr/bin/env python
# coding: utf-8
import os
import dypac_masker
import pickle as pk
from glob import glob
from tqdm import tqdm
from dypac import Dypac
from nilearn.plotting import view_img
from nilearn import datasets
from nilearn import plotting 
from fetcher import fetch_difumo

# load a dypac model
file_model = f'models/dev_aging_sz/Dypac_64c_256s_8mm.pickle'
pickle_in = open(file_model, "rb")
model = pk.load(pickle_in)
pickle_in.close()

# Fetch a preprocessed dataset
path_base = '/lustre04/scratch/dlussier/embeddings/'
path_func = 'resampled_data/'
r2_path = 'r2maps/dev_aging_sz/64c_256s_8mm/'

func = []
func_file = open((os.path.join(path_base, path_func, 'functional_test.txt')),'r')
for line in func_file:
    func.append(os.path.join(path_base,path_func, (line.strip())))
func_file.close()

epi_filename = func[0]

# # Dypac
# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    score = model.score(img)
    saving_name = os.path.join(path_base, r2_path, f'dypac_{idx}.nii.gz')
    score.to_filename(saving_name)

# # "hard parcels": the Schaefer atlas
atlas = datasets.fetch_atlas_schaefer_2018()
labels_masker = dypac_masker.LabelsMasker(model=model, labels=atlas.maps)
r2_map = labels_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = labels_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'schaefer_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# # "hard parcels": Yeo 2011
atlas = datasets.fetch_atlas_yeo_2011()
labels_masker = dypac_masker.LabelsMasker(model=model, labels=atlas.thick_17)
r2_map = labels_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = labels_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'yeo_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# # "hard parcels": MIST
atlas = "atlases/MIST_444.nii.gz"
labels_masker = dypac_masker.LabelsMasker(model=model, labels=atlas)
r2_map = labels_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = labels_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'mist_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# # "hard parcels": Shen
atlas = "atlases/shen_2mm_268_parcellation.nii.gz"
labels_masker = dypac_masker.LabelsMasker(model=model, labels=atlas)
r2_map = labels_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = labels_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'shen_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# # "hard parcels": Gordon
atlas = "atlases/Parcels_Gordon_MNI_333.nii"
labels_masker = dypac_masker.LabelsMasker(model=model, labels=atlas)
r2_map = labels_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = labels_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'gordon_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# # "soft" parcels: the ICA atlas from Smith et al. (2009)
ica_maps = datasets.fetch_atlas_smith_2009()
maps_masker = dypac_masker.MapsMasker(model=model, maps=ica_maps.rsn70)
r2_map = maps_masker.score(img=epi_filename)


# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = maps_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'smith_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# # Difumo
# Difumo 256
ica_maps = fetch_difumo(dimension=256).maps
maps_masker = dypac_masker.MapsMasker(model=model, maps=ica_maps)
r2_map = maps_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = maps_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'difumo_256_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# Difumo 512
ica_maps = fetch_difumo(dimension=512).maps
maps_masker = dypac_masker.MapsMasker(model=model, maps=ica_maps)
r2_map = maps_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = maps_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'difumo_512_{idx}.nii.gz')
    r2map.to_filename(saving_name)

# Difumo 1024
ica_maps = fetch_difumo(dimension=1024).maps
maps_masker = dypac_masker.MapsMasker(model=model, maps=ica_maps)
r2_map = maps_masker.score(img=epi_filename)

# generate a R2 map and save the R2 map as a nifti image
for idx in tqdm(range(len(func))):
    img = model.load_img(func[idx])
    r2map = maps_masker.score(img)
    saving_name = os.path.join(path_base, r2_path,f'difumo_1024_{idx}.nii.gz')
    r2map.to_filename(saving_name)
