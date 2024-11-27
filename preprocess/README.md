# Multi-thread MRI and PET data preprocessing pipelines
Currently, preprocessing brain images typically requires a significant amount of time. To address this, this sub-repository provides **multi-threaded** preprocessing scripts for MRI and PET scans written in `Python`. The scripts are organized in the following folder structure to enhance reproducibility and accelerate the preprocessing process.
## Folder structure

```
Preprocess
  ├─ MRI_preprocess
  │   ├─ scripts [xxx.sh run files] 
  │   ├─ MRI_Atlas [Software: ANTs]: Generation of individual brain atlases
  │   ├─ MRI_Flirt [Software: FSL]: Registration of the brain to the standard MNI template space
  │   ├─ MRI_SkullStrip [Software: FreeSurfer]: Skull-stripping the brain
  │   └─ MNI152_T1_1mm_brain.nii.gz <standard brain space>
  │
  ├─ Other_modality_preprocess
  │   ├─ scripts [xxx.sh run files] 
  │   └─ OM_SkullStrip [Software: ANTs via s3 algorithm]
  │ 
  └─ subject_ids.xlsx (ADNI subjects used in our experiments)
```

In this pipeline, we use several **important** neuroimaging software packages, including **ANTs, FSL,** and **FreeSurfer**, for the corresponding preprocessing steps. Note that the atlas to be registered must be in MNI space with a voxel resolution of `1mm × 1mm × 1mm`.

Additionally, unlike previous work that relies on alignment to **the MNI152 space** for processing, our approach emphasizes **individual differences** in the generative process, and alignment to the MNI152 standard space is not a requirement in this study.

If you find our preprocessing steps useful or if our project contributes to your work, please consider 🌟 our repository and citing **the corresponding software**❕ and the following paper:

```
@article{wang2024joint,
  title = {Joint learning framework of cross-modal synthesis and diagnosis for Alzheimer’s disease by mining underlying shared modality information},
  author = {Wang, Chenhui and Piao, Sirong and Huang, Zhizhong and Gao, Qi and Zhang, Junping and Li, Yuxin and Shan, Hongming and others},
  journal = {Medical Image Analysis},
  volume = {91},
  pages = {103032},
  year = {2024},
  publisher = {Elsevier}
}
```

```
@article{avants2009advanced,
	title={Advanced normalization tools ({ANTs})},
	author={Avants, Brian B and Tustison, Nick and Song, Gang and others},
	journal={Insight},
	volume={2},
	number={365},
	pages={1--35},
	year={2009}
}

@article{fischl2012freesurfer,
	title={{FreeSurfer}},
	author={Fischl, Bruce},
	journal={{NeuroImage}},
	volume={62},
	number={2},
	pages={774--781},
	year={2012},
	publisher={Elsevier}
}
```