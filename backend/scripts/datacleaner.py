import csv
# This class is meant for cleaning the data and removing redundant information
class DataCleaner():
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
    
    def dropColumns(self, cols_to_drop):
        with open(self.inputFile, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            header = next(reader)  # Read the header row
            column_indices = [index for index, col in enumerate(header) if col not in cols_to_drop]

        with open(self.outputFile, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([header[index] for index in column_indices])  # Write the modified header row

            for row in rows[1:]:  # Iterate over the remaining rows (excluding header)
                new_row = [row[index] for index in column_indices]
                writer.writerow(new_row)


dc = DataCleaner('data/offers.csv/offers.csv', 'data/offers.csv/offers_min.csv')
# Drop inbounddepartureairport and inboundarrivalairport since they are always PMI(Mallorca).
# Drop outboundarrivalairport since the airport is the same as the outbounddepartureairport.
dc.dropColumns(["inbounddepartureairport", "inboundarrivalairport", "outboundarrivalairport"])




