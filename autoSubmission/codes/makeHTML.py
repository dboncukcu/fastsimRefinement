import json
import os
from trainConfig import config

mainDir = config["outdir"] + config["trainingName"] + "/"
plot_categories = {
    'Weights': [],
    'Learning Curves': [],
    'Pareto': [],
    'Regression': [],
    'Regression Correlation Factors': [],
}

plots_dir = mainDir+'plots'
for plot_file in os.listdir(plots_dir):
    if plot_file.startswith('learningCurves'):
        plot_categories['Learning Curves'].append(plot_file)
    elif plot_file.startswith('pareto'):
        plot_categories['Pareto'].append(plot_file)
    elif plot_file.startswith('regression_1D'):
        plot_categories['Regression'].append(plot_file)
    elif plot_file.startswith('regression_correlationfactors'):
        plot_categories['Regression Correlation Factors'].append(plot_file)
    elif plot_file.startswith('weights'):
        plot_categories['Weights'].append(plot_file)

base_class = "badge badge-"
def generate_badge(transformer, tanhNorm, logBase):
    """Belirli bir transformer tipine göre HTML badge oluşturur."""
    if transformer == "tanh":
        badge_type = "warning"
        text = f"tanh{tanhNorm}"
    elif transformer == "log":
        badge_type = "primary"
        text = f"log{'' if logBase in [None, 1] else logBase}"
    elif transformer == "logit":
        badge_type = "success"
        text = "logit"
    else:
        badge_type = "danger"
        text = "No Transformer"
    return f'<span class="{base_class}{badge_type} badge-transformer">{text}</span>'

def generate_transformer_sequence(transformers, tanhNorm, logBase):
    """Belirli bir transformer dizisine göre uygun badge'leri oluşturur."""
    return ' → '.join(generate_badge(trans, tanhNorm, logBase) for trans in transformers) if transformers else "No Transformer"

