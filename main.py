# webscapper script

# written by boaz

# Have fun


import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import scipy.stats as stats

url = "https://www.worldometers.info/cars/"

data = requests.get(url)

# create lists that will hold the data that will be scrapped

years = []
amount = []

def change_to_integer(x):
    if "," in x:
        num = int(x.replace(",", ""))
    
    else:
       num = int(x)

    return num


if data.status_code == 200:
    soup = BeautifulSoup(data.content, 'lxml')

    table = soup.find('table')
    #print(table)

    

    if table:

      # open and write to the csv file
        
      with open("cars.csv", "w", newline="") as file:
        csv_writer = csv.writer(file, dialect='excel')

        for row in table.find_all('tr'):
            # print(row) 
            columns = row.find_all('td')
            if columns:
                row_data = [col.get_text(strip=True) for col in columns]
                if "cars producedin the world" in row_data:
                   
                  # removes and formats the headers

                   index = row_data.index("cars producedin the world")
                   row_data[index] = "Cars produced in the world"

                years.append(row_data[0])
                amount.append(row_data[1])


                # print(row_data)
                csv_writer.writerow(row_data)



# remove the heading of the columns (years and number of vehicles)

del years[0]
del amount[0]

# change the collected data to the right format

cleaned_years = list(map(change_to_integer, years))
cleaned_numbers = list(map(change_to_integer, amount))

# this is like a debug statement that ensures that the data we're collecting is in the 
# right format and can be ignored.

print(f"{years} \n {cleaned_numbers}")

slope, intercept, r, p, stderr = stats.linregress(cleaned_years, cleaned_numbers)

def y_values(x):
   return slope*x + intercept

# Get linear regression y values

y_axis_values = list(map(y_values, cleaned_years))

# plot the graphs

plt.scatter(cleaned_years, cleaned_numbers)
plt.plot(cleaned_years, y_axis_values)
plt.xlim(min(cleaned_years), max(cleaned_years))
plt.gca().set_aspect('auto')
plt.xlabel("Years")
plt.ylabel("Number of Cars")
plt.title("Cars")

if r > 0.7:
   print(f"The r score of {r} shows great corelation between the given data.")

elif r < -0.7:
   print(f"The r score of {r} shows great corelation between the given data.")

elif r == 0:
   print(f"The r score of {r} shows no corelation between the given data at all.")

else:
   print(f"The r score of {r} shows great corelation between the given data but it isn't substantial enough for future predictions.")



plt.show()


print(f'The number of cars in 2020 was {y_values(2020)}')
                    

