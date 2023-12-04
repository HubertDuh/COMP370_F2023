1.1- Using awk -F, 'END {printf "Number of Rows : %s\nNumber of Columns = %s\n", NR, NF}' clean_dialog.csv, we see that we have 36860 rows and 4 columns.
  - awk is a file processing tool
  - -F specifies a CSV format and that the field seperator is ','
  - The following portion is a script where:
    - End signifies that we want to do the operation after processing all the lines
    - printf is a printing format
    - NF is an awk built-in variable that represents the number of fields
    - NR is an awk built-in variable that represents the number of records
  - We input clean_dialog.csv in the script

1.2- Alternatively, we can use csvstat --count clean_dialog.csv to count the number of rows. We can also see the number of columns using csvcut -n clean_dialog.csv

2- Using csvstat clean_dialog.csv we can get the specification of each of the columns

3- From the previous command we see that there is 197 unique values for title, it is thus safe to assume that the dataset covers 197 episodes.

4- One tricky aspect could be when all ponies speak together so we also have to consider these cases for individual speaking frequencies. This also applies when a lot but not all ponies talk together, we will need to process the data and consider these cases. There are also instances where a pony's name is mentioned but they don't speak.

<br>

- Run cut -d ',' -f 3 clean_dialog.csv | egrep -w '\b[character_name]\b' | egrep '\S+[character_name]' | egrep -c '[character_name]\S+' to get the number of time the character spoke
- We can then calculate the frequencies by hand



  
