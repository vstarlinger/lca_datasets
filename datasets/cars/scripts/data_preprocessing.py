###
#
# In this file, several methods are present that can be used to preprocess the data.
#
###
import numpy as np

def replace_nominal_with_numbers(data_set):
    X = data_set["X"]

    nominal_parameters_indices = np.argwhere(np.array(data_set["nominal_parameters"]) == 1).flatten()
    parameter_names = data_set["parameter_names"]

    nominal_parameter_values = {}
    for i in nominal_parameters_indices:
        #names are extracted in alphabetical order
        names = np.unique(X[:,i])
        nominal_parameter_values[parameter_names[i]] = names
        for name in names:
            X[:,i][X[:,i]==name]=np.where(names==name)[0][0]

    data_set["X"] = X.astype(float)
    data_set["nominal_parameter_values"] = nominal_parameter_values

    return data_set


def split_data(data_set, train_split, val_split, test_split):
    rng = np.random.default_rng()

    size = data_set["X"].shape[0]
    train_size = int(size * train_split)
    val_size = int(size * val_split)
    test_size = int(size * test_split)

    # Generate indices arrays
    all_indices = np.arange(size)
    train_is = rng.choice(all_indices, train_size, replace=False)
    all_indices = np.delete(all_indices, train_is)
    smaller_indices = np.arange(len(all_indices))
    i_s = rng.choice(smaller_indices, val_size, replace=False)
    val_is = all_indices[i_s]
    all_indices = np.delete(all_indices, i_s)
    test_is = rng.choice(all_indices, test_size, replace=False)

    # split X
    X = data_set["X"]
    X_train = X[train_is,:]
    X_val = X[val_is,:]
    X_test = X[test_is,:]

    # split y
    y_train = {}
    y_val = {}
    y_test = {}

    y = data_set["y"]

    for impact_category in y:
        y_train[impact_category] = y[impact_category][train_is]
        y_val[impact_category] = y[impact_category][val_is]
        y_test[impact_category] = y[impact_category][test_is]

    return X_train, y_train, X_val, y_val, X_test, y_test



