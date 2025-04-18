import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

hit_test = pd.read_csv('data/final_hit_results.csv')

X = hit_test["Known Perfumes"].to_numpy().reshape(-1, 1)
Y_rng = hit_test["RNG"].to_numpy().reshape(-1, 1)
Y_user = hit_test["User(Sum)"].to_numpy().reshape(-1, 1)
Y_notes = hit_test["Notes"].to_numpy().reshape(-1, 1)
Y_popularity = hit_test["Popularity"].to_numpy().reshape(-1, 1)
Y_gamma = hit_test["Gamma"].to_numpy().reshape(-1, 1)
Y_top_20 = hit_test["Top 20"].to_numpy().reshape(-1, 1)


###RNG


def create_graph(X,Y,name):
    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.9, random_state=42)

    # Create a linear regression model
    model = LinearRegression(fit_intercept=False)

    # Train the model
    model.fit(X_train, Y_train)

    # Make predictions
    Y_pred = model.predict(X_test)

    # Evaluate the model
    #mse = mean_squared_error(Y_test, Y_pred)
    #print(f"Mean Squared Error: {mse}")


    sum_string =name + " (total hits = " + str(round(np.sum(Y),2)) + ")"
    slope_string = "Approximate Slope = " + str(round(model.coef_[0][0],3))

    # Plot the results
    plt.scatter(X, Y, color='blue', label= sum_string)
    plt.plot(X_test, Y_pred, color='black', linewidth=2, label=slope_string)
    plt.xlabel('Number of Perfumes Evaluated')
    plt.ylabel('Number of Hits')
    plt.legend()
    plt.show()
    return


create_graph(X,Y_rng, "RNG average")
create_graph(X, Y_user, "User")
create_graph(X, Y_notes, "Notes")
create_graph(X, Y_popularity, "Popularity")
create_graph(X, Y_gamma, "Gamma")
create_graph(X, Y_top_20, "Top 20")







