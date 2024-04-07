"This module parse the csv given."
import csv

class DataIngestor:
    """Class to parse the csv file """
    def __init__(self, csv_path: str, logger):
        self.path = csv_path
        self.logger = logger
        self.data = self.parse_csv(self.path, "DataValue")
        self.data_by_category = self.parse_csv(self.path, "Category")
       

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily']

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]
    def parse_csv(self, path, type_of_dict):
        """Function to parse the csv file and retrieve what's important."""
        self.logger.info(
            f" Enter the method PARSE_CSV with parameter: {path} and {type_of_dict}")
        # citesc fisierul csv si creez un dictionar cu datele extarse
        with open(path, 'r',encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            data_dict = {}
            for row in csv_reader:
                key = row[8]
                if key not in data_dict:
                    data_dict[key] = {}
                if type_of_dict == "DataValue":
                    col = row[4]
                else:
                    if (row[30] == '' or row[31] == ''):
                        continue
                    col = str((row[4], row[30], row[31]))
                if col not in data_dict[key]:
                    data_dict[key][col] = []
                data_dict[key][col].append(row[11])
        return data_dict
