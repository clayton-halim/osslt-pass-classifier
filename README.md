# Introduction
A logistic regression algorithm by gradient descent that identifies whether a student will pass the Ontario standardized literacy test on their first try.

While the logistic regression algorithm only requires numpy to run, it also requires scikit-learn for its confusion matrix capabilities so that the f1 score can be calculated.

# Usage
If you want to just play around, all of the work has already been done! `logistic_regression.py` has been set to run a k-fold crossfold validation test on the current data set `oversampled_output_normalized.csv`.

Training the classifier on new data is a simple as `lr.train(X, y)` where `lr` is the logistic regression object, `X` is the training set and `y` is the target set.

Utilizing the classifier is just `lr.predict(data)` where `data` is a 2D numpy array containing all the instances to predict, alternatively `lr.predict_proba(data)` also works if one wanted to see the confidence of the prediction for each instance.

# Dataset
In `oversampled_output_normalized.csv`the data is formatted as follows:

| Database ID | Passed on First Try | Sex | English as Native Language | Grade 9 English Average | Academic | Applied | Locally Developed | IB  |
| ----------- | ------------------- | --- | -------------------------- | ----------------------- | -------- | ------- | ----------------- | --- |

`Passed on First Try` is what is used as the target set. (1 for passing on first try, 0 for failling). 

In Ontario high schools, Academic, Applied, and Locally Developed are different levels of difficultly in the courses that students take from hardest to easiest respectively. IB is the International Baccalaureate programme that some Students also have the option of taking (a worldwide programme considered to be more rigourous than the other 3). The level of the student is determined by analyzing the course code of their grade 9 English course. (1 for being enrolled in the level, thus all other levels should be marked as 0).

`Sex` is 1 for male, 0 for female.

`Grade 9 English Average` is 0 to 100 z-scaled down to -1 to 1.

If you would like to try feature engineering on your own, the raw data has been included as txt files. `dataset_decoder.py` may give you a starting point on where to go.
