import subprocess
import os


def convert_pdf_to_images(input_pdf_path, output_folder_path):
    converter_path = '/home/ashkhen/Projects/table_detection/script'
    subprocess.call('java -jar "{}/pdf-local-converter-1.0.0-jar-with-dependencies.jar" "{}" '
                    '"{}" 300'.format(converter_path, input_pdf_path, output_folder_path), shell=True)


if __name__== '__main__':
    convert_pdf_to_images('/home/ashkhen/Projects/table_detection/data/pdf_files/PLR_Provide_Gems_2017_08_01.pdf',
                          '/home/ashkhen/Projects/table_detection/data/image_files')
