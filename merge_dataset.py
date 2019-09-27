import csv
import sys

csv.field_size_limit(sys.maxsize)

if __name__ == '__main__':

    d1_file_in = open('dataset/org_data.csv', 'r')
    d2_file_in = open('dataset/fixed_data.csv', 'r')
    file_out = open('data.csv', 'w')

    # load dataset 1
    d1 = {}
    csvr1 = csv.reader(d1_file_in)
    h1 = csvr1.__next__()
    for row in csvr1:
        d1[row[0]] = row[1:]
    d1_file_in.close()

    # read data set 2 and merge..
    d2 = []
    csvr2 = csv.reader(d2_file_in, delimiter='\t')
    h2 = csvr2.__next__()
    for row in csvr2:
        d2.append(row)
    d2_file_in. close()

    d3 = []

    for item in d2:

        url = item[0]
        try:
            other_data = d1[url]
            new_item = item + other_data
        except:
            print('Unvalid url: {}'.format(url))

        d3.append(new_item)

    # fix header
    h2[2], h2[3] = h2[3], h2[2]

    new_header = h2 + h1[1:]
    csvw = csv.writer(file_out)
    csvw.writerow(new_header)
    for item in d3:
        csvw.writerow(item)
    file_out.close()




















