# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

SeqNameList = ['left_cam'];
# Result_root = '/mnt/DATA/tmp/NewCollege/LDSO_Debug/'
Result_root = '/mnt/DATA/tmp/NewCollege/LDSO_Mono_Baseline_v2/'

Number_GF_List =  [2000]; # [600, 800, 1000, 1500, 2000]; # 
# Number_GF_List =  [800, 1200, 2000, 3000, 4000, 5000]; # 

Num_Repeating = 10 # 20 # 1 # 
SleepTime = 3 # 10 # 25

#----------------------------------------------------------------------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ALERT = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for ri, num_gf in enumerate(Number_GF_List):
    
    Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

    for iteration in range(0, Num_Repeating):

        Experiment_dir = Result_root + Experiment_prefix + '_Round' + str(iteration + 1)
        cmd_mkdir = 'mkdir -p ' + Experiment_dir
        subprocess.call(cmd_mkdir, shell=True)

        for sn, sname in enumerate(SeqNameList):
            
            print bcolors.ALERT + "====================================================================" + bcolors.ENDC

            SeqName = SeqNameList[sn]
            print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName

            File_Calib = './NewCollege/NewCollege_Mono_calib.txt'
            File_Gamma = ' '
            File_Vignette = ' '
            Misc_Config = ' mode=1 nolog=1 quiet=1 nogui=1'

            Path_Image   = '/mnt/DATA/Datasets/New_College/Stereo_Images'
            File_traj = Experiment_dir + '/' + SeqName

            cmd_slam   = str('../bin/run_dso_newcollege files=' + Path_Image + ' calib=' + File_Calib + ' gamma=' + File_Gamma + ' vignette=' + File_Vignette + ' preset='  + str(int(num_gf)) + ' realtime=' + File_traj + Misc_Config)
            
            print bcolors.WARNING + "cmd_slam: \n"   + cmd_slam   + bcolors.ENDC

            print bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC
            # proc_slam = subprocess.Popen(cmd_slam, shell=True)
            proc_slam = subprocess.call(cmd_slam, shell=True)

            print bcolors.OKGREEN + "Wait for exporting results" + bcolors.ENDC
            time.sleep(SleepTime)

            print bcolors.OKGREEN + "Finished playback, kill the process" + bcolors.ENDC
            subprocess.call('pkill run_dso_newcollege', shell=True)

