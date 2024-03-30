
    #!/bin/bash
    source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
    export PYTHONPATH=./site-packages:$PYTHONPATH
    mkdir /eos/user/d/dboncukc/fastsimTest/epoch1000_tanh800_logit_4/codes
    mkdir /eos/user/d/dboncukc/fastsimTest/epoch1000_tanh800_logit_4/plots
    cp *.py /eos/user/d/dboncukc/fastsimTest/epoch1000_tanh800_logit_4/codes/
    
    echo "Training..."
    python3 trainRegression_Jet.py
    
    echo "plotLearningCurves"
    python3 plotLearningCurves.py

    echo "plotWeights"
    python3 plotWeights.py


    echo "plotPareto"
    python3 plotPareto.py

    echo "plotRegression1D"
    python3 plotRegression1D.py

    echo "plotRegressionCorrelationFactors"
    python3 plotRegressionCorrelationFactors.py

    echo "All Done"
    
    