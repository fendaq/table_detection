"""
All tesseract_ocr based table detection functions are included under a single class of module.

"""

import  pyocr
import pyocr.builders
from PIL import Image

from table_detection.utils.string_utils import strip_value

TODO: "Handle all possible exceptions"

class OCR(object):
    """
    Class for dealing with tesseract through pyocr.
    """
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

    def __split_by_distance(self, compared_list, distance, comparison_key_1, comparison_key_2):
        """
        Helper function for comparing succeeding items of a list based on keys.

        :param list compared_list: list of dicts
        :param int distance: expresses pixel interval between comparable items
        :param string comparison_key_1: is used to call dict item as key
        :param string comparison_key_2: is used to call dict item as key
        :return: dict
        :rtype: dict
        """
        result = []
        temp_list = [compared_list[0]]
        for item in compared_list[1:]:
            if item[comparison_key_1] - temp_list[-1][comparison_key_2] <= distance:
                temp_list.append(item)
            else:
                result.append(temp_list)
                temp_list = []
                temp_list.append(item)
        result.append(temp_list)
        return result

    def get_ocr_data(self):
        zipped = zip([strip_value(i.content)
                      for i in self.word_boxes], [i.position for i in self.word_boxes])
        data = sorted([dict(ocr_text=j[0], x_left=j[1][0][0], y_top=j[1][0][1], x_right=j[1][1][0],
                      y_bottom=j[1][1][1]) for j in zipped], key=lambda x: x['y_bottom'])
        return list(filter(lambda x: len(x['ocr_text']) > 1, data))


    def get_rows(self, row_diff=13):
        words = self.get_ocr_data()
        result = self.__split_by_distance(words, row_diff, 'y_bottom', 'y_bottom')
        sorted_result = [sorted(row, key=lambda x: x['x_left']) for row in result]
        return sorted_result

    def split_row_to_columns(self, row, column_diff=25):
        return self.__split_by_distance(row, column_diff, 'x_left', 'x_right')

    def get_tables(self, diff=5):
        rows = self.get_rows()
        grid_items= list(filter(lambda x: len(x) > 1,
                                [self.split_row_to_columns(row) for row in rows]))
        tables = []
        print(grid_items)
        table = [grid_items[0]]
        for row in grid_items[1:]:
            if abs(row[1][-1]['x_right'] - table[-1][1][-1]['x_right']) <= diff:
                table.append(row)
            else:
                tables.append(table)
                table = [row]
        return tables



if __name__ == '__main__':
    path = '/home/anus/Desktop/image_files/balance_sheet_sample_bmp.bmp'
    ocr = OCR(path)
    # print(ocr.get_ocr_data())
    for item in ocr.get_tables()[0]:
        print(item)
    # for item in ocr.get_tables():
    #     print(item)
    # text = ''
    # for item in ocr.get_rows():
    #     for i in item:
    #         text+=i['ocr_text'] + ' '
    #     print(text)
    #     text = ''
    # print(text)
    # print(len(ocr.get_rows()))
    # list = ocr.get_rows()[6]
    # print(ocr.split_row_to_columns(list))
    # print(len(ocr.split_row_to_columns(list)), print(len(list)))






