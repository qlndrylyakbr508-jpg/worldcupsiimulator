# ==========================================================
# کلاس تیم‌های فوتبال
# ==========================================================
class Team:
    # مقداردهی اولیه مشخصات تیم
    def __init__(self, name, attack, defense, rank):
        self.name = name
        self.attack = int(attack)
        self.defense = int(defense)
        self.rank = int(rank)
        self.reset_stats()

    # محاسبه تفاضل گل تیم
    def goal_difference(self):
        return self.goals_for - self.goals_against

    # بازنشانی آمار تیم برای شبیه‌سازی جدید
    def reset_stats(self):
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    # نمایش متنی اطلاعات تیم
    def __repr__(self):
        return f"{self.name:<15} | Pts: {self.points:<2} | GD: {self.goal_difference():<3} | GF: {self.goals_for:<2}"