# HTML içeriğini formatlama
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{trainingName}</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <style>
        body {{ padding-top: 20px; }}
        .container {{ max-width: 960px; }}
        .badge-transformer {{ margin-left: 5px; }}
        .test-mode {{ text-decoration: line-through; }}
        .row {{ margin-bottom: 20px; }}
        .col-md-6 {{ padding: 5px; }}
        #filesCard .table-responsive {{ 
            max-height: 400px; /* Örneğin maksimum yüksekliği 400px olarak ayarlayın */
            overflow-y: auto; /* Dikey kaydırma çubuğunu etkinleştirin */
        }}
        .plot-img {{
            cursor: pointer; /* İmleci el şekline getir */
        }}

        #zoomTooltip {{
            z-index: 1000; /* Diğer içeriklerin üzerinde görünmesini sağlar */
            pointer-events: none; /* İmlecin tooltip üzerindeyken "altındaki" öğeleri tıklanabilir yapar */
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="display-4 text-center mb-4">{trainingName}</h1>
        <div class="card mb-4">
            <div class="card-body">
                <p class="card-text">{description}</p>
            </div>
        </div>
        <div class="card mb-4">
            <div class="card-header">Model Information</div>
            <div class="table-responsive">
                <table class="table">{model_info_rows}</table>
            </div>
        </div>
        <div class="card mb-4">
            <div class="card-header">Model Inputs - Variables</div>
            <div class="table-responsive">
                <table class="table">
                    <thead class="thead-light">
                        <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Transformer Queue</th>
                        </tr>
                    </thead>
                    <tbody>
                        {variables_rows}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="row">
            <div class="col-md-8 pr-1">
                <div class="card mb-4">
                    <div class="card-header">Model Inputs - Parameters</div>
                    <div class="table-responsive">
                        <table class="table">
                            <thead class="thead-light">
                                <tr>
                                <th scope="col">Name</th>
                                <th scope="col">Transformer Queue</th>
                                </tr>
                            </thead>
                            <tbody>
                                {parameters_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="col-md-4 pl-1">
                <div class="card mb-4">
                    <div class="card-header">Model Inputs - Spectators</div>
                    <div class="card-body">
                        <ul>{spectators_list}</ul>
                    </div>
                </div>
            </dviv>
        </div>
        </div>        
        {plot_cards}
        <div class="card mb-4" id="filesCard">
            <div class="card-header">Files</div>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>File Name</th>
                            <th>Type</th>
                            <th>Download</th>
                        </tr>
                    </thead>
                    <tbody>
                        {files_rows}
                    </tbody>
                </table>
            </div>
        </div>
        </div>
        <!-- Modal -->
        <div class="modal fade" id="plotModal" tabindex="-1" role="dialog" aria-labelledby="plotModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="plotModalLabel">Plot Image</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <img src="" id="modalImg" class="img-fluid">
                    </div>
                    <div class="modal-footer">
                        <a href="#" id="downloadBtn" class="btn btn-success" download target="_blank">Download</a>
                    </div>
                </div>
            </div>
        </div>
        <div id="zoomTooltip" style="display: none; position: absolute; background-color: rgba(0, 0, 0, 0.7); color: white; padding: 5px; border-radius: 5px; font-size: 12px;">Click for Zoom</div>
        <script>
            $(document).ready(function(){{
                $('.plot-img').click(function(){{
                    var src = $(this).attr('src');
                    var title = $(this).closest('.card').find('.card-header').text(); // Resmin dosya adını al
                    $('#modalImg').attr('src', src);
                    $('#plotModalLabel').text(title); // Modal başlığını dosya adı ile güncelle
                    $('#downloadBtn').attr('href', src); // Download butonunun href'ini güncelle
                    $('#plotModal').modal('show');
                }});
            }});
            document.addEventListener('DOMContentLoaded', function() {{
                var tooltip = document.getElementById('zoomTooltip');
                var plotImages = document.querySelectorAll('.plot-img');

                plotImages.forEach(function(img) {{
                    img.addEventListener('mouseenter', function() {{
                        tooltip.style.display = 'block'; // Tooltip'i görünür yap
                    }});

                    img.addEventListener('mousemove', function(e) {{
                        tooltip.style.left = e.pageX + 10 + 'px'; // Tooltip'in konumunu güncelle
                        tooltip.style.top = e.pageY + 10 + 'px';
                    }});

                    img.addEventListener('mouseleave', function() {{
                        tooltip.style.display = 'none'; // Tooltip'i gizle
                    }});
                }});
            }});
        </script>

</body>
</html>"""

model_info_rows = ''.join(f"<tr><th scope='row' class='{'test-mode' if config.get('isTest', False) and key in ['nEpochs', 'batchSize', 'numBatches'] else ''}'>{key}</th><td class='{'test-mode' if config.get('isTest', False) and key in ['nEpochs', 'batchSize', 'numBatches'] else ''}'>{value if key != 'numBatches' else json.dumps(value)}</td></tr>"
                          for key, value in config.items() if key not in ['modelInput', 'trainingName', 'description'])

parameters_rows = ''.join(f"<tr><td>{name}</td><td>{generate_transformer_sequence(transformers, config['tanhNorm'], config['logBase'])}</td></tr>"
                          for name, transformers in config['modelInput']['parameters'])

variables_rows = ''.join(f"<tr><td>{name}</td><td>{generate_transformer_sequence(transformers, config['tanhNorm'], config['logBase'])}</td></tr>"
                         for name, transformers in config['modelInput']['variables'])

spectators_list = ''.join(f"<li>{spec}</li>" for spec in config['modelInput']['spectators'])

plot_cards_html = ""
for category, files in plot_categories.items():
    if files:
        plot_cards_html += f'<div class="card mb-4">\n'
        plot_cards_html += f'    <div class="card-header">{category}</div>\n'
        plot_cards_html += '    <div class="card-body">\n'
        plot_cards_html += '        <div class="row">\n'
        for file in files:
            plot_path = os.path.join(plots_dir, file)
            plot_cards_html += '            <div class="col-md-6">\n'
            plot_cards_html += f'                <div class="card">\n'
            plot_cards_html += f'                    <div class="card-header">{file}</div>\n'
            plot_cards_html += f'                    <img src="{"/".join(plots_dir.split("/")[-2:])}" class="img-fluid plot-img" alt="{file}">\n'
            plot_cards_html += '                </div>\n'
            plot_cards_html += '            </div>\n'
        plot_cards_html += '        </div>\n'
        plot_cards_html += '    </div>\n'
        plot_cards_html += '</div>\n'

files = [
    (f"{config['trainingName']}.pt", "Output"),
    (f"{config['trainingName']}.root", "Output"),
    (f"{config['trainingName']}_train.csv", "Output"),
    (f"{config['trainingName']}_validation.csv", "Output"),
    ("checkONNX.py", "Training Files"),
    ("convertONNX.py", "Training Files"),
    ("my_mdmm.py", "Training Files"),
    ("my_mmd.py", "Training Files"),
    ("my_modules.py", "Training Files"),
    ("train.py", "Training Files"),
    ("trainRegression_Jet.py", "Training Files"),
    ("CMS_lumi.py", "Visualization"),
    ("plotPareto.py", "Visualization"),
    ("plotRegressionCorrelationFactors.py", "Visualization"),
    ("plotting.py", "Visualization"),
    ("plotLearningCurves.py", "Visualization"),
    ("plotRegression1D.py", "Visualization"),
    ("plot.sh", "Visualization"),
    ("plotWeights.py", "Visualization"),
    ("tdrstyle.py", "Visualization"),
]
files_rows = ''.join(f"<tr><td>{name}</td><td>{file_type}</td><td><a href='{mainDir +('codes/' if file_type != 'Output' else '') + name}' target='_blank' class='btn btn-success'>Download</a></td></tr>"
                     for name, file_type in files)

html_content = html_template.format(
    trainingName=config['trainingName'],
    description=config['description'],
    model_info_rows=model_info_rows,
    parameters_rows=parameters_rows,
    variables_rows=variables_rows,
    spectators_list=spectators_list,
    plot_cards=plot_cards_html,
    files_rows=files_rows, 
)

with open(mainDir + 'index.html', 'w') as f:
    f.write(html_content)
print("index.html file is created.")