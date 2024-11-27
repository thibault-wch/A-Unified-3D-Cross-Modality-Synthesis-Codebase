import torch
import pandas as pd
import os
import nibabel as nib
from tqdm import tqdm
from SSIM3D import *
import argparse
from datetime import datetime
from loguru import logger

def cal_single_mape(image_true, image_generated):
    mask = image_true != 0
    return (torch.abs(image_true - image_generated) / (image_true) * 100)[mask].mean().item()


def cal_single_mae(image_true, image_generated):
    return torch.abs(
        image_true - image_generated
    ).mean().item()


def cal_single_psnr(image_true, image_generated, data_range=2.6):
    return 10 * torch.log10((data_range ** 2) /
                            ((image_true - image_generated) ** 2).mean()).item()


def cal_single_performance_evaluation(image_true, image_generated, itemname, data_range=2.6, window_size=11):
    # please verify the all data value > 0

    # original cuda evaluation
    image_true = image_true.cuda()
    image_generated = image_generated.cuda()

    # metric calculation
    # mape = cal_single_mape(image_true, image_generated)
    mae = cal_single_mae(image_true, image_generated)
    psnr = cal_single_psnr(image_true, image_generated, data_range=data_range)
    ssim = ssim3D(image_true, image_generated, data_range=data_range, window_size=window_size).item()

    return {
        'name': itemname[-14:],
        'mae': mae,
        'psnr': psnr,
        'ssim': ssim
    }


def save_results(datalist, datadir, name):
    df = pd.DataFrame(datalist)
    stats = df.describe()

    logger.info(stats.loc[['mean', 'std', 'min', 'max']])

    if not os.path.exists(datadir):
        os.makedirs(datadir)
    if not os.path.exists(datadir + '/stats'):
        os.makedirs(datadir + '/stats')

    df.to_csv(datadir + '/'  + name + '.csv', index=False)
    stats.to_csv(datadir + '/stats/' + 'stats_' + name + '.csv')
    return None


def get_data_nii(datapath):
    img = nib.load(datapath)
    data = torch.tensor(img.get_fdata()).unsqueeze(0).unsqueeze(0).float()
    return data


def evaluate_single_type(real_image_path, generated_image_path, out_results_dir, methodname, data_range=2.6,
                         window_size=11):
    evaluate_list = []
    file_names = os.listdir(real_image_path)
    for item in tqdm(file_names):
        evaluate_item = cal_single_performance_evaluation(get_data_nii(real_image_path + '/' + item),
                                                          get_data_nii(
                                                              generated_image_path + '/' + item),
                                                          item, data_range=data_range, window_size=window_size)
        evaluate_list.append(evaluate_item)
    save_results(evaluate_list, out_results_dir + '/', methodname)



if __name__ == '__main__':

    """
    [A] real_image_path
        |___A.nii.gz / A.nii
        |___B.nii.gz / B.nii
        |___C.nii.gz / C.nii
        |___ ... ...
        |___N.nii.gz / N.nii

    [B] generated_image_path
        |___A.nii.gz / A.nii
        |___B.nii.gz / B.nii
        |___C.nii.gz / C.nii
        |___ ... ...
        |___N.nii.gz / N.nii
    """
    # args definition
    parser = argparse.ArgumentParser()
    parser.add_argument('-out_results_dir', type=str, default='./logs', help='the log dir for evaluation.')
    parser.add_argument('-methodname', type=str, default='GenPET', help='the methodname.')
    parser.add_argument('-data_range', type=float, default=2.6, help='the data range for generated nii images. [!the minimum value is 0]')
    parser.add_argument('-window_size', type=int, default=11, help='the SSIM evaluation window size.')
    parser.add_argument('-real_image_path', type=str, default='/public/home/chenhui/Radio/NEW_BL/MRI/0_MRI_NII',
                        help='your real path.')
    parser.add_argument('-generated_image_path', type=str, default='/public/home/chenhui/Radio/NEW_BL/MRI/1_After_Freesurfer',
                        help='your generated path.')
    args = parser.parse_args()

    # logger establish and examine the out path
    if not os.path.exists(args.logdir):
        os.makedirs(args.logdir)
    trace = logger.add(os.path.join(args.logdir, datetime.now().strftime("%Y-%m-%d  %H:%M:%S") + '.log'))

    #evaluate the generated performance
    evaluate_single_type(args.real_image_path,
                         args.generated_image_path,
                         args.log_dir, args.methodname,
                         data_range=args.data_range, window_size=args.window_size)

