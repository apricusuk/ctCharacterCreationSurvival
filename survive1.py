#!/usr/bin/env python3
'''
survive1.py

Using random character stat generation.
According to LBB1 (1981) Characters and Combat.
Generates counts of reason for ending service career during character creation for each service at each term.  

reference: https://www.farfuture.net/

The Traveller game in all forms is owned by Far Future Enterprises. Copyright 1977 – 2020 Far Future Enterprises. 
Traveller is a registered trademark of Far Future Enterprises. Far Future permits web sites and fanzines for this game, 
provided it contains this notice, that Far Future is notified, and subject to a withdrawal of permission on 90 days notice. 
The contents of this page are for personal, non-commercial use only. Any use of Far Future Enterprises’s copyrighted 
material or trademarks anywhere on this web page and its file should not be viewed as a challenge to those copyrights 
or trademarks. In addition, this program/file on this site cannot be republished or distributed without the consent 
of the author who contributed it.
'''

from collections import Counter
import numbers
import random
import sys

# set DEBUG to False by default
DEBUG = False

# default number of runs, which is not enough to be statistically significant
RUNS = 10

def d(n=1):
    """
    roll a number (n default 1) of d6

    test 1d6 values range from 1 to 6 inclusive
    >>> m=100000
    >>> all(1 <= d() <= 6 for _ in range(m))
    True

    test 3d6 values range from 3 to 18 inclusive
    >>> m=100000
    >>> all(3 <= d(3) <= 18 for _ in range(m))
    True

    test all values are present
    >>> m=100000
    >>> c=Counter(d() for _ in range(m))
    >>> set(c) == set(range(1,7))
    True

    test the mean of enough values is the median
    >>> m=100000
    >>> c=Counter(d() for _ in range(m))
    >>> t=0
    >>> for k,v in c.items():
    ...     t+=(k*v)
    >>> print(round(t/m))
    3

    """
    roll = random.randint(1,6)
    if n==1:
        return roll
    x=0
    while n>0:
        x+=d()
        n-=1
    if DEBUG: print(f"    roll {x:2}")
    return x

def d2():
    """
    roll 2d6

    test 2d6 values range from 2 to 12 inclusive
    >>> m=100000
    >>> all(2 <= d2() <= 12 for _ in range(m))
    True

    test all values are present
    >>> m=100000
    >>> c=Counter(d2() for _ in range(m))
    >>> set(c) == set(range(2,13))
    True

    test the mean of enough values is the median
    >>> m=100000
    >>> c=Counter(d2() for _ in range(m))
    >>> t=0
    >>> for k,v in c.items():
    ...     t+=(k*v)
    >>> print(round(t/m))
    7
    """
    return d(2)

# keys and strings
Str = "Str"
Dex = "Dex"
End = "End"
Int = "Int"
Edu = "Edu"
Soc = "Soc"
Reason = "reason"
Skills = "skill_count"
Terms = "terms"
Rank = "rank"
Benefits = "benefits"

navy = "navy"
marines = "marines"
army = "army"
scouts = "scouts"
merchant = "merchant"
other = "other"

enlistment = "enlistment"
aging = "aging"
survival = "survival"
reenlistment = "reenlistment"

def genStats():
    '''generate initial stats'''
    if DEBUG: print(f"[+] generate stats")
    return {Str:d2(), Dex:d2(), End:d2(), Int:d2(), Edu:d2(), Soc:d2()}

def doEnlist(service, stats):
    '''try to enlist'''
    if DEBUG: print(f"[+] enlistment {service} : {stats}")
    roll = d2()
    if service == navy:
        if stats[Int] >= 8: roll += 1
        if stats[Edu] >= 9: roll += 2
        if roll >= 8: return True
    elif service == marines:
        if stats[Int] >= 8: roll += 1
        if stats[Str] >= 8: roll += 2
        if roll >= 9: return True
    elif service == army:
        if stats[Dex] >= 6: roll += 1
        if stats[End] >= 5: roll += 2
        if roll >= 5: return True
    elif service == scouts:
        if stats[Int] >= 6: roll += 1
        if stats[Str] >= 8: roll += 2
        if roll >= 7: return True
    elif service == merchant:
        if stats[Str] >= 7: roll += 1
        if stats[Int] >= 6: roll += 2
        if roll >= 7: return True
    elif service == other:
        if roll >= 3: return True
    if DEBUG: print(f"[!] failed enlistment")
    return False

