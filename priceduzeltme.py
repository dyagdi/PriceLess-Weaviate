import csv

input_file = "/Users/dyagdi/Downloads/a101_products_2025-05-05.csv"
output_file = "/Users/dyagdi/Downloads/temizlenmisa101.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    headers = next(reader)
    writer.writerow(headers)

    for row in reader:
        cleaned_row = []
        for i, value in enumerate(row):
            value = value.strip()

            # price veya high_price kolonlarında ise
            if headers[i] in ["price", "high_price"]:
                if value == "":
                    cleaned_row.append("")
                else:
                    # "1.194,50" → "1194.50"
                    value = value.replace(".", "").replace(",", ".")
                    try:
                        # kuruşla yazılmışsa böl
                        if value.isdigit():
                            value = str(float(value) / 100)
                        cleaned_row.append(value)
                    except:
                        cleaned_row.append("")
            else:
                cleaned_row.append(value)
        writer.writerow(cleaned_row)