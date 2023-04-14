import pandas as pd
import os

class DataProcessing:

    def __init__(self):
        self.dataset = None
        self.routeToData = os.path.abspath("./data/co2-dataset/CO2-emissions.csv")
        self.dataset = pd.read_csv(self.routeToData)
        self.country_codes = list(self.dataset["Code"].unique())

    def top_ten(self, col_name, top):
        """

        :param col_name:  str name of column from
        :param top: int how many rows to return in answer
        :return: list with size of top or less
        """
        result_list = self.dataset.sort_values(by=[col_name], ascending=False).head(top)['Country'].values
        encoded_list = [x.encode('UTF-8') for x in result_list]
        return encoded_list

    def check_country_code(self, list_of_codes_from_request):
        # Check if input codes are corresponding to reference list of codes from datasource
        check_result = [True if x in self.country_codes else False for x in list_of_codes_from_request]

        if False in check_result:
            return False
        else:
            return True

    def co_2_emissions_and_yearly_change(self, country_codes):
        return self.dataset[self.dataset['Code'].isin(country_codes)].loc[:, ["Country", "CO2Emissions", "YearlyChange"]].to_dict('records')

    def total_emission(self, country_codes):

        return str(self.dataset[self.dataset['Code'].isin(country_codes)]["CO2Emissions"].sum())

    def calculate_statistics(self, statistics_type: int, country_codes=None, top=10):

        if statistics_type == 1 or statistics_type == 3:
            if statistics_type == 1:
                col_name = "Percapita"
            elif statistics_type == 3:
                col_name = "LifeExpectancy"
            result = self.top_ten(col_name, top=top)

        elif statistics_type == 2 or statistics_type == 4:

            # Converting codes to upper case and utf
            country_codes = [x.upper() for x in country_codes]

            # Checking if all the codes are in table
            country_codes_correct = self.check_country_code(country_codes)

            if country_codes_correct:
                if statistics_type == 2:
                    result = self.co_2_emissions_and_yearly_change(country_codes=country_codes)
                elif statistics_type == 4:
                    result = self.total_emission(country_codes=country_codes)
            else:
                result = "code misspell error"
        return result
