### En passant as a follow up Q

- Does a player's ELO predict whether they're more likely to win?

- FOllow up: Is it possible to predict ELO based on the context of a potential en passant move?

    Things that count as context:
    - Does it put you in a significantly better/worse board position
    - Does it barely affect board position
    - Did the player take a significantly short/long amount of time to en passant when available
    - 

    Could look at whether each time en passant is taken does it actually put you in a better position or are ppl taking it for the sake of e.p., or are ppl not taking e.p. cos they don't wanna be in a worse position, or are they not taking it cos they don't know it's a thing - and can we use this to predict ELO?




## Q1 Does the player with a higher ELO have a higher chance of winning a game against someone with a lower ELO?
### Linear regression (s2 w6)
Answers the questions:
- What is our confidence in the regression coefficients?
- Do they represent a real effect and not just a chance or correlation in data?
- Can we quantify uncertainty?



## Q2 Is it possible to predict ELO based on the context of a potential en passant move?

### Building our prediction model:

### Evaluating our prediction model: Linear regression (s2 w6)
Answers the questions:
- What is our confidence in the regression coefficients?
- Do they represent a real effect and not just a chance or correlation in data?
- Can we quantify uncertainty in our predictions? Use bootstrap to estimate uncertainty in the coefficients.
  
### Evaluating our prediction model: Bootstrap for Hypothesis testing (s2 w6)
Shows that the slope of the regression model is significantly different from 0.

Can also do a T-test and p-value for this.

Prediction uncertainty for comparing predicted ELO of player to actual ELO.
For this we could also use principle of maximum likelihood: adjust the model coefficients so as to maximise likelihood that observed data arises from the model.

Can derive algebraic expression for standard error of intercept of gradient

Standard error in estimator.