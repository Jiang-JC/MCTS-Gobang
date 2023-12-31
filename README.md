# MCTS-Gobang

## AlphaGo Zero Concept

The algorithm of AlphaGo Zero can be divided into two primary parts: Monte Carlo Tree Search (MCTS) and Neural network. MCTS is an approach to finding optimal decisions. AlphaGo Zero algorithm uses a variant of the asynchronous policy and value Monte Carlo Tree Search algorithm (APV-MCTS). In this algorithm, each node $s$ represents a board state, and each node s in the MCTS has edges $(s,a)$ to represent an action a based on state node $s$, in which action $a \in A(s)$. ($A(s)$ is a set of all legal actions). Besides, each edge stores the following statistics.

{ $N(s,a)$, $W(s,a)$, $Q(s,a)$, $P(s,a)$ }

$N(s,a)$ is the visit count, which records the time of visiting node $s$ and choosing action $a$.

$W(s,a)$ is the total action value.

$Q(s,a)$ is the mean action value, which is $W(s,a)/N(s,a)$.

$P(s,a)$ is the prior probability of selecting this edge.

AlphaGo Zero can be divided into 4 phases: **Selection, Expansion and Evaluation, Backup, and Play**. We will introduce each part as follows.

### Selection

<img src="Result_Presentation\Selection.png" width="400">

The selection is the first step of the Monte Carlo Tree Search. In a complete simulation, we start the simulation at the root node $s_0$, and reach a leaf node $s_L$ at time-step $L$. (There are two kinds of leaf node $s_L$: first one is a node that has not been expanded and doesn't have child nodes, the second one satisfies the simulation finish condition, and the game is finished.)

In each time-step before time-step $L$, an action based on the statistic of Monte Carlo Tree Search will be selected by the following equation.

$a^*=\underset {a}{argmax}(Q(s_t,a)+U(s_t,a))$

$U(s,a)=c_{puct}P(s,a)\frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)}$

$Q(s_t,a)$ is the mean action value mentioned above.

$U(s_t,a)$ is a value that represents the level of preferring exploration.

$c_{puct}$ is a constant to adjust the tendency to explore.

$Q(s_t,a)$ is affected by the performance of the action, $U(s_t,a)$ is dependent on the visit count and prior probability, representing the exploration level. Consequently, this algorithm will prefer actions with low visit count, high prior probability, and high action value.

In other words, the strategies both have exploration and exploitation tendencies (exploration means preferring non-explored action, and exploitation means preferring best-known action). The algorithm will make a trade-off between them, which will be affected by some parameters, for example, changing the number of $c_puct$ will make a great difference.

### Expansion and Evaluation

<img src="Result_Presentation\Expansion.png" width="400">

The first kind of leaf node $s_L$, which has not been extended and doesn't have child nodes, will be added to the neural network for evaluation.

$(d_i (p),v)=f_\theta (d_i (s_L))$

$f_\theta$ means neural network

$d_i$ means rotation or dihedral reflection uniformly, which can augment the data and train the neural network better.

$v$ is scalar evaluation, estimating the probability of the current player winning from position $s$.

$p$ is the vector of move probabilities, representing the probability of selecting each move $a$. 

After that, the leaf node $s_L$ will be extended with all legal moves, and each edge $(s_t,a)$ will be initialized as follows.

${ N(s_t,a)=0, W(s_t,a)=0, Q(s_t,a)=0, P(s_t,a)=p_a }$

Besides, $v$ will be backed up.

### Backup

<img src="Result_Presentation\Backpropagation.png" width="400">

The next phase is backup. The edge statistics will be updated in this step as follows.

$N(s_t,a_t) = N(s_t,a_t )+1$

$W(s_t,a_t) = W(s_t,a_t )+ v$

$Q(s_t,a_t) = (W(s_t,a_t))/(N(s_t,a_t))$

There are two significant features of backup. Firstly, the edge update will backtrack from the leaf node $s_L$ until the root node $s_0$; secondly, we use virtual loss $v$ to update edges, ensuring that each thread can evaluate different nodes.

### Play

AlphaGo Zero will select an action a in the root node s_0 at the end of the search, which is proportional to its exponentiated visit count.

$\pi(a|s_0 )=\frac{N(s_0,a)^{\frac{1}{\tau}}}{\sum_b {N(s_0,b)^\frac{1}{\tau}}}$


$τ$ is a temperature parameter that can adjust the level of exploration.

$N(s_0,a)$ is the visit count, which records the time of visiting the node $s_0$ and choosing action a.

The Monte Carlo Tree will be reused at subsequent time-steps, and the child node representing played action will become a new root node. The subtree below this child node will be retained along with all its statistics. The remaining part of the tree is discarded.

Besides, if the root and best child values are lower than a threshold value v_resign, AlphaGo Zero will resign.


## Result

<img src="MCTS_code\movies\game_3.gif" width="400">

<img src="MCTS_code\movies\game_8.gif" width="400">



