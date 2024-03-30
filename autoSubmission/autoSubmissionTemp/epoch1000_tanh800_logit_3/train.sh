
    #!/bin/bash
    source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
    export PYTHONPATH=./site-packages:$PYTHONPATH
    cp autoSubmissionTemp/epoch1000_tanh800_logit_3/*.py /eos/user/d/dboncukc/fastsimTest/epoch1000_tanh800_logit_3/
    python3 trainRegression_Jet.py
    