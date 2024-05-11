import os
import subprocess
import time
import multiprocessing
from joblib import Parallel, delayed
import argparse
from datetime import datetime
from loguru import logger



def registration(original_path, out_path,filename,datatype):
    '''
    original_path: the original data path
    out_path :temporal FreeSurfered datapath
    final_path : final output datapath
    subjectid : finalid
    preprocess_step : [1] for recon-all 1-5 steps [2] for the copy operation
    datatype : nii /nii.gz
    '''
    if datatype=='nii':
        subjectid =filename[:-4]
    else:
        subjectid =filename[:-7]
    template_file = "MNI152_T1_1mm_brain.nii.gz"
    cmd = "flirt -ref {} -in {}/{}  -out {}/{}".format(template_file, original_path,filename, out_path,filename)


    time_start_train = time.time()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        logger.info(line.decode('gbk').strip("b'"))
        if line == b'' or subprocess.Popen.poll(p) == 0:
            p.stdout.close()
            break
    time_end_train = time.time()
    logger.info('totally train cost{:.2f}'.format(time_end_train - time_start_train))
    logger.info('subjectID {} is already registrating'.format(subjectid))


if __name__ == '__main__':

    """
    [A] original_path
        |___A.nii.gz / A.nii
        |___B.nii.gz / B.nii
        |___C.nii.gz / C.nii
        |___ ... ...
        |___N.nii.gz / N.nii
        
    [B] out_path
        |___A.nii.gz / A.nii
        |___B.nii.gz / B.nii
        |___C.nii.gz / C.nii
        |___ ... ...
        |___N.nii.gz / N.nii
    """
    # args definition
    parser = argparse.ArgumentParser()
    parser.add_argument('-ncore', type=int, default=1, help='the total cores for multiprocess.')
    parser.add_argument('-log_dir', type=str, default='./logs', help='the log dir for MRI preprocess.')
    parser.add_argument('-datatype', type=str, default='nii', help='the data type for brain images [nii|nii.gz]')
    parser.add_argument('-original_path', type=str, default='/public/home/chenhui/Radio/NEW_BL/MRI/0_MRI_NII',
                        help='the original data path.')
    parser.add_argument('-out_path', type=str, default='/public/home/chenhui/Radio/NEW_BL/MRI/1_After_Freesurfer',
                        help='the tmp-freesurfer preprocessed path.')
    args = parser.parse_args()

    # logger establish and examine the out path
    if not os.path.exists(args.logdir):
        os.makedirs(args.logdir)
    trace = logger.add(os.path.join(args.logdir, datetime.now().strftime("%Y-%m-%d  %H:%M:%S") + '.log'))
    if not os.path.exists(args.out_path):
        os.makedirs(args.out_path)

    # preprocessed original path
    datalist = os.listdir(args.original_path)
    logger.info('{} files are conducted'.format(len(datalist)))

    # [preprocess step 1] Freesurfer preprocessing
    num_cores = multiprocessing.cpu_count()
    logger.info('{} ncores are simultaneously conducted.'.format(min(args.ncore, num_cores - 4)))
    Parallel(n_jobs=min(args.ncore, num_cores - 4), prefer='threads')(
        delayed(registration)(args.original_path,
                           args.out_path,
                           item, args.datatype) for item in datalist)

    logger.info("[Flirt] completed all Flirt preprocessing pipelines.")
