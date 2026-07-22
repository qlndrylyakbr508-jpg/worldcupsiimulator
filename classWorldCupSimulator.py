import csv
import os
import random
from classteam import Team
from classgroup import Group
from classmatch import Match

# ==========================================================
# کلاس اصلی شبیه‌ساز
# ==========================================================
class WorldCupSimulator:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.all_teams = []
        self.groups = []
        self.last_knockout_results = []
        self.is_loaded = False
        self.is_drawn = False

    # مدیریت خطا در بارگذاری فایل CSV
    def load_teams(self):
        if not os.path.exists(self.csv_file):
            print(f"❌ خطا: فایل '{self.csv_file}' یافت نشد. لطفاً ابتدا فایل را در پوشه برنامه قرار دهید.")
            return

        self.all_teams = []
        try:
            with open(self.csv_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.all_teams.append(Team(row['name'], row['attack'], row['defense'], row['rank']))
            self.is_loaded = True
            print(f"✅ موفقیت: {len(self.all_teams)} تیم با موفقیت بارگذاری شدند.")
        except Exception as e:
            print(f"❌ خطا در پردازش فایل CSV: {e}")

    # قرعه‌کشی با بررسی بارگذاری تیم‌ها
    def perform_draw(self, verbose=True):
        if not self.is_loaded:
            print("❌ خطا: ابتدا تیم‌ها را بارگذاری کنید.")
            return
        
        sorted_teams = sorted(self.all_teams, key=lambda x: x.rank)
        pots = [sorted_teams[i:i+8] for i in range(0, 32, 8)]
        for p in pots: random.shuffle(p)
        
        self.groups = [Group(chr(65+i), [pots[j][i] for j in range(4)]) for i in range(8)]
        for t in self.all_teams: t.reset_stats()
        self.is_drawn = True
        if verbose: print("✅ قرعه‌کشی با موفقیت انجام شد.")

    # اجرای مرحله گروهی با بررسی بارگذاری
    def run_group_stage(self, verbose=True):
        if not self.is_loaded:
            print("❌ خطا: ابتدا تیم‌ها را بارگذاری کنید.")
            return None
        if not self.is_drawn:
            print("❌ خطا: ابتدا قرعه‌کشی را انجام دهید.")
            return None
        
        top_teams = []
        for g in self.groups:
            g.play_all_matches(verbose=verbose)
            ranked = g.get_ranking()
            top_teams.append(ranked)
            if verbose:
                print(f"\n📊 جدول گروه {g.name}:")
                for i, t in enumerate(ranked, 1): print(f"{i}. {t}")
        return top_teams

    # اجرای مرحله حذفی
    def run_knockout_stage(self, top_teams, verbose=True):
        self.last_knockout_results = []
        knockout_teams = []
        pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
        for g1, g2 in pairs:
            knockout_teams.append(top_teams[g1][0]); knockout_teams.append(top_teams[g2][1])
            knockout_teams.append(top_teams[g2][0]); knockout_teams.append(top_teams[g1][1])

        current_round = knockout_teams
        stages = ["یک‌هشتم نهایی", "یک‌چهارم نهایی", "نیمه‌نهایی", "فینال"]
        
        for stage in stages:
            if verbose: print(f"\n⚽ مرحله {stage}:")
            winners = []
            round_matches = []
            for i in range(0, len(current_round), 2):
                m = Match(current_round[i], current_round[i+1], is_knockout=True)
                m.play()
                if verbose: print(f"{m.details} -> برنده: {m.winner.name}")
                winners.append(m.winner)
                round_matches.append(m.details + f" (برنده: {m.winner.name})")
            
            self.last_knockout_results.append((stage, round_matches))
            current_round = winners
        return current_round[0]

    # اجرای کامل مسابقات
    def run_full_tournament(self, verbose=True):
        if not self.is_loaded:
            print("❌ خطا: ابتدا تیم‌ها را بارگذاری کنید.")
            return None
        if not self.is_drawn: self.perform_draw(verbose=False)
        top_teams = self.run_group_stage(verbose=verbose)
        if top_teams is None: return None
        winner = self.run_knockout_stage(top_teams, verbose=verbose)
        if verbose: print(f"\n🏆 قهرمان نهایی: {winner.name}")
        return winner
