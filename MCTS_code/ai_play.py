import pickle
from game_visual import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from PolicyNetwork import PolicyValueNet

# Play Chess With Human
class Human(object):
    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 4
    width, height = 6, 6
    model_file = './best_model/best_policy_' + str(width) + '_' + str(height) + '.pt'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)

        # ############### AI VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

        # best_policy = PolicyValueNet(width, height, model_file = model_file)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy

        policy_param = model_file
        best_policy = PolicyValueNet(width, height, policy_param)

        mcts_player1 = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)  # set larger n_playout for better performance

        mcts_player2 = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)  # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game.start_play(mcts_player1, mcts_player2, start_player=0, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
