Statistics App

Project idea came from my past work experience working for 5 years as financial crime analyst in a financial institution.
Working in a organized team within department, all of the work is quatified out of data extracted from in same format
for 3 years straight. This app provides overview, necesarry data formatting, graphs required to minimize time spent
on creating reports for management. Although, the dataset used is not one that i have encoutered in my previous job,
app allows minor modifications to be adaptable to required dataset template.

The dataset used was acquired from https://www.kaggle.com/datasets/dermisfit/fraud-transactions-dataset

App functions:
- View of general data:
  Allows to upload most common excel files to view general data - Column count, column names, unique values in columns,
  and empty value counts
- Clean data (applicable only on master dataset):
  Allows user to select how to format the uploaded dataset. Current options are:
  -Remove unnecessary columns: Removes columns and their values not necessary for statistics generation
  -Rename columns: Renames all columns to be more user friendly
  -Calculate distance based on coordinates: Dataset has persons' home coordinates and stores' coordinates, method
  takes all coordinate values to calculate distance between home location and store which can indicate financial fraud.
  -Adjust values: Dataset contains merchant names starting with fraud_ which method removes. In addition, first name
  and last name columns are joined for easier unique name matching.
  -Split date and time column: Date and time column is meshed together in master dataset which method splits in two
  columns of date and time.
  -Add card type and industry columns: Based on card number, method extrapolates additional information of type (i.e.
  MasterCard, Visa) and industry type card was issued for (Airlines, Oil, Banking, etc.)
-Statistics (applicable only on master dataset):
  Allows to generate graphs from dataset provided and download them to place in reports. Although only one graph is
  programmed, it's not difficult to program more relevant graphs.

Installed libraries:
Pandas
Custom Tkinter
Odfpy
Xlrd
Openpyxl
Xlsxwriter
Requests (only if using API)

For specific releases read requirements.txt