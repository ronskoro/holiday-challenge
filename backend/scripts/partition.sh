#!/bin/bash

# Create the partitions folder if it doesn't exist
mkdir -p data/new_partitions

# change the column to partition on based ont eh 
# Read the input CSV file and process each line using AWK
tail -n +2 data/offers.csv/offers.csv | awk -F',' '{
    # Extract the value from the 10th column (column index 10)
    value = $10
    gsub(/"/, "", value)  # Remove surrounding double quotes from the value

    # Set the output file path based on the value
    filename = "data/partitions/offer_" value ".csv"

    # Check if the output file exists, if not create it and write the header
    if (!(filename in files)) {
        files[filename] = 1
        print header > filename
    }

    # Append the current line as a CSV to the output file
    csv_line = gensub(/"/, "", "g", $0)  # Remove surrounding double quotes from the line
    print csv_line >> filename
}' header="\"hotelid\",\"outbounddeparturedatetime\",\"inbounddeparturedatetime\",\"countadults\",\"countchildren\",\"price\",\"inbounddepartureairport\",\"outboundarrivalairport\",\"inboundarrivaldatetime\",\"outbounddepartureairport\",\"inboundarrivalairport\",\"outboundarrivaldatetime\",\"mealtype\",\"oceanview\",\"roomtype\""