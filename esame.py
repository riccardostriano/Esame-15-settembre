class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        try:
            data = []
            with open(self.name, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) != 2:
                        continue
                    date, passengers = parts
                    try:
                        date = date.strip()
                        passengers = int(passengers.strip())
                        data.append([date, passengers])
                    except ValueError:
                        continue
            return data
        except FileNotFoundError:
            raise ExamException(f"File '{self.name}' not found.")
        except Exception as e:
            raise ExamException(str(e))

def detect_similar_monthly_variations(time_series, years):
    if len(years) != 2:
        raise ExamException("Input 'years' must contain two years.")

    data_filtered = [item for item in time_series if years[0] <= int(item[0].split('-')[0]) <= years[1]]

    if len(data_filtered) < 12:
        raise ExamException("Insufficient data for the specified years.")

    similar_variations = []
    for i in range(1, len(data_filtered) - 1):
        current_year_diff = data_filtered[i][1] - data_filtered[i - 1][1]
        next_year_diff = data_filtered[i + 1][1] - data_filtered[i][1]
        
        is_similar = abs(current_year_diff - next_year_diff) <= 2
        similar_variations.append(is_similar)

    return similar_variations[::2]

if __name__ == "__main__":
    time_series_file = CSVTimeSeriesFile(name='data.csv')
    time_series = time_series_file.get_data()
    
    years_to_check = [1949, 1950]
    
    try:
        result = detect_similar_monthly_variations(time_series, years_to_check)
        for value in result:
            print(value)  
    except ExamException as e:
        print("Error:", e) 