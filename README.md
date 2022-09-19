# Classic Traveller Character Creation Survival script

> The Traveller game in all forms is owned by Far Future Enterprises. Copyright 1977 – 2022 Far Future Enterprises. Traveller is a registered trademark of Far Future Enterprises. Far Future permits web sites and fanzines for this game, provided it contains this notice, that Far Future is notified, and subject to a withdrawal of permission on 90 days notice. The contents of this page are for personal, non-commercial use only. Any use of Far Future Enterprises’s copyrighted material or trademarks anywhere on this web page and its file should not be viewed as a challenge to those copyrights or trademarks. In addition, this program/file on this site cannot be republished or distributed without the consent of the author who contributed it.

This python3 script runs through character creation rules from LBB1 (1981) Characters and Combat.  
It is an attempt to determine the likelihood of a character surviving character creation for particular careers.  
It also generates a numbers of runs that gained a number of benefits for each term on failing reenlistment.  

It follows some simple logic:
1. for each run the charactistics are randomly generated
2. for each term if reenlistment is succesful then the run continues to the next term i.e. no option to voluntarily muster out is given
3. if more than one skill is awarded in any term then one role (at least) is made on the personal development table

## usage
```
python3 survive1.py <service> <runs> <debug>
```
- service is required argument; one of navy, marines, army, scounts, merchant, other or all - all indicates that number of runs are made for every service
- runs is optional, with a default of 10 (which is not statistically significant)
- debug is optional debug flag which must be 'debug' if wanted, it is quite verbose

### example usage
```
python3 survive1.py marines
python3 survive1.py scouts 100000
python3 survive1.py army debug
python3 survive1.py all 1 debug
```

## output
Output for survival are given as comma separated variables of counts for those that fail enlistement, survival, aging and reenlistment at each term.
Output for benefits is given as comma separated variables of counts for a number of benefits at each term.  

## enlistment
A set of results for 1 million runs against each career indicate the likelihood for enlisting as

| service | likelihood of enlistment |
| ------- | ------------------------ |
| navy | 56 % |
| marines | 46 % |
| army | 98 % |
| scouts | 77 % |
| merchant | 82 % |
| other | 97 % |

## survival
Of those that successfully enlist, the following indicates the reason for leaving the service at each term (as a percentage (to two significant figures) of those that enlist).

### Navy
| terms | failed survival | failed aging | failed reenlistment |
| -- | -- | -- | -- |
| 1 |	8.0 | 0.0 | 26 |
| 2 | 4.7 | 0.0 | 17 |
| 3 | 2.9 | 0.0 | 12 |
| 4 | 1.8 | 0.0 | 7.9 |
| 5 | 1.1  | 0.12 | 5.4 |
| 6 | 0.69 | 0.21 | 3.7 |
| 7 | 0.45 | 0.22 | 8.5 |
| 8 | 0.011 | 0.011 | 0.22 |
| 9 | 0.00036 | 0.00053 | 0.0064 |




> The Traveller game in all forms is owned by Far Future Enterprises. Copyright 1977 – 2022 Far Future Enterprises. Traveller is a registered trademark of Far Future Enterprises. Far Future permits web sites and fanzines for this game, provided it contains this notice, that Far Future is notified, and subject to a withdrawal of permission on 90 days notice. The contents of this page are for personal, non-commercial use only. Any use of Far Future Enterprises’s copyrighted material or trademarks anywhere on this web page and its file should not be viewed as a challenge to those copyrights or trademarks. In addition, this program/file on this site cannot be republished or distributed without the consent of the author who contributed it.