def doSurvive(service, stats):
    '''check for survival'''
    if DEBUG: print(f"[+] survival {service} : {stats}")
    roll = d2()
    if service == navy:
        if stats[Int] >= 7: roll += 2
        if roll >= 5: return True
    elif service == marines:
        if stats[End] >= 8: roll += 2
        if roll >= 6: return True
    elif service == army:
        if stats[Edu] >= 6: roll += 2
        if roll >= 5: return True
    elif service == scouts:
        if stats[End] >= 9: roll += 2
        if roll >= 7: return True
    elif service == merchant:
        if stats[Int] >= 7: roll += 2
        if roll >= 5: return True
    elif service == other:
        if stats[Int] >= 9: roll += 2
        if roll >= 5: return True
    if DEBUG: print(f"[!] failed survival")
    return False

def doCommission(service, stats):
    '''try for comission'''
    if DEBUG: print(f"[+] commission {service} : {stats}")
    roll = d2()
    if service == navy:
        if stats[Soc] >= 10: roll += 1
        if roll >= 8: return True
    elif service == marines:
        if stats[Edu] >= 7: roll += 1
        if roll >= 9: return True
    elif service == army:
        if stats[End] >= 7: roll += 1
        if roll >= 5: return True
    elif service == merchant:
        if stats[Int] >= 6: roll += 1
        if roll >= 4: return True
    if DEBUG: print(f"[!] failed commission")
    return False

def doPromotion(service, stats):
    '''try for promotion'''
    if DEBUG: print(f"[+] promotion {service} : {stats}")
    roll = d2()
    if service == navy:
        if stats[Edu] >= 8: roll += 1
        if roll >= 8: return True
    elif service == marines:
        if stats[Soc] >= 8: roll += 1
        if roll >= 9: return True
    elif service == army:
        if stats[Edu] >= 7: roll += 1
        if roll >= 6: return True
    elif service == merchant:
        if stats[Int] >= 9: roll += 1
        if roll >= 10: return True
    if DEBUG: print(f"[!] failed promotion")
    return False

def doReenlist(service, stats):
    '''attempt to reenlist'''
    if DEBUG: print(f"[+] reenlistment {service} : {stats}")
    roll = d2()
    if roll == 12: return True
    if stats[Terms] < 7:
        if service == navy:
            if roll >= 6: return True
        elif service == marines:
            if roll >= 6: return True
        elif service == army:
            if roll >= 7: return True
        elif service == scouts:
            if roll >= 3: return True
        elif service == merchant:
            if roll >= 4: return True
        elif service == other:
            if roll >= 5: return True
    if DEBUG: print(f"[!] failed reenlistment")
    return False

def doBenefits(stats):
    benefits = 0
    if stats[Reason] == reenlistment:
        benefits = stats[Terms]
        if stats[Rank] >= 5:
            benefits+=3
        elif stats[Rank] >= 3:
            benefits+=2
        elif stats[Rank] >=1:
            benefits+=1
    stats[Benefits] = benefits
    return stats

def getPersonalDevelopment(service):
    ''' get serive specific personal development table for stats'''
    if service == navy: return "SDEIUO"
    if service == marines: return "SDEKKK"
    if service == army: return "SDEKUK"
    if service == scouts: return "SDEIUK"
    if service == merchant: return "SDESKK"
    if service == other: return "SDEKKX"
    return None

def incrementStat(stats, stat):
    ''' increment a stat '''
    if DEBUG: print(f"        incrementing {stat}")
    stats[stat] += 1
    return stats

def decrementStat(stats, stat):
    ''' decrement a stat '''
    if DEBUG: print(f"        deccrementing {stat}")
    stats[stat] -= 1
    return stats

