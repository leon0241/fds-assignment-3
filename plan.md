
## .
## __Q1 Does the player with a higher ELO have a higher chance of winning a game against someone with a lower ELO?__
## .

### __Sampling data:__
Random sample? Stratified for time-control?
Filter out all with incomplete entries
### .

### __Determine answer for question: Logistic regression:__
Find association between continuous predictor (ELO) and binary outcome (win/loss).

Don't include draws.

Determine the decision boundary (threshold for a win/loss).

If logistic regression doesn't work, look into k-nearest neighbours.

Use principle of max likelihood to get best estimates for logistic regression?
### .

### __Determine answer for question: Odds ratios__
Graph, contingency tables for odds ratio.
### .

### __Evaluate confidence of our findings: Hypothesis testing (s2 w1)__
p-values
### .

### __Evaluate confidence and uncertainty for our findings: Linear regression (s2 w6)__
Answers the questions:
- What is our confidence in the regression coefficients?
- Do they represent a real effect and not just a chance or correlation in data?
- Can we quantify uncertainty?
## .

## __Q2 Is it possible to predict ELO based on the context of a potential en passant move?__
## .

### __Sampling data:__
Only require games which involve a potential ep
### .

### __Building our prediction model: Unsupervised learning__

We wish to predict ELO on basis of the variables:
- (Assuming player is making the ep capture): 
    - Whether ep was taken where opportunity arose
    - Time taken to take/respond to taking the ep capture
    - Colour
    - If it gives an advantage
### .

###### __PCA__
Before clustering, apply PCA to reduce dimensionality.
### .

###### __Scree plot__
Use this to find the number of desired clusters for K-Means.

Plot mean squared error against the number of clusters k and look for an elbow.
### .

###### __Clustering: Partitional K-Means__

Divide set of D-dimensional unlabelled data points into k clusters (k was found earlier using a scree plot).

Represent each cluster by a single prototype (centre of cluster).

Look into vector quantisation?

Compare different clustering combinations with a mean squared error function?
### .

###### __Training and Testing set__
(See FDS CW2 Paintings report for info on the ratio to split the training and testing data.)
(Lila Check what the equivalent for unspurervised learning is. Rn this paragraph is info for a supervised learning set.)
Training set = Players with known data
Test set = 'Unknown ELO' - it is the job of a classifier to predict a label for each test item.
### .

### __Evaluating our prediction model: Linear regression (s2 w6)__
Answers the questions:
- What is our confidence in the regression coefficients?
- Do they represent a real effect and not just a chance or correlation in data?
- Can we quantify uncertainty in our predictions? Use bootstrap to estimate uncertainty in the coefficients.
### .
  
### __Evaluating our prediction model: Bootstrap for Hypothesis testing (s2 w6)__
Shows that the slope of the regression model is significantly different from 0.

Can also do a T-test and p-value for this.

p-values indicate how incompatible the data are with a specified statistical model. Can talk about confidence intervals with this.

Prediction uncertainty for comparing predicted ELO of player to actual ELO.
For this we could also use principle of maximum likelihood: adjust the model coefficients so as to maximise likelihood that observed data arises from the model.

Can derive algebraic expression for standard error of intercept of gradient

Standard error in estimator.
### .