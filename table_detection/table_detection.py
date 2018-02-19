import cv2
import pytesseract, pyocr
import pyocr.builders
from PIL import Image
import numpy as np


class OCR(object):
    tools = pyocr.get_available_tools()
    tool = tools[0]
    lang = 'eng'

    def __init__(self, img):
        self.img = img
        self.word_boxes = self.tool.image_to_string(
            Image.open(self.img),
            lang=self.lang,
            builder=pyocr.builders.WordBoxBuilder()
        )
    @staticmethod
    def split_by_distance(compared_list, comparison_key, distance):
        result = list()
        temp_list = [compared_list[0]]
        for item in compared_list[1:]:
            if item[comparison_key] - temp_list[-1][comparison_key] <= distance:
                temp_list.append(item)
            else:
                result.append(temp_list)
                temp_list = [item]
        result.append(temp_list)
        return result

    def get_ocr_data(self):
        zipped = zip([i.content for i in self.word_boxes], [i.position for i in self.word_boxes])
        data = sorted([dict(ocr_text=j[0], x_left=j[1][0][0], y_top=j[1][0][1], x_right=j[1][1][0],
                        y_bottom=j[1][1][1]) for j in zipped], key=lambda x: x['y_bottom'])
        return data

    def get_rows(self, row_diff=15):
        words = self.get_ocr_data()
        result = self.split_by_distance(words, 'y_bottom', row_diff)
        return result


        # rows.append(sorted(row, key=lambda x: x['x_left']))
        # return rows

    def split_row_to_columns(self, column_diff=25):
        columns = self.get_rows()[1]



# def get_rows(self, row_diff=15):
    #     words = self.get_ocr_data()
    #     rows = []
    #     row = []
    #     for i in range(len(words)-1):
    #         if not row:
    #             row.append(words[i])
    #         if words[i+1]['y_bottom'] - row[-1]['y_bottom'] <= row_diff:
    #             row.append(words[i+1])
    #         else:
    #             rows.append(sorted(row, key=lambda x: x['x_left']))
    #             if i != len(row)-2:
    #                 row = []
    #             else:
    #                 row = words[i+1]
    #     rows.append(sorted(row, key=lambda x: x['x_left']))
    #     return rows
    #
    # def split_row_to_columns(self, column_diff=25):
    #     rows = self.get_rows()[1]
    #     columns = []
    #     column = [rows[0]]
    #     for row in rows[1:]:
    #         if row['x_left'] - column[-1]['x_right'] <= column_diff:
    #             column.append(row)
    #         else:
    #             columns.append(column)
    #             column = list()
    #             column.append(row)
    #     columns.append(column)
    #     print(columns)



if __name__ == '__main__':
    path = '//home/anus/Projects/dl-table-detection/tests/test_resources/image_files/Strong_Oil_June_30_2012_Financials_4_600.jpg'
    ocr = OCR(path)
    for item in ocr.get_rows():
        print(item)




