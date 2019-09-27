import csv


if __name__ == '__main__':

    d1_file_in = open('file', 'r')
    d2_file_in = open('file', 'r')
    file_out = open('file', 'w')

    # load dataset 1
    d1 = []
    csvr1 = csv.reader(d1_file_in)
    h1 = csvr1.__next__()
    for row in csvr1:
        d1.append(row)
    # read data set 2 and merge..

    csvr2 = csv.reader(d2_file_in)
    csvw = csv.writer(file_out)
    h2 = csvr2.__next__()
    h2 = h2[1:]
    hf = h1.append(h2)
    csvw.writerow(hf)
    for row in csvr2:

       continue



