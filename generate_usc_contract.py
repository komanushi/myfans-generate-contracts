import sys
import csv
import os
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

EXPORT_FOLDER = 'exported'
TEMPLATE_PATH = 'templates/USC2257契約書.j2'


def main():
    if len(sys.argv) != 2:
        print('CSVファイルを指定してください')
        sys.exit(1)

    csv_file_name = sys.argv[1]
    print(f'{csv_file_name=}')
    with open(csv_file_name, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            pdf_file_name = f'usc2257_{row["宣誓日"]}_{row["出演者本名"]}.pdf'

            if os.path.exists(f'{EXPORT_FOLDER}/{pdf_file_name}'):
                print(f'{pdf_file_name} is already exported')
                continue

            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template(TEMPLATE_PATH)

            rendered_text = template.render(row)

            HTML(string=rendered_text).write_pdf(f'{EXPORT_FOLDER}/{pdf_file_name}')
            print(f'exported {pdf_file_name}')


if __name__ == "__main__":
    main()
