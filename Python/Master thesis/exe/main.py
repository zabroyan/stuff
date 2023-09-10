from util import *
from models import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        agents, map = read_input(' '.join(arg for arg in sys.argv[1:]))  # input from command line
    else:
        agents, map = read_input()  # input via input() method

    R = Solution()
    R.agents.extend(agents)
    R.paths = [[None]] * len(R.agents)
    start = time.time()

    for agent in range(len(R.agents)):
        R.paths[agent] = find_path(map=map, root_node=R, a=R.agents[agent])  # find initial paths
    try:
        error = False
        R.calculate_cost()
    except IndexError:
        error = True
        print('Something went wrong during initial paths calculation.')
    if not error:
        print('\nInitial path:')
        R.print()

        S, calls, stats = find_solution(R, map, start)  # finding solution
        end = time.time()

        if S is None or S.cost == 0:
            print('\nNo solution')
        else:
            S.print()
            print_stats(S, map, start, end, calls, stats)
            if len(sys.argv) == 1:
                draw_map(map, S.paths, ask_input=True)
