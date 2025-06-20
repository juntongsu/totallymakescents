import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

sentiment_test = pd.read_csv('../data/final_sentiment_results.csv')

X = sentiment_test["Known Perfumes"].to_numpy().reshape(-1, 1)
Y_user = sentiment_test["User Similarity"].to_numpy().reshape(-1, 1)
Y_rng = sentiment_test["Random Similarity"].to_numpy().reshape(-1, 1)
Y_popular = sentiment_test["Popular Similarity"].to_numpy().reshape(-1, 1)
Y_notes = sentiment_test["Notes Similarity"].to_numpy().reshape(-1, 1)


###RNG


def create_graph(X,Y,name):
    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.9, random_state=42)

    # Create a linear regression model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, Y_train)

    # Make predictions
    Y_pred = model.predict(X_test)

    # Evaluate the model
    #mse = mean_squared_error(Y_test, Y_pred)
    #print(f"Mean Squared Error: {mse}")

    slope_string = "Approximate Slope = " + str(round(model.coef_[0][0],4))

    # Plot the results
    plt.scatter(X, Y, color='blue', label= name)
    plt.plot(X_test, Y_pred, color='black', linewidth=2, label=slope_string)
    plt.xlabel('Number of Perfumes Evaluated')
    plt.ylabel('Number of Hits')
    plt.legend()
    plt.show()
    return

create_graph(X, Y_user, "User")
create_graph(X, Y_rng, "RNG")
create_graph(X, Y_popular, "Popular")
create_graph(X, Y_notes, "Notes")





