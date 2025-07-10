from solve import HanoiSolver

def init_game(disk_count, peg_count):
    pegs = [[] for _ in range(peg_count)]
    pegs[0] = list(reversed(range(disk_count)))  # All discs on the first rod
    return pegs

def display_game(pegs):
    print("\nCurrent state of the stems :")
    max_height = max(len(peg) for peg in pegs)
    for level in reversed(range(max_height)):
        row = ""
        for peg in pegs:
            if level < len(peg):
                row += f"  [{peg[level]}]  "
            else:
                row += "   |   "
        print(row)
    print(" ".join(f" T{i+1} " for i in range(len(pegs))))
   

def is_valid_move(pegs, source, target):
    if not pegs[source]:
        return False
    if not pegs[target]:
        return True
    return pegs[source][-1] < pegs[target][-1]

def make_move(pegs, source, target):
    if is_valid_move(pegs, source, target):
        disk = pegs[source].pop()
        pegs[target].append(disk)
        return True
    return False

def is_game_won(pegs, disk_count):
    return any(len(peg) == disk_count and i != 0 for i, peg in enumerate(pegs))

def play_game():
    print("Welcome to the Tower of Hanoi game (console)")
    disk_count = int(input("Number of disks : "))
    peg_count = int(input("Number of stems : "))
    pegs = init_game(disk_count, peg_count)

    while True:
        display_game(pegs)
        cmd = input("\nCommand (ex: 1 3 to move from T1 to T3, or 'solve') : ")

        if cmd.lower() == "solve":
            solver = HanoiSolver(disk_count, peg_count)
            moves = solver.solve()
            for i, move in enumerate(moves):
                print(f"{i+1}. {move[0]} → {move[1]}")
            print(f"Solved in {len(moves)} moves.")
            break

        try:
            src, tgt = map(int, cmd.strip().split())
            if not (1 <= src <= peg_count and 1 <= tgt <= peg_count):
                print("Invalid stem numbers.")
                continue
            if not make_move(pegs, src-1, tgt-1):
                print(" No movement (small disc rule).")
        except:
            print("Invalid input. Expected example: 1 3")

        if is_game_won(pegs, disk_count):
            display_game(pegs)
            print("Congratulations, you won!!")
            break

if __name__ == "__main__":
    play_game()
