from game import Game
from helpers import csv_to_lineup
from season import Season
from itertools import permutations
from copy import deepcopy
from random import shuffle
from math import ceil
import sys


# simulate season for every permutation of lineup and rank lineups
# from most runs/game to least runs/game
def sim_and_rank_seasons(lineup, num_seasons=1000):
    ordered_seasons = []  # stores seasons in descending order by runs/game
    counter = 0
    counter_modulo = ceil(362880.0/num_seasons)

    lineup_copy = lineup[:]
    shuffle(lineup_copy)  # to ensure random selection

    for l in permutations(lineup_copy):
        if counter % counter_modulo == 0:
            # play full season with l
            s = Season(lineup=deepcopy(list(l)), num_games=162)
            s.play_season()
            ordered_seasons.append(s)
            print counter

        counter += 1

    ordered_seasons.sort(key=lambda s: s.get_runs_per_game())

    return ordered_seasons

"""
Returns:
1) sample top 3 best lineups
2) player, position, runs/game table
2b) names_to_index table
in a tuple

Note: the position is indexed 0-8, but real positions are 1-9
Note: cannot deal with lineups with duplicate names!  Must have unique named players!
"""


def ordered_seasons_expl(ordered_seasons):
    sample_best_lineups = [ordered_seasons[0], ordered_seasons[1], ordered_seasons[2]]
    best_season = ordered_seasons[0]
    best_lineup = best_season.get_lineup()
    lineup_size = len(best_lineup)
    name_to_index = {}  # dictionary converting names to an index

    for i, p in enumerate(best_lineup):
        if p in name_to_index:
            print "Error: cannot use duplicate names in lineup!"
            sys.exit()
        name_to_index[p.get_name()] = i

    print name_to_index
    #make list of lineups and associated runs per game (will be in descending run order)
    lineup_runs_list = []
    for s in ordered_seasons:
        lineup_runs_list.append([s.get_lineup(), s.get_runs_per_game()])

    #create matrix of players by batting position with [runs, games] in each entry
    temp_runs_matrix = [[[0, 0] for x in range(lineup_size)] for y in range(lineup_size)]

    for [lineup, runs] in lineup_runs_list:
        for position, player in enumerate(lineup):
            temp_runs_matrix[name_to_index[player.get_name()]][position][0] += runs
            temp_runs_matrix[name_to_index[player.get_name()]][position][1] += 1.0

    # contains runs/game in eacn entry instead of [runs, games]
    runs_matrix = [[[0, 0] for x in range(lineup_size)] for y in range(lineup_size)]
    for i, row in enumerate(temp_runs_matrix):
        for j, col in enumerate(row):
            if (col[1] < .001):  # i.e. dividing by 0
                runs_matrix[i][j] = 0.0
            else:
                runs_matrix[i][j] = col[0]/float(col[1])

    return (sample_best_lineups, runs_matrix, name_to_index)


def main():
    # lineup = csv_to_lineup('bos_2004_ws_g2.csv')
    lineup = csv_to_lineup('bos_2015_random_order.csv')
    print "***And the lineup is...***"
    for elem in lineup:
        print str(elem) + ", " + str(elem.get_attr_obj().get_attr_dic())
    print "**************************"

    # num_sim = 162
    # total_score = 0

    # for _ in range(num_sim):
    #     g = Game(live_update=True, game_summary=True, lineup=lineup)
    #     g.play_ball()
    #     total_score += g.get_score()

    # print total_score/float(num_sim)

    # s = Season(lineup=lineup)
    # s.play_season()
    # s.print_season_summary()
    # print "Runs per game: " + str(s.get_runs_per_game())

    ordered_seasons = sim_and_rank_seasons(lineup=lineup, num_seasons=10)
    for s in ordered_seasons:
        print s.print_season_summary()
        print s.get_runs_per_game()
    print "Num Seasons:" + str(len(ordered_seasons))

    good_tup = ordered_seasons_expl(ordered_seasons)
    print good_tup


if __name__ == "__main__":
    main()
