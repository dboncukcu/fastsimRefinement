import shutil
import os
import subprocess

def printc(text, **kwargs):
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "black": "\033[30m",
    }
    background_colors = {
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
        "bg_magenta": "\033[45m",
        "bg_cyan": "\033[46m",
        "bg_white": "\033[47m",
        "bg_black": "\033[40m",
    }
    styles = {
        "bold": "\033[1m",
        "italic": "\033[3m",
        "underline": "\033[4m",
    }
    reset = "\033[0m"
    
    # Stil işlemleri
    for style in styles:
        start_tag = f"<{style}>"
        end_tag = f"</{style}>"
        if start_tag in text and end_tag in text:
            text = text.replace(start_tag, styles[style]).replace(end_tag, reset)
    
    # Renk işlemi
    for color in colors:
        start_tag = f"<{color}>"
        end_tag = f"</{color}>"
        if start_tag in text and end_tag in text:
            text = text.replace(start_tag, colors[color]).replace(end_tag, reset)

    # Arka plan renk işlemi
    for bg_color in background_colors:
        start_tag = f"<{bg_color}>"
        end_tag = f"</{bg_color}>"
        if start_tag in text and end_tag in text:
            text = text.replace(start_tag, background_colors[bg_color]).replace(end_tag, reset)
    
    print(text, **kwargs)
    
def log(message, message_type="raw",**kwargs):
    message_formats = {
        "raw" : "{}",
        "info": "<blue><bold>{}</bold></blue>",
        "warning": "<yellow><bold>{}</bold></yellow>",
        "primary": "<cyan><bold>{}</bold></cyan>",
        "error": "<red><bold>{}</bold></red>",
        "error_bg" : "<bg_red><white><bold>{}</bold></white></bg_red>",
        "success": "<green><bold>{}</bold></green>",
        "success_bg" : "<bg_green><black><bold>{}</bold></black></bg_green>",
        "debug": "<magenta><bold>{}</bold></magenta>",
    }
    
    # Mesaj tipine göre formatı seç ve printc fonksiyonu ile yazdır
    if message_type in message_formats:
        formatted_message = message_formats[message_type].format(message)
        printc(formatted_message,**kwargs)
    else:
        printc(message,**kwargs)
        


def cp(source, destination):
    if isinstance(source, str):
        source = [source]
    log("*"*50,message_type="debug")
    destination_paths = []
    for src in source:
        source_path = os.path.abspath(src)
        destination_path = os.path.join(os.path.abspath(destination), os.path.basename(src))
        shutil.copy(source_path, destination_path)
        destination_paths.append(destination_path)
        log(f"'{src}' -> '{destination_path}' copied.",message_type="success")
    log("*"*50,message_type="debug")
    return destination_paths


def create_submission_file(executableFile, tempTrainDir, inputFiles,jobFlavour, requestGPUs):
    
    template = """
    universe   = vanilla
    executable = $executableFile$
    output     = $tempTrainDir$output/output.out
    error      = $tempTrainDir$output/error.err
    log        = $tempTrainDir$output/log.log

    MY.WantOS = "el7"
    +JobFlavour = "$jobFlavour$"
    request_gpus            = $requestGPUs$
    should_transfer_files = YES
    transfer_input_files = $inputFiles$
    arguments = $(Cluster) $(Process)
    queue
    """
    
    template = template.replace("$executableFile$", executableFile)
    template = template.replace("$tempTrainDir$", tempTrainDir)
    template = template.replace("$jobFlavour$", jobFlavour)
    template = template.replace("$inputFiles$", ", ".join(inputFiles))
    template = template.replace("$requestGPUs$", str(requestGPUs))
    file_path = tempTrainDir + "start_train.sub"
    with open(file_path, "w") as file:
        file.write(template)
        log("Submission file created -> " + file_path, message_type="success")
        
