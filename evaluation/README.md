

# 3D Cross-Modality Synthesis Evaluation Metrics

In this sub-repository, we provide a set of supervised evaluation scripts for imaging metrics such as `MAE`, `PSNR`, `SSIM2D`, and `SSIM3D`. These can be used by specifying the file paths for the real and generated images.

## Evaluation

To evaluate the generated images in a supervised manner, run the following command:

```
python ./evaluation_metrics.py \
  --out_results_dir ./ \              # Output directory for the results
  --methodname GenPET \               # Specify the subdirectory of the generated images
  --data_range 2.6 \                  # Specify the PSNR range for the modality
  --window_size 11 \                  # Specify the SSIM window size
  --real_image_path your_real_image_path \  # Path to the real image
  --generated_image_path your_generated_image_path  # Path to the generated image
```

**Note**: We do not use `PSNR` as the evaluation metric in this case, because voxel intensities for tracer-specific PET images can vary, and using a unified `data_range` may not fully capture the differences across different tracers.


## Acknowledgement & Citation
If you find our preprocessing steps useful or if our project contributes to your work, please consider 🌟 our repository and citing **the corresponding metric**❕ and the following paper:
```
@article{wang2024joint,
  title = {Joint learning framework of cross-modal synthesis and diagnosis for {Alzheimer’s} disease by mining underlying shared modality information},
  author = {Wang, Chenhui and Piao, Sirong and Huang, Zhizhong and Gao, Qi and Zhang, Junping and Li, Yuxin and Shan, Hongming and others},
  journal = {Med. Image Anal.},
  volume = {91},
  pages = {103032},
  year = {2024},
  publisher = {Elsevier}
}
```

```
@article{setiadi2021psnr,
  title={{PSNR} vs {SSIM}: imperceptibility quality assessment for image steganography},
  author={Setiadi, De Rosal Igantius Moses},
  journal={Multimed. Tools Appl.},
  volume={80},
  number={6},
  pages={8423--8444},
  year={2021},
  publisher={Springer}
}
```