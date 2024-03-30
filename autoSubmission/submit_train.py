

training_config = {
    "outdir" : "/eos/user/d/dboncukc/fastsimTest/", #"/eos/user/d/dboncukc/fastsim/",
    "trainingName": "epoch1000_tanh800_logit",
    "description": "epoch1000_tanh800_logit",
    "inputFile" : '/eos/cms/store/group/comm_fastsim/RefinementTraining/T1ttttRun3_CMSSW_13_0_13/mc_fullfast_T1tttt_JetsMuonsElectronsPhotonsTausEvents.root',
    "treeName": "tJet",
    "preSelection": "1",
    "jobFlavour" : "espresso",
    "requestGPUs" : 1,
    "isTest" : True,
    # if not isTest, the following parameters are used
    "nEpochs" : 1000, 
    "batchSize" : 2048,
    "numBatches" : [500, 100, 200], # [train, val, test]
    "logBase" : None,
    "tanhNorm" : 800,
    "modelInput" : {
        "parameters" : [
            ('GenJet_pt', ['tanh', 'logit']),
            ('GenJet_eta', []),
            ('RecJet_hadronFlavour_FastSim', [])
        ],
        "variables" : [
            ('RecJet_pt_CLASS', ['tanh200','logit']),
            ('RecJet_btagDeepFlavB_CLASS', ['logit']),
            ('RecJet_btagDeepFlavCvB_CLASS', ['logit']),
            ('RecJet_btagDeepFlavCvL_CLASS', ['logit']),
            ('RecJet_btagDeepFlavQG_CLASS', ['logit'])
        ],
        "spectators" : [     
            'GenJet_pt',
            'GenJet_eta',
            'GenJet_phi',
            'GenJet_mass',
            'GenJet_hadronFlavour',
            'GenJet_partonFlavour',
        ]
    }
}


training_files = [
    "./codes/checkONNX.py",
    "./codes/convertONNX.py",
    "./codes/my_mdmm.py",
    "./codes/my_mmd.py",
    "./codes/my_modules.py",
    "./codes/trainRegression_Jet.py",
    "./codes/visualization/plotting.py",
    "./codes/visualization/CMS_lumi.py",
    "./codes/visualization/plotLearningCurves.py",
    "./codes/visualization/plotPareto.py",
    "./codes/visualization/plotRegression1D.py",
    "./codes/visualization/plotRegressionCorrelationFactors.py",
    "./codes/visualization/plotWeights.py",
    "./codes/visualization/tdrstyle.py",
]

from utils import *
import os

# create temp directory

temp_directory = "autoSubmissionTemp/"

training_outdir = training_config["outdir"] + training_config["trainingName"]

log("_"*50,message_type="debug") # create main temp directory
if not os.path.exists(temp_directory):
    log("No temp directory found, creating one", message_type="warning")
    os.makedirs(temp_directory)
else:
    log("Temp directory found", message_type="success")
log("_"*50,message_type="debug") # create training output directory
if os.path.exists(training_outdir):
    log("Training output directory already exists, creating new one\nSearching possible directory:", message_type="warning")
    counter = 1
    new_folder_path = f"{training_outdir}_{counter}"
    log(f"Trying {new_folder_path}:", end=" ", message_type="primary")
    while os.path.exists(new_folder_path):
        log("exists", message_type="error_bg")
        counter += 1
        new_folder_path = f"{training_outdir}_{counter}"
        log(f"Trying {new_folder_path}:", end=" ", message_type="primary")
    log("does not exist",message_type="success_bg")
    log(f"Created {new_folder_path}", message_type="success")
    os.makedirs(new_folder_path)
    training_outdir = new_folder_path + "/"
    training_temp_dir = temp_directory + new_folder_path.split("/")[-1] + "/"
    training_config["trainingName"] = new_folder_path.split("/")[-1]    
else:
    log("Created training output directory, " + training_outdir, message_type="success")
    os.makedirs(training_outdir)
    training_temp_dir = temp_directory + training_outdir.split("/")[-1] + "/"
    
    
log("_"*50,message_type="debug") # create training temp directory
if not os.path.exists(training_temp_dir):
    log("Created training temp directory, "+ training_temp_dir, message_type="success")
    os.makedirs(training_temp_dir)
    os.makedirs(training_temp_dir + "/output")
log("_"*50,message_type="debug") # copy files to training temp directory
temp_copied_files_paths = cp(training_files, training_temp_dir)
temp_copied_files_paths.append(training_temp_dir + "trainConfig.py")
log("_"*50,message_type="debug") # create submission file
create_submission_file(training_temp_dir + "train.sh", training_temp_dir, temp_copied_files_paths, training_config["jobFlavour"],training_config["requestGPUs"])
log("_"*50,message_type="debug") # create executable file
create_executable_file(training_temp_dir,training_outdir)
log("_"*50,message_type="debug") # create config file for training
create_config_file(training_temp_dir, training_config)
log("_"*50,message_type="debug") # submit job
condor_submit(training_temp_dir)
log("_"*50,message_type="debug")