def create_executable_file(tempTrainDir,training_outdir,outdir,trainingName):
    template = """
    #!/bin/bash
    source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
    export PYTHONPATH=./site-packages:$PYTHONPATH
    mkdir $training_outdir$/codes
    mkdir $training_outdir$/plots
    cp *.py $training_outdir$/codes/
    
    python3 $outdir$makeHomePage.py --trainingName $trainingName$ --status Prepared
    echo "Training..."
    python3 trainRegression_Jet.py
    
    python3 $outdir$makeHomePage.py --trainingName $trainingName$ --status Plotting --plot "Learning Curves"
    echo "plotLearningCurves"
    python3 plotLearningCurves.py
    python3 $outdir$makeHomePage.py --trainingName $trainingName$ --status Plotting --plot "Weights"
    echo "plotWeights"
    python3 plotWeights.py

    python3 $outdir$makeHomePage.py --trainingName $trainingName$ --status Plotting --plot "Pareto"
    echo "plotPareto"
    python3 plotPareto.py

    python3 $outdir$makeHomePage.py --trainingName $trainingName$ --status Plotting --plot "Regression 1D"
    echo "plotRegression1D"
    python3 plotRegression1D.py

    python3 $outdir$makeHomePage.py --trainingName $trainingName$ --status Plotting --plot "Regression Correlation Factors"
    echo "plotRegressionCorrelationFactors"
    python3 plotRegressionCorrelationFactors.py

    echo "All Plots Done"
    
    python3 $training_outdir$/codes/makeHTML.py
    
    python3 $outdir$makeHomePage.py --trainingName $trainingName$ --status Completed
    echo "train.sh executed successfully!"
    """
    template = template.replace("$tempTrainDir$", tempTrainDir)
    template = template.replace("$training_outdir$", training_outdir)
    template = template.replace("$outdir$", outdir)
    template = template.replace("$trainingName$", trainingName)
    file_path = tempTrainDir + "train.sh"
    with open(file_path, "w") as file:
        file.write(template)
        log("Executable file created -> " + file_path, message_type="success")
        
def create_config_file(tempTrainDir, training_config):
    template = """
config =  {
    "outdir" : "$outdir$",
    "trainingName": "$trainingName$",
    "description": "$description$",
    "inputFile" : '$inputFile$',
    "treeName": "$treeName$",
    "preSelection": "$preSelection$",
    "isTest" : $isTest$,
    "nEpochs" : $nEpochs$, 
    "batchSize" : $batchSize$,
    "numBatches" : $numBatches$,
    "logBase" : $logBase$,
    "tanhNorm" : $tanhNorm$,
    "modelInput" : {
        "parameters" : $parameters$,
        "variables" : $variables$,
        "spectators" : $spectators$
    }
}
        """
    template = template.replace("$outdir$", training_config["outdir"])
    template = template.replace("$trainingName$", training_config["trainingName"])
    template = template.replace("$description$", training_config["description"])
    template = template.replace("$jobFlavour$", training_config["jobFlavour"])
    template = template.replace("$isTest$", str(training_config["isTest"]))
    template = template.replace("$nEpochs$", str(training_config["nEpochs"]))
    template = template.replace("$batchSize$", str(training_config["batchSize"]))
    template = template.replace("$numBatches$", str(training_config["numBatches"]))
    template = template.replace("$logBase$", str(training_config["logBase"]))
    template = template.replace("$tanhNorm$", str(training_config["tanhNorm"]))
    template = template.replace("$parameters$", str(training_config["modelInput"]["parameters"]))
    template = template.replace("$variables$", str(training_config["modelInput"]["variables"]))
    template = template.replace("$spectators$", str(training_config["modelInput"]["spectators"]))
    template = template.replace("$inputFile$", training_config["inputFile"])
    template = template.replace("$treeName$", training_config["treeName"])
    template = template.replace("$preSelection$", training_config["preSelection"])
    
    file_path = tempTrainDir + "trainConfig.py"
    with open(file_path, "w") as file:
        file.write(template)
        log("Train Config file created -> " + file_path , message_type="success")

def condor_submit(tempTrainDir,outdir,trainingName):
    
    process = subprocess.run(["python3", f"{outdir}makeHomePage.py", "--trainingName", trainingName, "--status", "idle"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(process.stdout,process.stderr) 
    command = ["condor_submit", tempTrainDir + "start_train.sub"]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode == 0:
        log("Job has been succesfully submitted:\n", message_type="success_bg")
        log(process.stdout)
    else:
        log("An error has been accured:\n", message_type="error_bg")
        log(process.stderr)