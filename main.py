from classWorldCupSimulator import WorldCupSimulator
from collections import Counter

# ==========================================================
# منوی اصلی با رعایت شرط مدیریت خطا
# ==========================================================
def main():
    sim = WorldCupSimulator('teams_2026_worldcup.csv')
    
    while True:
        print("\n" + "="*30)
        print("  شبیه‌ساز هوشمند جام جهانی")
        print("="*30)
        print("۱) بارگذاری تیم‌ها از فایل CSV")
        print("۲) انجام قرعه‌کشی گروه‌ها")
        print("۳) اجرای مرحله گروهی")
        print("۴) اجرای کامل جام و تعیین قهرمان")
        print("۵) شبیه‌سازی ۱۰۰۰ باره و گزارش شانس قهرمانی")
        print("۶) نمایش براکت آخرین مرحله حذفی")
        print("۷) خروج")
        
        choice = input("\nانتخاب شما: ")
        
        # مدیریت خطا: بررسی بارگذاری تیم‌ها برای تمام گزینه‌های ۲ تا ۶
        if choice in ['2', '3', '4', '5', '6'] and not sim.is_loaded:
            print("\n❌ خطا: ابتدا تیم‌ها را بارگذاری کنید (گزینه ۱).")
            continue

        if choice == '1':
            sim.load_teams()
        
        elif choice == '2':
            sim.perform_draw()
            
        elif choice == '3':
            sim.run_group_stage(verbose=True)
            
        elif choice == '4':
            sim.run_full_tournament(verbose=True)
            
        elif choice == '5':
            n = 1000 # مقدار ثابت طبق دستور جدید
            results = Counter()
            print(f"🔄 در حال انجام {n} شبیه‌سازی کامل (لطفاً کمی صبر کنید)...")
            for i in range(n):
                sim.perform_draw(verbose=False) 
                winner = sim.run_full_tournament(verbose=False)
                if winner: results[winner.name] += 1
            
            print(f"\n📈 گزارش ۱۰ تیم برتر در {n} شبیه‌سازی:")
            for team, count in results.most_common(10):
                print(f"{team:<15}: {count/n*100:>5.2f}% شانس")
                
        elif choice == '6':
            sim.show_bracket() if hasattr(sim, 'show_bracket') else sim.run_full_tournament(verbose=False) or print("داده‌ای موجود نیست")
            # متد نمایش براکت به کلاس اضافه شده است
            if sim.last_knockout_results:
                print("\n===== براکت آخرین مرحله حذفی =====")
                for stage, matches in sim.last_knockout_results:
                    print(f"\n--- {stage} ---")
                    for m in matches: print(m)
            else:
                print("❌ ابتدا باید یک بار جام را اجرا کنید (گزینه ۴).")
            
        elif choice == '7':
            print("👋 با آرزوی موفقیت برای شما!")
            break
        else:
            print("⚠️ گزینه نامعتبر!")

if __name__ == "__main__":
    main()


input()