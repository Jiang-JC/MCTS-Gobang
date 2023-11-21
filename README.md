# MCTS-Gobang

## MONTE CARLO TREE SEARCH (MCTS) Concept

The algorithm of AlphaGo Zero can be divided into two primary parts: Monte Carlo Tree Search and Neural network. Monte Carlo Tree Search is an approach to finding optimal decisions. AlphaGo Zero algorithm uses a variant of the asynchronous policy and value Monte Carlo Tree Search algorithm (APV-MCTS). In this algorithm, each node s represents a board state, and each node s in the MCTS has edges (s,a) to represent an action a based on state node s, in which action a∈A(s). (A(s) is a set of all legal actions). Besides, each edge stores the following statistics.
\{$N(s,a)$,$W(s,a)$,$Q(s,a)$,$P(s,a)$\}

$N(s,a)$ is the visit count, which records the time of visiting node s and choosing action a.

$W(s,a)$ is the total action value.

Q(s,a) is the mean action value, which is W(s,a)/N(s,a).

P(s,a) is the prior probability of selecting this edge.

Monte Carlo Tree Search can be divided into 4 phases: Select, Expand and Evaluate, Backup, and Play. We will introduce each part as follows.

### Select

The selection is the first step of the Monte Carlo Tree Search. In a complete simulation, we start the simulation at the root node s_0, and reach a leaf node s_L at time-step L. (There are two kinds of leaf node s_L: first one is a node that has not been expanded and doesn't have child nodes, the second one satisfies the simulation finish condition, and the game is finished.)

In each time-step before time-step L, an action based on the statistic of Monte Carlo Tree Search will be selected by the following equation.
s_t=argmax┬a (Q(s_t,a)+U(s_t,a))
U(s,a)=c_puct P(s,a)√(∑_b▒〖N(s,b)〗)/(1+N(s,a))
Q(s_t,a) is the mean action value mentioned above.
U(s_t,a) is a value that represents the level of preferring exploration.
c_puct is a constant to adjust the tendency to explore.
Q(s_t,a) is affected by the performance of the action, U(s_t,a) is dependent on the visit count and prior probability, representing the exploration level. Consequently, this algorithm will prefer actions with low visit count, high prior probability, and high action value.
 In other words, the strategies both have exploration and exploitation tendencies (exploration means preferring non-explored action, and exploitation means preferring best-known action). The algorithm will make a trade-off between them, which will be affected by some parameters, for example, changing the number of c_puct will make a great difference.
