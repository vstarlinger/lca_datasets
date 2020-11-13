import numpy as np
import time
from carculator import *

class ResultPoint:
    def __init__(self, parameters, params_array, results):
        self.parameters = parameters
        self.params_array = params_array
        self.results = results

class Datapoint:
    def __init__(self, params, size, powertrain, year, country, impact_category, impact_values):
        self.size = size
        self.params = params
        self.powertrain = powertrain
        self.year=year
        self.country=country
        self.impact_category = impact_category
        self.impact_values = impact_values
        self.impact_sum = float(impact_values.sum("impact"))


    def get_datapoint_vector(self):
        #standardize and encode strings to numbers (one hot encoding?)
        return self.impact_sum, [self.size, self.powertrain, self.year, self.country, self.lft_km]

def generate_data(num_iterations, countries):
    data = []

    # Generate data using the stochastic mode of carculator
    cip = CarInputParameters()
    cip.stochastic(num_iterations)
    dcts, array = fill_xarray_from_input_parameters(cip)
    cm = CarModel(array)
    cm.set_all()
    params = cm.array.sel(parameter=cip.input_parameters)

    for country in countries:
        bc = {'country': country}
        ic = InventoryCalculation(cm.array, background_configuration=bc)
        results = ic.calculate_impacts()

        data.append(ResultPoint({"country": country}, params, results))

    # After data generation, bring the data a format that can easily be used for 
    # training machine learning algorithms
    datapoints = {}

    # Separating data points by impact category.
    for impact_category in data[0].results.coords["impact_category"].values:
        datapoints[impact_category] = []

    print("stochastic_data_to_datapoints")
    for dp in data: #ResultPoints
        for size in dp.results.coords["size"].values:
            for powertrain in dp.results.coords["powertrain"].values:
                # Ignore plug in hybrid vehicles.
                if powertrain in ['PHEV-p', 'PHEV-d']:
                    continue

                for year in dp.results.coords["year"].values:
                    for impact_category in dp.results.coords["impact_category"].values:
                        for i in range(dp.results.shape[-1]):
                            impact = dp.results.sel({"impact_category": impact_category, "size": size, "powertrain": powertrain, "year": year, "value": i})
                            params = dp.params_array.sel({"size": size, "powertrain": powertrain, "year": year, "value": i})
                            datapoints[impact_category].append(Datapoint(params, size,powertrain,year, dp.parameters["country"], impact_category, impact))

    return datapoints

def main():
    countries = ['GB', 'CH', 'DE', 'AT', 'CA', 'US', 'BR', 'IN', 'CN', 'RU', 'ZA', 'JP', 'IT', 'ES']
    num_iterations = 200

    data = generate_data(num_iterations, countries)

    nominal_parameters = []
    parameters = []
    results = []

    for rp in data:
        for size in rp.results.coords["size"].values:
            for powertrain in rp.results.coords["powertrain"].values:
                for year in rp.results.coords["year"].values:
                    for i in range(rp.results.shape[-1]):
                        impact = rp.results.sel({"size": size, "powertrain": powertrain, "year": year, "value": i})
                        params = rp.params_array.sel({"size": size, "powertrain": powertrain, "year": year, "value": i})

                        nominal_parameters.append(xa.DataArray(data=[size,powertrain,year,rp.parameters["country"]],dims=["nom_params"]))
                        parameters.append(params)
                        results.append(impact)

    np.save('data/results{}.npy'.format(counter),np.array(results))
    np.save('data/params{}.npy'.format(counter),np.array(parameters))
    np.save('data/nom_params{}.npy'.format(counter),np.array(nominal_parameters))

main()
