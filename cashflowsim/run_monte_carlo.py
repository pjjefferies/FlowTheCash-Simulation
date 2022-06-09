"""
Created on Mon Oct 19 22:20:09 2015.

@author: PaulJ
"""

import random
import cash_flow_rat_race_simulation as cfrrs

PROFESSIONS_FN = '../game_data/ProfessionsList.json'
STRATEGIES_FN = '../simulation_strategies/Strategies.json'


def single_run_repeat(a_profession, a_strategy, repetitions, verbose=False):
    """Run Cash Flow Simulations."""
    results = []

    for test in range(0, repetitions):
        random.seed(test)

        if verbose and test % (max(repetitions/5.0, 1000)) == 0:
            print("Profession:", a_profession.name,
                  "Strategy:", a_strategy.name,
                  "Running Test:", test, "test of",
                  repetitions)

        am_i_rich, am_i_broke, turn_counter = (
            cfrrs.cash_flow_rat_race_game_simulation(a_profession,
                                                     a_strategy,
                                                     verbose))
        results.append([test,
                        a_profession.name,
                        a_strategy.name,
                        am_i_rich,
                        am_i_broke,
                        turn_counter])

    return results


if __name__ == '__main__':
    import time
    import profession
    import strategy
    import csv
    import datetime

    VERBOSE = False
    TESTS_TO_RUN = 10
    profession_defs = profession.get_profession_defs(PROFESSIONS_FN)
    strategy_defs = strategy.get_strategy_defs(STRATEGIES_FN)
    no_sims = len(profession_defs) * len(strategy_defs)
    time_sim = True

    RESULTS_TITLE_LIST = ['test no.', 'professionName', 'strategyName',
                          'Am I Rich', 'Am I Poor', 'Turns']

    game_file_log_filename = "GameLog-" + datetime.datetime.now().strftime(
        '%Y%m%d-%H%M%S') + 'csv'
    with open(game_file_log_filename, "w", newline='') as output_file:
        writer = csv.writer(output_file, delimiter=",")
        writer.writerow(RESULTS_TITLE_LIST)
        start_time = time.time()
        if time_sim:
            single_start_time = time.time()
        for a_prof in iter(profession_defs):
            for strategy_to_eval in iter(strategy_defs):
                results_list_to_save = single_run_repeat(
                    a_profession=profession_defs[a_prof],
                    a_strategy=strategy_defs[strategy_to_eval],
                    repetitions=TESTS_TO_RUN,
                    verbose=VERBOSE)
                for game_result in results_list_to_save:
                    writer.writerow(game_result)
                if time_sim:
                    single_time = time.time() - single_start_time
                    print('Time per prof, strat combo:',
                          '{0:.1f}'.format(single_time),
                          "seconds.\nTotal Expected Time:",
                          "{0:.1f}".format((single_time*no_sims)))
                    time_sim = False
        output_file.close()

    print("Time to run", TESTS_TO_RUN, "tests for each profession/strategy:",
          '{0:.2f}'.format(time.time() - start_time), "seconds.")
