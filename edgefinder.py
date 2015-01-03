__author__ = 'dasprunger'

import png
import sys

START_AT_ROW = 44
END_AT_ROW = 441
START_AT_COL = 19
END_AT_COL = 655
GRID_COLOR = 55

TRIGGER_R = 76
TRIGGER_G = 48
TRIGGER_B = 76


def find_horizontal_edges(filename):
    reader = png.Reader(filename=filename)
    data = reader.asDirect()

    # Figure out how many color entries there will be
    if data[3]['greyscale']:
        COLOR_FACTOR = 1
    else:
        COLOR_FACTOR = 3

    pixels = list(data[2])
    edge_matrix = []

    for row_index, row in enumerate(pixels):
        # Ignore rows outside the indicated range
        if START_AT_ROW < row_index <= END_AT_ROW:
            prev_row = pixels[row_index - 1]
            edge_row = [False for i in range(END_AT_COL - START_AT_COL + 1)]

            for col_index, col in enumerate(row):
                # Ignore columns outside the indicated range
                if START_AT_COL * COLOR_FACTOR <= col_index < (END_AT_COL + 1) * COLOR_FACTOR:
                    if prev_row[col_index] != col and prev_row[col_index] != GRID_COLOR and col != GRID_COLOR:
                        edge_row[(col_index - START_AT_COL * COLOR_FACTOR) // COLOR_FACTOR] = True

            edge_matrix.append(edge_row)

    return edge_matrix


def find_top_edge_trigger_color(filename):
    reader = png.Reader(filename=filename)
    data = reader.asDirect()

    # Figure out how many color entries there will be
    if data[3]['greyscale']:
        raise Exception("Greyscale images not supported.")
    else:
        COLOR_FACTOR = 3

    pixels = list(data[2])
    edge_matrix = []
    triggered = [False for i in range(END_AT_COL - START_AT_COL + 1)]

    for row_index, row in enumerate(pixels):
        # Ignore rows outside the indicated range
        if START_AT_ROW < row_index <= END_AT_ROW:
            edge_row = [False for i in range(END_AT_COL - START_AT_COL + 1)]

            for col_index, col in enumerate(row):
                # Ignore columns outside the indicated range
                if START_AT_COL * COLOR_FACTOR <= col_index < (END_AT_COL + 1) * COLOR_FACTOR:
                    if col_index % 3 == 0 and not triggered[(col_index - START_AT_COL * COLOR_FACTOR) // COLOR_FACTOR] \
                            and row[col_index] == TRIGGER_R and row[col_index + 1] == TRIGGER_G \
                            and row[col_index + 2] == TRIGGER_B:
                        triggered[(col_index - START_AT_COL * COLOR_FACTOR) // COLOR_FACTOR] = True
                        edge_row[(col_index - START_AT_COL * COLOR_FACTOR) // COLOR_FACTOR] = True

            edge_matrix.append(edge_row)

    return edge_matrix


def output_csv(filename, mode='top'):
    if mode == 'top':
        edge_matrix = find_top_edge_trigger_color(filename)
    if mode == 'all':
        edge_matrix = find_horizontal_edges(filename)

    name, ending = filename.split(".", 2)
    with open(name + "_edges.csv", 'w') as csv:
        rows = len(edge_matrix)
        for row_index, row in enumerate(edge_matrix):
            for col_index, col in enumerate(row):
                if col:
                    csv.write(str(col_index) + "," + str(rows - row_index) + "\n")


if __name__ == '__main__':
    if sys.argv[1] == 'help':
        print 'usage: edgefinder.py <input-png-filename>'
        print 'usage: edgefinder.py <input-png-filename> <start-row> <start-col> <end-row> <end-col>'
    elif len(sys.argv) == 2:
        output_csv(sys.argv[1])
        print 'Edge detection finished. Csv output.'
    elif len(sys.argv) == 3:
        output_csv(sys.argv[1], sys.argv[2])
        print 'Edge detection finished. Csv output'
    elif len(sys.argv) == 6:
        START_AT_ROW = int(sys.argv[2])
        START_AT_COL = int(sys.argv[3])
        END_AT_ROW = int(sys.argv[4])
        END_AT_COL = int(sys.argv[5])
        output_csv(sys.argv[1])
    else:
        print 'usage: edgefinder.py <input-png-filename>'
        print 'usage: edgefinder.py <input-png-filename> <start-row> <start-col> <end-row> <end-col>'
