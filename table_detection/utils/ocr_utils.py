import pyocr
from PIL import Image


def get_ocr_data(image_path):
    tools = pyocr.get_available_tools()
    tool = tools[0]
    word_boxes = tool.image_to_string(
        Image.open(image_path),
        lang="eng",
        builder=pyocr.builders.WordBoxBuilder()
    )
    zipped = zip([i.content for i in word_boxes], [i.position for i in word_boxes])
    data = sorted([dict(ocr_text=j[0], x_left=j[1][0][0], y_top=j[1][0][1], x_right=j[1][1][0],
                   y_bottom=j[1][1][1]) for j in zipped], key=lambda x: x['y_bottom'])
    return data


def detect_rows(image_path, threshold=15):
    rows = []
    words = get_ocr_data(image_path)
    row = []
    for index in range(len(words)-1):
        if not row:
            row.append(words[index])
        if words[index+1]['y_bottom'] - row[-1]['y_bottom'] <= threshold:
            row.append(words[index+1])
        else:
            if index!= len(row) - 2:
                rows.append(sorted(row, key=lambda x: x['x_left']))
                row = []
            else:
                rows.append(sorted(row, key=lambda x: x['x_left']))
                row = words[index + 1]
    rows.append(sorted(row, key=lambda x: x['x_left']))
    return rows


def split_row_to_columns(row, threshold=25):
    columns = []
    column = []
    for index in range(len(row)-1):
        if not column:
            column.append(row[index])
        if row[index + 1]['x_left'] - column[-1]['x_right'] <= threshold:
            column.append(row[index + 1])
        else:
            if index != len(row) - 2:
                columns.append(column)
                column = []
            else:
                columns.append(column)
                column = [row[index + 1]]
    columns.append(column)
    return columns


def get_tables(data_list, thresh=5):
    """
    if at least 3 succeeding  rows have  columns  with the same x coordinates,the group of
    those rows is considered to be table.

    """
    data_list = list(filter(lambda x: len(x) >= 2, data_list))
    print(len(data_list))
    tables = []
    table = [data_list[0]]
    print(table)
    for raw in data_list[1:]:
        if abs(raw[1][-1]['x_right']-table[1][-1]['x_right']) <= 5:
                table.append(raw)
        else:
            tables.append(table)
            table.append(raw)
    tables.append(table)
    return tables







if __name__== '__main__':
    all_rows = detect_rows('/home/ashkhen/Projects/table_detection/data/image_files/004.jpg')
    column_and_rows = [split_row_to_columns(row) for row in all_rows]
    # rows_with_multi_columns = list(filter(lambda x: len(x)>=2,column_and_rows ))
    # for row in rows_with_multi_columns:
    #     print(len(row))
    # print(rows_with_multi_columns)
    # for row in column_and_rows:
    #     if len(row) < 2:
    #         del row
    # print(column_and_rows)
    tables_list = get_tables(column_and_rows)
    print(tables_list)

    # for i in detect_rows('/home/ashkhen/Projects/table_detection/data/image_files/004.jpg'):
    #     print (i)
    # for i in get_ocr_data('/home/ashkhen/Projects/table_detection/data/image_files/002.jpg'):
    #     print (i)
    # row = [{'ocr_text': 'Prepaid', 'x_right': 194, 'y_bottom': 352, 'y_top': 333, 'x_left': 132},
    #        {'ocr_text': 'expenses', 'x_right': 272, 'y_bottom': 352, 'y_top': 338, 'x_left': 200},
    #        {'ocr_text': '64,533', 'x_right': 1119, 'y_bottom': 353, 'y_top': 338, 'x_left': 1065}]
    # row = [{'x_right': 1232, 'ocr_text': 'A+', 'y_bottom': 446, 'y_top': 423, 'x_left': 1194}, {'x_right': 1500, 'ocr_text': 'A', 'y_bottom': 446, 'y_top': 423, 'x_left': 1479}, {'x_right': 1848, 'ocr_text': 'B', 'y_bottom': 446, 'y_top': 423, 'x_left': 1830}, {'x_right': 2393, 'ocr_text': 'D', 'y_bottom': 446, 'y_top': 423, 'x_left': 2374}, {'x_right': 2707, 'ocr_text': 'E', 'y_bottom': 446, 'y_top': 423, 'x_left': 2690}, {'x_right': 327, 'ocr_text': 'Class', 'y_bottom': 447, 'y_top': 423, 'x_left': 245}, {'x_right': 2122, 'ocr_text': 'C', 'y_bottom': 447, 'y_top': 423, 'x_left': 2102}]
    # row = sorted(row, key=lambda x: x['x_left'])
    # row = [{'y_top': 114, 'y_bottom': 174, 'ocr_text': 'Principal', 'x_left': 1006, 'x_right': 1266}, {'y_top': 114, 'y_bottom': 162, 'ocr_text': 'and', 'x_left': 1289, 'x_right': 1397}, {'y_top': 114, 'y_bottom': 162, 'ocr_text': 'Interest', 'x_left': 1422, 'x_right': 1646}, {'y_top': 113, 'y_bottom': 174, 'ocr_text': 'Summary', 'x_left': 1668, 'x_right': 1954}]
    # print(split_row_to_columns(row))
    # for i in detect_rows('/home/ashkhen/Projects/table_detection/data/image_files/004.jpg'):
    #     print (split_row_to_columns(i))


