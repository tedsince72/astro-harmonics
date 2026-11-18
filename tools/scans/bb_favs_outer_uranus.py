"""Favourites and Neptune / Sedna on natal Uranus (17 Nov 2026, Eddie: 'interesting to see across all the favourites and which planes and
families are involved'; read-only). Favourites taken from the result sections Eddie pasted into the watch files (27 of the 36 result races;
no favourite on file for Lingfield AW 14:35 2021, Haydock 13:45 2020, Beverley 14:05 2024, York 15:45 2024, Catterick 14:40 2022, Fontwell 15:30
2023, Newcastle AW 16:33 2021, Newton Abbot 15:25 2022, Chelmsford AW 13:20 2024). No favourite in these 27 won. Every S Neptune / S Sedna →
H / J Uranus line with a score, by group (favourite, winner, other runners): plane, family, score; holders at >= 80 / >= 50."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_fieldcheck_outer_uranus as O
FAV = {'20220716_doncaster_1845': 'Crackovia', '20220712_bath_1530': 'Overstate', '20220707_carlisle_1630': 'Million Thanks',
       '20220616_ripon_1525': 'Bollin Joan', '20220613_nottingham_1750': 'Gidwa', '20220603_bath_1750': 'Soi Dao',
       '20220601_nottingham_1530': 'Princess Shabnam', '20220510_sedgefield_1500': 'Wheres Maud Gone',
       '20220509_musselburgh_1550': 'The Thin Blue Line', '20220507_haydock_1718': 'Out From Under', '20220504_kelso_1450': 'Spanish Present',
       '20220420_perth_1610': 'Zambella', '20220414_newmarket_1535': 'Masekela', '20220406_lingfield_aw_1425': "Judy's Park",
       '20220323_ffos_las_1725': 'You Say Nothing', '20220321_wincanton_1420': 'Ballyblack', '20220318_wolverhampton_aw_2030': 'Coase',
       '20220318_doncaster_1440': 'Oot Ma Way', '20220311_newcastle_1540': 'Edmond Dantes', '20220223_doncaster_1600': 'Half Track',
       '20211014_carlisle_1355': 'Gold Des Bois', '20220219_haydock_1405': 'Molly Ollys Wishes', '20220215_newcastle_aw_1640': 'Onesmoothoperator',
       '20220129_doncaster_1410': 'Miranda', '20220123_lingfield_1500': 'Dashel Drasher', '20220105_ffos_las_1420': 'Gustavian',
       '20220102_newcastle_aw_1330': 'Good Effort', '20211216_exeter_1415': 'Maskada',
       '20211211_newcastle_aw_1420': 'Coltrane', '20211205_huntingdon_1352': 'Allmankind', '20211204_sandown_1425': 'Chacun Pour Soi', '20211126_newbury_1350': 'Mister Coffey', '20211119_catterick_1505': 'Reve', '20211112_newcastle_aw_1540': 'Rabat', '20211112_newcastle_aw_1220': 'Buxted Too',
       '20211020_fontwell_1505': 'Dorking Lad'}


def main():
    grp = {'favourite': [], 'winner': [], 'other': []}
    holders = {g: {0: 0, 50: 0, 80: 0, 'n': 0} for g in grp}
    print('# Favourites: S Neptune / S Sedna on natal Uranus\n')
    for race, win in O.RACES:
        if race not in FAV:
            continue
        R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        fav = next(r for r in R if FAV[race] in r)
        for run, D in R.items():
            g = 'favourite' if run == fav else 'winner' if win in run else 'other'
            ls = (O.lines(D, 'Neptune') + O.lines(D, 'Sedna')) if 'Uranus' in D else []
            holders[g]['n'] += 1
            for c in (0, 50, 80):
                holders[g][c] += any(r['sc'] >= c for r in ls)
            for r in ls:
                grp[g].append((race, run, r))
            if g == 'favourite':
                print(f"- {race} {run}: " + ('; '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} {r['fam']} ({r['sc']})" for r in ls) or 'none'))
    print('\n## Runners holding a line (27 races): any score / >= 50 / >= 80 of runners')
    for g, h in holders.items():
        print(f"- {g}: {h[0]} / {h[50]} / {h[80]} of {h['n']}  ({h[80] / h['n'] * 100:.0f} % at >= 80)")
    for c in (50, 80):
        print(f'\n## Lines scoring >= {c} by group: body, chart, plane, family')
        for g, L in grp.items():
            L = [x for x in L if x[2]['sc'] >= c]
            tab = {}
            for race, run, r in L:
                y = r['line'].split('→')[0][2:].strip(); ch = r['line'].split('→')[1].strip()[0]
                for key in (f'{y}', f'chart {ch}', f"plane {r['plane']}", f"family {r['fam']}"):
                    tab[key] = tab.get(key, 0) + 1
            print(f"- {g} ({len(L)} lines): " + ', '.join(f'{k} {v}' for k, v in sorted(tab.items())))


if __name__ == '__main__':
    main()
