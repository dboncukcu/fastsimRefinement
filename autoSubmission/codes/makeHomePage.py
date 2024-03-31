import argparse
import os
from datetime import datetime
def create_status_badge(status):
    """Duruma göre Bootstrap badge'lerini oluştur."""
    if status.lower() == 'training':
        return '<span class="badge badge-pill badge-primary">Training</span>'
    elif status.lower() == 'plotting':
        return '<span class="badge badge-pill badge-warning">Plotting</span>'
    elif status.lower() == 'completed':
        return '<span class="badge badge-pill badge-success">Completed</span>'
    elif status.lower() == 'prepared':
        return '<span class="badge badge-pill badge-info">Prepared</span>'
    return '<span class="badge badge-pill badge-danger">Unknown</span>'

def create_detail_column(status, training_name, plot_text=None, epoch=None, max_epoch=None):
    """Duruma göre detay sütunu içeriğini oluştur."""
    if status.lower() == 'training' and epoch is not None and max_epoch is not None:
        progress_percentage = (epoch / max_epoch) * 100
        return (f'<div class="progress" style="width:100%; height: 100%;">'
                f'<div class="progress-bar bg-info" role="progressbar" style="width: {progress_percentage}%; color: black; font-weight: bold;" '
                f'aria-valuenow="{epoch}" aria-valuemin="0" aria-valuemax="{max_epoch}">'
                f'{epoch}/{max_epoch}</div></div>')
    elif status.lower() == 'plotting':
        plot_text_display = f'<span style="margin-left: 10px;">{plot_text}</span>' if plot_text else ''
        return f'<div class="spinner-border text-warning" role="status"></div>{plot_text_display}'
    elif status.lower() == 'completed':
        return f'<a href="{training_name}/" target="_blank" class="btn btn-success"><i class="fas fa-file"></i> Open</a>'
    elif status.lower() == 'prepared':
        return f'All Necessary Files Prepared.'
    return 'N/A'

def update_html(training_name,index_path, status,plot_text=None, epoch=None, max_epoch=None, reset=False):
    html_file = index_path +'/index.html'
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if reset:
        with open(html_file, 'w') as f:
            f.write('')
        return

    if not os.path.exists(html_file) or os.path.getsize(html_file) == 0:
        with open(html_file, 'w') as f:
            header = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
                      '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                      '<title>Training Status</title>\n'
                      '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">\n'
                      '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.2/css/all.css">\n'
                      '</head>\n<body>\n'
                      '<div class="container">\n'
                      '<button onclick="location.reload();" class="btn btn-primary" style="position: absolute; right: 10px; top: 10px;">Refresh</button>\n'
                      '<table class="table">\n'
                      '<thead class="thead-light"><tr><th>Training Name</th><th>Status</th><th>Detail</th><th>Updated Date</th></tr></thead>\n<tbody>\n')
            f.write(header)

    with open(html_file, 'r') as f:
        lines = f.readlines()

    tbody_start, tbody_end = None, None
    for i, line in enumerate(lines):
        if '<tbody>' in line:
            tbody_start = i
        elif '</tbody>' in line:
            tbody_end = i

    table_row_class = 'table-active' if status == 'Training' else ''
    new_entry = (f'<tr class="{table_row_class}"><td>{training_name}</td><td>{create_status_badge(status)}</td>'
                 f'<td>{create_detail_column(status, training_name, plot_text, epoch, max_epoch)}</td><td>{now}</td></tr>\n')

    existing_entry_indices = [i for i, line in enumerate(lines[tbody_start+1:tbody_end], tbody_start+1) if training_name in line]

    if existing_entry_indices:
        lines[existing_entry_indices[0]] = new_entry  # Mevcut girdiyi güncelle
    else:
        lines.insert(tbody_start + 1, new_entry)  # Yeni girdiyi en üstte ekle

    with open(html_file, 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update or create training status HTML file with advanced features.')
    parser.add_argument('--trainingName', help='Unique name of the training session')
    parser.add_argument('--status', help='Current status of the training')
    parser.add_argument('--plot', help='Plot text for Plotting status, optional')
    parser.add_argument('--epoch', type=int, help='Current epoch, only for Training status')
    parser.add_argument('--maxEpoch', type=int, help='Maximum number of epochs, only for Training status')
    parser.add_argument('--reset', action='store_true', help='Reset the table, removing all entries')

    args = parser.parse_args()
    index_path = os.path.realpath(__file__)
    index_path = os.path.dirname(index_path)

    update_html(args.trainingName, index_path,args.status, args.plot, args.epoch, args.maxEpoch, args.reset)
    print("HTML file updated successfully.")