def modifyStat(stats, statletter):
    '''
    translate a stat letter for personal development to a change in 
    stat (or a skill)
    '''
    if statletter == 'S': return incrementStat(stats, Str)
    elif statletter == 'D': return incrementStat(stats, Dex)
    elif statletter == 'E': return incrementStat(stats, End)
    elif statletter == 'I': return incrementStat(stats, Int)
    elif statletter == 'U': return incrementStat(stats, Edu)
    elif statletter == 'O': return incrementStat(stats, Soc)
    elif statletter == 'X': return decrementStat(stats, Soc)
    elif statletter == 'K': 
        stats[Skills]+=1
        if DEBUG: print("    adding a skill")

    return stats

def doPersonalDevelopment(service, stats):
    '''
    Take a roll on the personal development table
    '''
    if DEBUG: print("    doing personal development")
    develop = getPersonalDevelopment(service)
    if develop is not None:
        roll = d()
        stat = develop[roll - 1]
        stats = modifyStat(stats, stat)
    return stats

def doTerm(service, stats):
    '''
    do one term
        service - string one of navy, marines, army, scouts, merchant, other
        stats - the current stats dictionary
    
    returns
        boolean - true if
        stats - the updated stats dictionary
    '''
    if DEBUG: print()
    if DEBUG: print(f"[*] start term {stats[Terms]}")
    if not doSurvive(service, stats):
        stats[Reason] = survival
        return False,stats

    skillrolls = 1
    if stats[Terms] == 1 or service == scouts:
        skillrolls += 1

    if service is not scouts and service is not other:
        if stats[Rank] < 1:
            if doCommission(service, stats):
                stats[Rank] = 1
                skillrolls += 1

    if service is not scouts and service is not other:
        if stats[Rank] > 0:
            if (stats[Rank] < 6 or (service is merchant and stats[Rank] < 5)):
                if doPromotion(service, stats):
                    stats[Rank] += 1
                    skillrolls += 1

    if DEBUG: print(f"    {skillrolls} skill rolls this turn")

    # one roll on personal development if they have 2+ rolls?
    if skillrolls > 1:
        stats = doPersonalDevelopment(service, stats)
        skillrolls -= 1
    
    # take any more rolls randomly amongst available tables?
    while skillrolls > 0:
        if stats[Edu] >= 8:
            skillstable = random.randint(1,4)
        else:
            skillstable = random.randint(1,3)

        if skillstable == 1:
            stats = doPersonalDevelopment(service, stats)
        else:
            if DEBUG: print("    adding a skill")
            stats[Skills] += 1
        skillrolls -= 1

    alive, stats = doAging(stats)
    if not alive:
        stats[Reason] = aging
        return False, stats

    if not doReenlist(service, stats):
        stats[Reason] = reenlistment
        return False,stats

    stats[Terms] += 1

    return True,stats

def doAging(stats):
    ''' Check for and apply aging effects '''
    if DEBUG: print(f"[+] aging {stats}")
    if stats[Terms] < 4:
        return True, stats
    elif stats[Terms] < 8:
        if d2() < 8:
            stats = decrementStat(stats, Str)
        if d2() < 7:
            stats = decrementStat(stats, Dex)
        if d2() < 8:
            stats = decrementStat(stats, End)
    elif stats[Terms] < 12:
        if d2() < 9:
            stats = decrementStat(stats, Str)
        if d2() < 8:
            stats = decrementStat(stats, Dex)
        if d2() < 9:
            stats = decrementStat(stats, End)
    else:
        if d2() < 9:
            stats = decrementStat(stats, Str)
            stats = decrementStat(stats, Str)
        if d2() < 9:
            stats = decrementStat(stats, Dex)
            stats = decrementStat(stats, Dex)
        if d2() < 9:
            stats = decrementStat(stats, End)
            stats = decrementStat(stats, End)
        if d2() < 9:
            stats = decrementStat(Int)
    if DEBUG: print(f"[-] aging {stats}")
    for stat in (Str,Dex,End,Int):
        if stats[stat] < 1:
            if d2() >= 8:
                if DEBUG: print(f"[!] survived aging crisis {stat} is {stats[stat]}")
                stats[stat] = 1
            else:
                if DEBUG: print(f"[!] failed aging crisis {stat} is {stats[stat]}")
                return False, stats
    return True, stats

def doCareer(service):
    ''' do a career '''
    stats = genStats()
    stats[Terms] = 0
    stats[Rank] = 0
    if not doEnlist(service, stats):
        stats[Reason] = enlistment
        return stats
    else:
        stats[Skills] = 0
    stillgoing = True
    stats[Terms] += 1
    while stillgoing:
        keepgoing,stats = doTerm(service, stats)
        if not keepgoing:
            return stats

