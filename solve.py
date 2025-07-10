class HanoiSolver:
    def __init__(self, disk_count, peg_count=3):
        if peg_count < 3:
            raise ValueError("It takes at least 3 rods to solve the Tower of Hanoi.")
        self.disk_count = disk_count
        self.peg_count = peg_count
        self.moves = []

    def solve(self):
        self.moves.clear()
        if self.peg_count == 3:
            self._solve_three_pegs(self.disk_count, 1, 3, 2)
        else:
            pegs = list(range(1, self.peg_count + 1))
            self._solve_k_pegs(self.disk_count, pegs)
        return self.moves

    def _solve_three_pegs(self, n, source, target, auxiliary):
        if n == 1:
            self.moves.append((source, target))
        else:
            self._solve_three_pegs(n - 1, source, auxiliary, target)
            self.moves.append((source, target))
            self._solve_three_pegs(n - 1, auxiliary, target, source)

    def _solve_k_pegs(self, n, pegs):
        if n == 0:
            return
        if n == 1:
            if pegs[0] != pegs[-1]:
                self.moves.append((pegs[0], pegs[-1]))
            return
        if len(pegs) == 3:
            self._solve_three_pegs(n, pegs[0], pegs[-1], pegs[1])
            return

        # Heuristic choice of the number of disks to transfer
        t = n - int((2 * n + 1) ** 0.5) + 1
        t = max(1, min(n - 1, t))

        A = pegs[0]      # Source
        B = pegs[-1]     # Target
        others = pegs[1:-1]

        # We choose the first free rod to store t disks
        helper = None
        for p in others:
            if p != A and p != B:
                helper = p
                break
        if helper is None:
            helper = others[0]

        pegs_without_target = [A] + [p for p in others if p != helper] + [helper]
        pegs_without_source = [helper] + [p for p in others if p != helper] + [B]

        # Step 1: Move t disks to helper
        self._solve_k_pegs(t, pegs_without_target)

        # Step 2: Move n - t disks to target (3 rods: A, helper, B)
        self._solve_three_pegs(n - t, A, B, helper)

        # Step 3: Move t disks from helper to B
        self._solve_k_pegs(t, pegs_without_source)
    def get_moves(self):
        return self.moves


# For testing from the terminal
if __name__ == "__main__":
    n = int(input("Number of disks : "))
    k = int(input("Number of stems : "))
    solver = HanoiSolver(n, k)
    solver.solve()
    for move in solver.get_moves():
        print(f"{move[0]} -> {move[1]}")
    print(f"\n✔ Solved in {len(solver.get_moves())} moves with {k} rods.")

"""import math
from functools import lru_cache

class HanoiSolver:
    def __init__(self, disk_count, peg_count=3):
        if peg_count < 3:
            raise ValueError("Il faut au moins 3 tiges pour résoudre la Tour de Hanoï.")
        self.disk_count = disk_count
        self.peg_count = peg_count
        self.moves = []

    def solve(self):
        self.moves.clear()
        pegs = list(range(self.peg_count))
        self._frame_stewart(self.disk_count, pegs[0], pegs[-1], pegs[1:-1])
        return self.moves

    def _frame_stewart(self, n, src, tgt, aux_pegs):
        if n == 0:
            return
        if len(aux_pegs) == 0:
            self._solve_three_pegs(n, src, tgt, None)
            return

        k = self._find_optimal_k(n, len(aux_pegs) + 2)
        tmp = aux_pegs[0]  # On choisit toujours le premier peg auxiliaire pour stocker temporairement
        rest = aux_pegs[1:]

        # 1. Déplacer k disques sur tmp
        self._frame_stewart(k, src, tmp, [p for p in [tgt] + rest if p != tmp])

        # 2. Déplacer les (n-k) disques restants vers la cible
        self._frame_stewart(n - k, src, tgt, rest)

        # 3. Déplacer les k disques de tmp vers la cible
        self._frame_stewart(k, tmp, tgt, [p for p in [src] + rest if p != tmp])

    def _solve_three_pegs(self, n, src, tgt, aux):
        if n == 0:
            return
        if aux is None:
            raise ValueError("Il manque une tige auxiliaire pour la résolution à 3 tiges.")
        if n == 1:
            self.moves.append((src + 1, tgt + 1))
        else:
            self._solve_three_pegs(n - 1, src, aux, tgt)
            self.moves.append((src + 1, tgt + 1))
            self._solve_three_pegs(n - 1, aux, tgt, src)

    def get_moves(self):
        return self.moves

    @staticmethod
    @lru_cache(maxsize=None)
    def _find_optimal_k(n, r):
        # Formule optimisée (recommandée pour Frame-Stewart)
        return max(1, n - int(math.sqrt(2 * n + 1)) + 1)

# Test manuel depuis le terminal
if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(5000)

    n = int(input("Nombre de disques : "))
    p = int(input("Nombre de tiges : "))

    solver = HanoiSolver(n, p)
    solver.solve()
    for i, move in enumerate(solver.get_moves(), 1):
        print(f"{i}. {move[0]} → {move[1]}")
    print(f"\n✔ Résolu en {len(solver.get_moves())} coups avec {p} tiges.")"""
