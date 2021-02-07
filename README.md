# LCA data sets for machine learning

This repository features data sets that can be used to learn [Life Cycle Assessment (LCA)](https://en.wikipedia.org/wiki/Life-cycle_assessment) models.

Currently the only data set available is a data set for learning a LCA model for cars. It is generated using the open source model [carculator](https://github.com/romainsacchi/carculator).

## Usage
The data for the carculator model is available as zipped .csv files in the /data folder and as numpy arrays in the data_numpy folder. The data can easily be loaded using the python scripts in the scripts folder.
The script folder also contains the script for generating data as it is represented in the data set.

### Loading the data
Data can be loaded using the lca_model class in the lca_model.py file. This loads the data using the .npz files in the data_numpy folder
```python
lca_model = lca_model()
lca_model.load_data(path_to_data)
```
The data will be loaded into a dictionary with the following structure:
```python
{ 
  parameter_names: [] list containing the parameter names (dim N)
  nominal_parameters: [] list containing a 1 for nominal parameters 0 for numerical parameters
  attribution_names: [] list containing the attribution names (dim D)
  impact_category_names: [] list containing the impact categories
  X: np.array of size NxM containing the parameter values
  y: { impact_category: np.array of size MxD } containing the impact results for the corresponding impact category
     }
}
```
