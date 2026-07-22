import random
import numpy as np

# ==========================================================
# کلاس مدیریت مسابقه بین دو تیم
# ==========================================================
class Match:
    # مقداردهی اولیه مسابقه
    def __init__(self, team1, team2, is_knockout=False):
        self.team1 = team1
        self.team2 = team2
        self.is_knockout = is_knockout
        self.goals1 = 0
        self.goals2 = 0
        self.lambda1 = 0.0
        self.lambda2 = 0.0
        self.winner = None
        self.details = ""

    # شبیه‌سازی بازی با فرمول تصویر پروژه
    def play(self):
        # فرمول محاسبه لامبدا بر اساس توان حمله و دفاع (تصویر پروژه)
        self.lambda1 = (self.team1.attack / 100) * 1.5 + (1 - self.team2.defense / 100) * 0.8
        self.lambda2 = (self.team2.attack / 100) * 1.5 + (1 - self.team1.defense / 100) * 0.8
        
        self.goals1 = np.random.poisson(self.lambda1)
        self.goals2 = np.random.poisson(self.lambda2)

        if not self.is_knockout:
            self.update_group_stats()
        else:
            if self.goals1 > self.goals2:
                self.winner = self.team1
            elif self.goals2 > self.goals1:
                self.winner = self.team2
            else:
                self.simulate_extra_time()
        
        self.details = f"{self.team1.name} {self.goals1} - {self.goals2} {self.team2.name}"

    # به‌روزرسانی امتیازات و جدول گروهی
    def update_group_stats(self):
        self.team1.goals_for += self.goals1
        self.team1.goals_against += self.goals2
        self.team2.goals_for += self.goals2
        self.team2.goals_against += self.goals1
        
        if self.goals1 > self.goals2:
            self.team1.points += 3; self.team1.wins += 1; self.team2.losses += 1
        elif self.goals2 > self.goals1:
            self.team2.points += 3; self.team2.wins += 1; self.team1.losses += 1
        else:
            self.team1.points += 1; self.team2.points += 1
            self.team1.draws += 1; self.team2.draws += 1

    # شبیه‌سازی وقت‌های اضافه (0.33 برابر لامبدای اصلی)
    def simulate_extra_time(self):
        extra_lambda1 = self.lambda1 * 0.33
        extra_lambda2 = self.lambda2 * 0.33
        self.goals1 += np.random.poisson(extra_lambda1)
        self.goals2 += np.random.poisson(extra_lambda2)
        
        if self.goals1 > self.goals2:
            self.winner = self.team1
        elif self.goals2 > self.goals1:
            self.winner = self.team2
        else:
            self.simulate_penalties()

    # شبیه‌سازی پنالتی‌ها و پنالتی‌های ناگهانی (Sudden Death)
    def simulate_penalties(self):
        p1 = max(0.6, min(0.9, 0.75 + (self.team1.attack - self.team2.defense) / 250))
        p2 = max(0.6, min(0.9, 0.75 + (self.team2.attack - self.team1.defense) / 250))
        
        sc1, sc2 = 0, 0
        for _ in range(5):
            if random.random() < p1: sc1 += 1
            if random.random() < p2: sc2 += 1
            
        if sc1 == sc2: # پنالتی ناگهانی
            while True:
                t1_goal = random.random() < p1
                t2_goal = random.random() < p2
                if t1_goal: sc1 += 1
                if t2_goal: sc2 += 1
                if t1_goal != t2_goal: break
                    
        self.winner = self.team1 if sc1 > sc2 else self.team2
        self.details += f" (پنالتی: {sc1}-{sc2})"