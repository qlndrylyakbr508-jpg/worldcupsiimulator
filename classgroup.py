import itertools
from classmatch import Match

# ==========================================================
# کلاس مدیریت گروه‌ها
# ==========================================================
class Group:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

    def play_all_matches(self, verbose=False):
        if verbose: print(f"\n--- بازی‌های گروه {self.name} ---")
        for t1, t2 in itertools.combinations(self.teams, 2):
            m = Match(t1, t2)
            m.play()
            if verbose: print(m.details)

    def get_ranking(self):
        self.teams.sort(key=lambda t: (t.points, t.goal_difference(), t.goals_for), reverse=True)
        return self.teams
