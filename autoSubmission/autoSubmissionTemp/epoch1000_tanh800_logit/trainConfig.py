
config =  {
    "outdir" : "/eos/user/d/dboncukc/fastsimTest/epoch1000_tanh800_logit",
    "trainingName": "epoch1000_tanh800_logit",
    "description": "epoch1000_tanh800_logit",
    "jobFlavour" : "espresso",
    "isTest" : False,
    "nEpochs" : 1000, 
    "batchSize" : 2048,
    "numBatches" : [500, 100, 200],
    "logBase" : None,
    "tanhNorm" : 800,
    "modelInput" : {
        "parameters" : [('GenJet_pt', ['tanh200', 'logit']), ('GenJet_eta', []), ('RecJet_hadronFlavour_FastSim', [])],
        "variables" : [('RecJet_pt_CLASS', ['tanh200', 'logit']), ('RecJet_btagDeepFlavB_CLASS', ['logit']), ('RecJet_btagDeepFlavCvB_CLASS', ['logit']), ('RecJet_btagDeepFlavCvL_CLASS', ['logit']), ('RecJet_btagDeepFlavQG_CLASS', ['logit'])],
        "spectators" : ['GenJet_pt', 'GenJet_eta', 'GenJet_phi', 'GenJet_mass', 'GenJet_hadronFlavour', 'GenJet_partonFlavour']
    }
}
        