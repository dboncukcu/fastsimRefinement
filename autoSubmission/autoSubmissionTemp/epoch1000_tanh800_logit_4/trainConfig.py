
config =  {
    "outdir" : "/eos/user/d/dboncukc/fastsimTest/",
    "trainingName": "epoch1000_tanh800_logit_4",
    "description": "epoch1000_tanh800_logit",
    "inputFile" : '/eos/cms/store/group/comm_fastsim/RefinementTraining/T1ttttRun3_CMSSW_13_0_13/mc_fullfast_T1tttt_JetsMuonsElectronsPhotonsTausEvents.root',
    "treeName": "tJet",
    "preSelection": "1",
    "isTest" : True,
    "nEpochs" : 1000, 
    "batchSize" : 2048,
    "numBatches" : [500, 100, 200],
    "logBase" : None,
    "tanhNorm" : 800,
    "modelInput" : {
        "parameters" : [('GenJet_pt', ['tanh', 'logit']), ('GenJet_eta', []), ('RecJet_hadronFlavour_FastSim', [])],
        "variables" : [('RecJet_pt_CLASS', ['tanh', 'logit']), ('RecJet_btagDeepFlavB_CLASS', ['logit']), ('RecJet_btagDeepFlavCvB_CLASS', ['logit']), ('RecJet_btagDeepFlavCvL_CLASS', ['logit']), ('RecJet_btagDeepFlavQG_CLASS', ['logit'])],
        "spectators" : ['GenJet_pt', 'GenJet_eta', 'GenJet_phi', 'GenJet_mass', 'GenJet_hadronFlavour', 'GenJet_partonFlavour']
    }
}
        