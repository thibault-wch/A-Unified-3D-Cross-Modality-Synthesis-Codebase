'''
purpose: Skullstrip all the MRIs.
Author: Chenhui Wang
Data: 27/11/2024
Software: Freesurfer
'''
import os
import subprocess
import time
import multiprocessing
from joblib import Parallel, delayed
import argparse
from datetime import datetime
from loguru import logger



def recon_all(original_path, out_path ,final_path ,filename,datatype,preprocess_step):
    """
    original_path: the original data path
    out_path :temporal FreeSurfered datapath
    final_path : final output datapath
    subjectid : finalid
    preprocess_step : [1] for recon-all 1-5 steps [2] for the copy operation
    datatype : nii /nii.gz
    """
    if datatype=='nii':
        subjectid =filename[:-4]
    else:
        subjectid =filename[:-7]

    cur_path = out_path + '/' + str(subjectid)
    if preprocess_step==1:
        cmd1 = "recon-all -i {}/{} -autorecon1 -subjid {}".format(original_path, filename, subjectid)
        cmd2 = "&&mri_convert {}/mri/brainmask.mgz {}/mri/brainmask.nii.gz".format(cur_path, cur_path)
        cmd =cmd1+cmd2
    else:
        cmd="cp {}/mri/brainmask.nii.gz {}/{}.nii.gz".format(cur_path ,final_path, subjectid)
    time_start_train = time.time()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        logger.info(line.decode('utf-8').strip("b'"))
        if line == b'' or subprocess.Popen.poll(p) == 0:
            p.stdout.close()
            break

    time_end_train = time.time()
    logger.info('totally train cost{:.2f}'.format(time_end_train - time_start_train))
    logger.info('subjectID {} is already skull stripping'.format(subjectid))


if __name__ == '__main__':
    """
    [A] original_path
        |___A.nii.gz / A.nii
        |___B.nii.gz / B.nii
        |___C.nii.gz / C.nii
        |___ ... ...
        |___N.nii.gz / N.nii
        
    [B] out_path
        |___A_subjectid
        |   |___mri---brainmask.mgz
        |   |___...
        |
        |___B_subjectid
        |   |___mri---brainmask.mgz
        |   |___...
        |
        |___C_subjectid
        |   |___mri---brainmask.mgz
        |   |___...
        |
        |___...
        |
        |___N_subjectid
            |___mri---brainmask.mgz
            |___...
        
    [C] final_path
        |___A.nii.gz / A.nii
        |___B.nii.gz / B.nii
        |___C.nii.gz / C.nii
        |___ ... ...
        |___N.nii.gz / N.nii
    """
    # args definition
    parser = argparse.ArgumentParser()
    parser.add_argument('-ncore', type=int, default=1,help='the total cores for multiprocess.')
    parser.add_argument('-log_dir',type=str,default='./logs',help='the log dir for MRI preprocess.')
    parser.add_argument('-datatype',type=str,default='nii',help='the data type for brain images [nii|nii.gz]')
    parser.add_argument('-original_path',type=str, default='/public/home/chenhui/Radio/NEW_BL/MRI/0_MRI_NII', help='the original data path.')
    parser.add_argument('-out_path',type=str, default='/public/home/chenhui/Radio/NEW_BL/MRI/1_After_Freesurfer',help='the tmp-freesurfer preprocessed path.')
    parser.add_argument('-final_path',type=str, default='/public/home/chenhui/Radio/NEW_BL/MRI/2_After_Final',help='the final path.')
    args = parser.parse_args()

    # logger establish and examine the out path
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    trace = logger.add(os.path.join(args.log_dir, datetime.now().strftime("%Y-%m-%d  %H:%M:%S") + '.log'))
    if not os.path.exists(args.out_path):
        os.makedirs(args.out_path)

    # preprocessed original path
    datalist = os.listdir(args.original_path)
    logger.info('{} files are conducted'.format(len(datalist)))

    # [preprocess step 1] Freesurfer preprocessing
    num_cores = multiprocessing.cpu_count()
    logger.info('{} ncores are simultaneously conducted.'.format(min(args.ncore, num_cores - 4)))
    Parallel(n_jobs=min(args.ncore, num_cores - 4), prefer='threads')(
        delayed(recon_all)(args.original_path,
                           args.out_path,
                           args.final_path,
                           item, args.datatype, 1) for item in datalist)

    logger.info("[Recon] completed all FreeSurfer preprocessing pipelines.")

    # [preprocess step 2] Copy all files
    Parallel(n_jobs=min(args.ncore, num_cores - 4), prefer='threads')(
        delayed(recon_all)(args.original_path,
                           args.out_path,
                           args.final_path,
                           item,args.datatype, 2) for item in datalist)
    logger.info("[Copy] completed all copy preprocessing pipelines.")

