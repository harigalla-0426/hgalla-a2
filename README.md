# a2-release-res
# Part – 1: Raichu
# How we formulated the problem:
This is a 2-player turn-based game and hence, a classic Mini-Max problem. Here, we find the optimal move for a player, assuming that our opponent also plays optimally. Here, the White player is considered the Maximizer who tries to maximize the evaluation function, while the Black player acts as a Minimizer who will always try to minimize the evaluation function. 
The evaluation function used here will tell us how good the board is for a given player. If the score here is positive, it favours the White player i.e. Maximizer and vice-versa for the Black player/Minimizer.

=====================================================================================

# How our program works:

Step 1: First, the main function validates the inputs and calls the find_best_move method which is the main method that yields the output boards for each depth.
Step 2: The find_best_move method internally calls the minimax method with the desired player.  
Step 3: The mini-max method will be called recursively in a depth-first manner, until it either reaches its maximum depth or an end solution.
Step 4: The evaluation from these states is then propagated back to the top which will help the player to make a decision.
Step 5: Here, we have also included the alpha and beta values for pruning. The alpha value of max is the lower bound of the backed-up values whereas the beta value will give the min on the upper bound.


## Below are the functions used in the program:
•	Function board_to_string takes in the current board state and N as arguments and returns the board state as a string.

•	Function string_to_board takes in the string value for board state and N as arguments and returns board in the matrix format from the input string.

•	Function string_output takes in the board state and N as arguments and converts the board from grid format back to a string before displaying the output.

•	Function is_valid_index takes in the positions i, j and N as arguments and will check if the given index is inside the scope of the board.

•	Function find_count takes in the current board state as an argument and returns the count along with indices of each piece on the boardFunction outer_move_clockwise takes in the current board state as an argument and returns the count along with indices of each piece on the board.

•	Function return_modified_board takes in the board, oldpos, newpos, isAttack, attackPos, returnCopy as arguments and returns the modified board by swapping the positions and other options specified like: whether it's in attack mode or whether to return a copy of board etc..

•	Function evaluation_function takes in the current board state as an argument and returns the calculated value of the evaluation function e(s), which will help decide how good a particular board is for one player

•	Function check_raichu_evolution takes in the current board state and N as arguments, and Checks for Raichu formation for both white and black pieces.

•	Function check_game_end takes the current board state as input and Checks if the game has ended.

•	Function successors takes the board state and isWhiteTurn as inputs and finds all the successors for a given board state. Here, we calculate the possible moves and attacks of Pichu, Pickachu and Raichu for both the Black and White players respectively, as mentioned in the problem. After calculating this, the successors are returned.

•	Function minimax takes the board, depth, isWhiteTurn, alpha and beta values as input arguments. This method will call minimax recursively in a depth-first fashion until 
    a) it reaches its max depth or 
    b) it reaches an end solution. 
The evaluation values from these states are propagated upwards keeping in check that each player will make the best possible move from the successors available.

Here alpha and beta values are used for pruning.
The beta value of min is the upper bound on the final backed-up value. It can never increase.
The alpha value of max is the lower bound on the final backed-up value. It can never decrease.

•	Function find_best_move takes the board, N, player and timelimit as input arguments. Here, we increment the depth every time and yield the minimax output until the program is terminated.

=====================================================================================

# Problems/Assumptions/Decision designs/Simplifications:
•	Assumptions:
1. We assume that each player optimally i.e. chooses the best possible move for themselves.

2. We assume that for the given weights of the evaluation function and the board sizes, the max value will be lesser than 99999 and the min value will be greater than 99999

•	Problems faced:
1.	We faced very few issues when completing the successor functions and evaluation functions. However, the main struggle started when our code was competing with AI and other players. Our code had some edge cases that were missed, and our player was missing some obvious moves when the opponent made mistakes. 
2.	We put in a lot of effort to debug this, but could not figure out where it was missing. The game goes very smoothly at the beginning and the above issue may or may not occur at the end. Sometimes we win, and sometimes we get this issue. But mostly we are able to beat the AI.


==============================================================================================================================================================================================================================================================================================================================================

# Part 2 : Truth To Be Told
# How we formulated the problem:
    We are given to solve a classifier problem for Spam detection using the Naive Bayes classifier.
    Naive Bayes is one of the classification techniques used in Machine Learning, NLP and AI. This is derived from the Bayes theorem, which assumes that all the features that predict a target value are independent.

Bayes theorem:
P(H|E) =       (P(E|H) * P(H)) / P(E)
    

Here, P(H|E) is the Posterior probability given that the Evidence is true.
P(E|H) is Likelihood of the evidence given that the Hypothesis is true.
P(H) is the Prior probability of the Hypothesis.
P(E) is the Prior probability of the Evidence being true.

For the current problem, we are given some reviews and need to classify if they are spam or not. The idea is to train on the given set of reviews where for each review, we have a class present either as Spam or Not Spam. We use the Naïve Bayes Classifier to solve this problem where for any new input of data/review, we classify it either as Spam or Not Spam after training on the current set of inputs.

