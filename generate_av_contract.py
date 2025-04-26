import sys
import csv
import os
import base64

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

EXPORT_FOLDER = 'exported'
TEMPLATE_PATH = 'templates/AV新法契約書.j2'


def image_to_base64(image_path: str):
    with open(image_path, mode='rb') as img_file:
        encoded_bytes = base64.b64encode(img_file.read())
        encoded_str = encoded_bytes.decode('utf-8')
        # 拡張子に応じてMIMEタイプを決める
        if image_path.lower().endswith(".png"):
            mime_type = "image/png"
        elif image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif image_path.lower().endswith(".gif"):
            mime_type = "image/gif"
        else:
            raise ValueError("Unsupported image format")

        return f"data:{mime_type};base64,{encoded_str}"


def main():
    if len(sys.argv) != 2:
        print('CSVファイルを指定してください')
        sys.exit(1)

    csv_file_name = sys.argv[1]
    print(f'{csv_file_name=}')
    with open(csv_file_name, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            pdf_file_name = f'AV新法契約書_{row["撮影年"]}{int(row["撮影月"]):02}{int(row["撮影日"]):02}_{row["作品名"]}.pdf'

            if os.path.exists(f'{EXPORT_FOLDER}/{pdf_file_name}'):
                print(f'{pdf_file_name} is already exported')
                continue
            for key in ['宣伝顔出し可', '宣伝声出し可', '作品顔出し可', '作品声出し可']:
                row[key] = row[key].strip().lower() == 'true'

            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template(TEMPLATE_PATH)

            rendered_text = template.render(row)

            HTML(string=rendered_text, base_url='.').write_pdf(f'{EXPORT_FOLDER}/{pdf_file_name}')

            print(f'exported {pdf_file_name}')


if __name__ == "__main__":
    main()