def surviveResultsToCsv(results):
    '''
    convert career results dictionary to comma separated variable string with heading
    this is given in number that failed the roll on that term
    enlistment test occurs on term 0 only
    '''
    csv = f"{Terms},{enlistment},{survival},{aging},{reenlistment}"
    for term in sorted(list(results.keys())):
        line = f"{term},"
        if enlistment in results[term]:
            line += f"{results[term][enlistment]}"
        line += ","
        if survival in results[term]:
            line += f"{results[term][survival]}"
        line += ","
        if aging in results[term]:
            line += f"{results[term][aging]}"
        line += ","
        if reenlistment in results[term]:
            line += f"{results[term][reenlistment]}"
        csv += f"\n{line}"
    return csv

def benefitsResultsToCsv(results):
    '''
    convert results dictionary to comma separated variable string with heading
    this gives number that received a certain number of benefit rolls per term
    '''
    maxBenefits = 0
    for term in results:
        for benefits in results[term]:
            if benefits > maxBenefits:
                maxBenefits = benefits

    csv = f"{Terms},"
    for benefits in range(1, maxBenefits + 1):
        csv += f"{benefits},"
    csv = csv[:-1]

    for term in sorted(list(results.keys())):
        line = f"{term},"
        for benefits in range(1, maxBenefits + 1):
            if benefits in results[term]:
                line += f"{results[term][benefits]},"
            else:
                line += "0,"
        line = line[:-1]
        csv += f"\n{line}"
    return csv

def printUsage():
    '''print usage message with current variable values'''
    print(f"usage: {sys.argv[0]} [service] [count] [debug]")
    print(f"    where service is one of {navy}, {marines}, {army}, {scouts}, {merchant}, {other}, all")
    print(f"    optional count is number of runs (default {RUNS})")
    print(f"    optional debug flag is 'debug' (default {DEBUG})")

def doService(service):
    surviveResults = dict()
    benefitsResults = dict()
    for _ in range(RUNS):
        stats = doCareer(service)
        stats = doBenefits(stats)
        term = stats[Terms]
        reas = stats[Reason]
        if DEBUG: print( f"failed {reas} in term {term}, {stats}" )
        if term not in surviveResults.keys(): surviveResults[term] = dict()
        if reas not in surviveResults[term]: surviveResults[term][reas] = 0
        surviveResults[term][reas] += 1

        bene = stats[Benefits]
        if term not in benefitsResults.keys(): benefitsResults[term] = dict()
        if bene not in benefitsResults[term]: benefitsResults[term][bene] = 0
        benefitsResults[term][bene] += 1

        if DEBUG: 
            print(surviveResults)
            print(benefitsResults)
            print()
            if term > 7 and stats[Reason] is reenlistment:
                print(f"{term} : {stats}")

    surviveCsv = surviveResultsToCsv(surviveResults)
    print("survival results")
    print(surviveCsv)
    print()

    print("benefits results")
    benefitsCsv = benefitsResultsToCsv(benefitsResults)
    print(benefitsCsv)
    print()

if __name__=="__main__":
    argc = len(sys.argv)
    if argc < 2 or argc > 4:
        printUsage()
        sys.exit(1)

    service = sys.argv[1]
    services = (navy,marines,army,scouts,merchant,other)
    if service not in services and not service == "all":
        print(f"unknown service argument {service}")
        printUsage()
        sys.exit(2)

    if argc > 3:
        debug = sys.argv[3]
        if debug != "debug":
            print(f"if you wish to enable debug you must use'debug' for debug flag - beware debug is verbose")
            printUsage()
            sys.exit(4)
        else:
            DEBUG = True
    
    if argc > 2:
        count = sys.argv[2]
        if not count.isnumeric():
            if count != "debug":
                print(f"{count} is not numeric")
                printUsage()
                sys.exit(3)
            else:
                DEBUG = True
        else:
            RUNS = int(count)

    if service == "all":
        for serv in services:
            print(f"{serv}")
            doService(serv)
            print()
    else:
        doService(service)