The features here are nothing but a set of words in each review and the target class is either Spam or Not Spam. So this forms under the Binary Classification problem. Naïve Bayes is Naïve because it assumes that the features that predict the class are independent of each other. We calculate the probability of each class given a set of features and see which class the features belong to comparing the probabilities for each class.

Let’s take the features as X = {x1, x2, x3, ……, xn}
The target class label Y = {y1, y2}

Example: For each review we take, X is a set of words in the review and Y is the class for the review after classification.

Review1: The movie is good, however, it can be better – Not Spam
X = {The, movie, is, good, however, it, can be, better}
Y = {Not Spam}

Review2: The movie is very good, the good is movie very, click on the below link to win the lottery – Spam
X = {The, movie, is, very, good, click, on, below, link, to, win, lottery}
Y = {Spam}

From the Bayes chain rule, we can use the below formula to find the probabilities.

             P(y|X) = (P(X|y)*P(y)) / P(X)           


But as Naïve Bayes is Naïve, and it assumes the conditional probabilities to be independent, we can break this probability to below.
X= (x1, x2, x3, …..) are the set words for each review
P(X|y) = P(x1|y) * P(x2|y) * P(x3|y) * P(x4|y) * ………. P(xn|y) 
P(X) = P(x1) * P(x2) * P(x3) * P(x4) *…………… P(xn) 


 P(y|X)  =  ((P(x1|y) * P(x2|y) * P(x3|y) * P(x4|y) * ………. P(xn|y)) *P(y)) /  (P(x1) * P(x2) * P(x3) * P(x4) *…………… P(xn))         

                

Therefore, from the above formula, we calculate the probabilities for both the classes Y = {Spam, Not Spam} and compare to select the higher value of these probabilities to classify the review accordingly.

=====================================================================================

# How our Program works:

Step 1: We create a function called computeParameters wherein we first create a dictonary ClassDict that holds two types of classes as the keys and the values contain all the words in reviews corresponding to the class.

Step 2: next we create a probDict Dictonary which also has two keys for two class types and holds the probability of each word given that it belong to a particular class.ie..P(wn/T)or P(xn/F)

Step 3: later we perform laplace smoothening for all the probabilities so that if there is any probability with a value 0, then we give it a weight so that it is not biased because of the 0
Step4: Then we created a mainProb Dictionary which holds the probability of each class type(Deceptive or truthful)

Step5: Now,we perform naïve bayes wherein we calculate the probability if is the truth given the word & also the probability of deceptive given the word. We multiply the probability of all the words in the review with the corresponding class type probability.

Step6: Finally we compare the deceptive and Truthful probability for each word calculated. If the truthful probability is greater than the deceptive probability, then we append a label truthful, else we append a label deceptive. 

=====================================================================================

# Problems/Assumptions/Decision designs/Simplifications:

•	Assumptions:
1. Naïve Bayes is Naïve, therefore the features are independent of each other.

2. We assume that there are only 2 classes and hence this works for Binary classification. However, we can use the same for Multi-Class classification with very little modification of the code base.


•	Problems faced:
One major issue that we encountered when solving this problem is the probabilities being calculated as 0 for one category and some non-zero values for another. On careful observation, we noticed that this is occurring because there are some words which are present in one class – A, while not in another - B, which is resulting in the probability for the review to be under class A is 0, and thereby classifying the review always into the class B. To address this, we used the below technique.

Zero Frequency Problem/ Laplace Smoothing: A small-sample correction is included in every probability estimate.

i.e. we add a value ‘a’ to the numerator and ‘1 + a*d’ to the denominator when calculating the probabilities. This ensures that the probabilities are never 0. 
In this case, we took the values as follows:
a = 1
d = No. of unique words in our dataset


•	Design decisions:
1. To eliminate all the punctuations and numerals from the reviews as they do not contribute much to the class prediction/classification.

2. One Design decision that we considered is to go for logarithmic values of the probabilities instead of their plain products. This is because we see that the product of probabilities is resulting in extremely small values which are eventually rounded off to 0.0 by Python in some cases. To avoid this, we took the logarithm for the probabilities and tested it, which has no effect on the result modification.

3. 
P(y|X) =  ((P(x1|y) * P(x2|y) * P(x3|y) * P(x4|y) * ………. P(xn|y)) *P(y)) /  (P(x1) * P(x2) * P(x3) * P(x4) *…………… P(xn))   

                 

In the above probability calculation, we can eliminate the denominator because it is same for all the values.

P(y|X) is directly proportional to (P(x1|y) * P(x2|y) * P(x3|y) * P(x4|y) * ………. P(xn|y)) *P(y).



•	Other Attempts made: 
1. Using NLTK library to tokenize the sentence. The accuracy has dropped by 2% when testing this and hence it was not used. Instead of this, we eliminated the punctuations and special characters by ourselves in the code.

2. Using NLTK to eliminate the stop words. The accuracy has dropped again in this case by >5%, and it is expected, because the stop words might contribute to the result being Spam or Not Spam.

3. Extract the frequently occurring words instead of the entire set of words, however, we see a decline of accuracy here as well, since the less frequent occurring words might play a key role in the classification.

