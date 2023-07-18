def update_leaderboards(player_puzzle, player_moves, player_name):
    '''
    Function: update_leaderboards
        Maintains and updates leaderboard.txt
    Parameters:
        player_puzzle -- name of player's current puzzle
        player_moves -- number of moves player solved puzzle in
        player_name -- name of player
    Does not return anything
    '''
    # opens leaderboard.txt and creates metadata list of
    # all puzzles and respective scores
    with open("leaderboard.txt") as leaderboard_file:
        temp_leaderboards = [x for x in leaderboard_file.read()\
            .strip().split("Puzzle: ")]
        leaderboards = []
        for each in temp_leaderboards[1:]:
            x = each.index("\n")
            puzzle_name = each[:x]
            each = each[x+1:].split("\n") # why is this x+1 and not x+2?
            first = []
            if each[-1] == "":
                for score in each[:-1]:
                    if score != "":
                        first.append(score.split(": "))
            else:
                for score in each:
                    first.append(score.split(": "))
            leaderboards.append([puzzle_name, first])

    # finds puzzle and determines where to rank score
    puzzle_found = 0
    place_found = 0
    for i in range(len(leaderboards)):
        if player_puzzle == leaderboards[i][0]:
            puzzle_found += 1
            for j in range(len(leaderboards[i][1])):
                # if score beats any existing score, adds score
                if player_moves < int(leaderboards[i][1][j][0]):
                    if j == 0:
                        leaderboards[i][1] = [[str(player_moves), \
                            player_name]] + leaderboards[i][1]
                        place_found += 1
                        break
                    else:
                        leaderboards[i][1] = [leaderboards[i][1][j-1]] + \
                            [[str(player_moves), player_name]] + \
                                leaderboards[i][1][j:]
                        place_found += 1
                        break
            # if score is last, places in last position
            if place_found == 0:
                leaderboards[i][1] = leaderboards[i][1] + \
                    [[str(player_moves), player_name]]
            leaderboards[i][1] = leaderboards[i][1][:10] # only takes top 10
    # adds new puzzle name if not in leaderboard.txt
    if puzzle_found == 0:
        leaderboards.append([player_puzzle, [[str(player_moves) + ": " + \
            player_name]]])

    # converts list of leaderboards back into text to write to leaderboard.txt
    for i in range(len(leaderboards)):
        scores = []
        for j in range(len(leaderboards[i][1])):
            scores.append(": ".join(leaderboards[i][1][j]))
        leaderboards[i][1] = "\n".join(scores) + "\n"
        leaderboards[i] = "Puzzle: " + "\n".join(leaderboards[i])
        
    with open("leaderboard.txt", "w") as leaderboard_file:
        leaderboard_file.write("".join(leaderboards))
