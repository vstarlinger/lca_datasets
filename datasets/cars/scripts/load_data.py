def load_data(path_to_data, num_files=-1):
    data_set = {}
    with open(os.path.join(path_to_data, "meta_information.json"), "r") as f:
        data = f.read()
        data_set = json.loads(data)

    if num_files > 0:
        X_parts = []
        y_parts = []

        for i in range(num_files):
            X_parts.append(np.load(os.path.join(path_to_data, "X_chunk{}.npz".format(i)))["X"])
            y_parts.append(np.load(os.path.join(path_to_data, "y_chunk{}.npz".format(i))))

        X = np.concatenate(X_parts)

        y = {}
        for cat in y_parts[0]:
            y[cat] = []
            for i in range(len(y_parts)):
                y[cat].append(y_parts[i][cat])
            y[cat] = np.concatenate(y[cat])

    else:
        X = np.load(os.path.join(path_to_data, "X.npz"))
        X = X["X"]

        y = np.load(os.path.join(path_to_data, "y.npz"))

    data_set["X"] = X
    data_set["y"] = y

    return data_set

