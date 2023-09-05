

# introduction

Alternative to GNSS  (global navigation satellite systems) such as GPS(USA), Galileo(europe), Glonass(Russie), BeiDou(China), QZSS(Japan)

navigation celestre
navigation visuel assisté (adométrie)
navigation magnétique
...
# usage
Try test_2lop_fix.py for 2 lop fix, test_3lop_fix.py for 3 lop fix and so on.
Try test_cartopy for a navigation using waypoint, 3lop fix and course of stear in "rade de lorient"

# navigation visuel assisté
python module for backend (traditional) marine navigation  
one can choose the "fix method"  

> 2 Line of Position(LOP)
> 3 LOP
> running fix

Both distance and angle between LOPs have influence on the certaincy of the position fix.
The optimal angular spread is 90° for two objects and 120° for three objects.

also
> The Willebrord Snellius construction
> Double anglr fix - RFix
> Four point fix - RFix
> Special angle fix - RFix

# nautical_marker
python module to extend the set of markers used in matplotlib.pyplot. The extension are symbols used in nautical charts
