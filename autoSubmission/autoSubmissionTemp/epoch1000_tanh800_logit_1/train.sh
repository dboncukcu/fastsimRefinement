
    #!/bin/bash
    source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
    export PYTHONPATH=./site-packages:$PYTHONPATH
    cp autoSubmissionTemp/epoch1000_tanh800_logit_1//*.py /eos/user/d/dboncukc/fastsimTest/epoch1000_tanh800_logit_1/
    python trainRegression_Jet.py
    