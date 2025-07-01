# Counting and Sampling Triangles from a Graph Stream

## Algorithm's Scientific Paper
- https://www.vldb.org/pvldb/vol6/p1870-aduri.pdf

---

## Results
```
┌─────────────────────────────────┬───────────┬──────────────┐
│ dataset                         ┆ triangles ┆ process_took │
│ ---                             ┆ ---       ┆ ---          │
│ str                             ┆ i64       ┆ str          │
╞═════════════════════════════════╪═══════════╪══════════════╡
│ Oregon-1::oregon1_010519.tsv    ┆ 226       ┆ 112.83ms     │
│ Oregon-1::oregon1_010414.tsv    ┆ 318       ┆ 162.30ms     │
│ Oregon-1::oregon1_010512.tsv    ┆ 289       ┆ 168.54ms     │
│ Oregon-1::oregon1_010428.tsv    ┆ 219       ┆ 171.72ms     │
│ Caida::as-caida20060109.tsv     ┆ 1729      ┆ 174.80ms     │
│ Caida::as-caida20070917.tsv     ┆ 1001      ┆ 215.62ms     │
│ Oregon-1::oregon1_010331.tsv    ┆ 285       ┆ 218.81ms     │
│ Caida::as-caida20070326.tsv     ┆ 2525      ┆ 235.81ms     │
│ Oregon-1::oregon1_010407.tsv    ┆ 154       ┆ 253.57ms     │
│ Oregon-1::oregon1_010526.tsv    ┆ 290       ┆ 258.92ms     │
│ Oregon-1::oregon1_010421.tsv    ┆ 344       ┆ 301.05ms     │
│ Caida::as-caida20070910.tsv     ┆ 2334      ┆ 312.43ms     │
│ Caida::as-caida20041004.tsv     ┆ 1790      ┆ 395.89ms     │
│ Caida::as-caida20040802.tsv     ┆ 1555      ┆ 406.18ms     │
│ Caida::as-caida20051107.tsv     ┆ 1569      ┆ 407.42ms     │
│ Caida::as-caida20050606.tsv     ┆ 1818      ┆ 412.41ms     │
│ Caida::as-caida20050502.tsv     ┆ 1655      ┆ 413.58ms     │
│ Caida::as-caida20040503.tsv     ┆ 1688      ┆ 415.24ms     │
│ Caida::as-caida20050801.tsv     ┆ 1655      ┆ 424.31ms     │
│ Caida::as-caida20061016.tsv     ┆ 2150      ┆ 427.59ms     │
│ Caida::as-caida20060403.tsv     ┆ 1994      ┆ 438.99ms     │
│ Caida::as-caida20061023.tsv     ┆ 2205      ┆ 440.96ms     │
│ Caida::as-caida20060508.tsv     ┆ 1851      ┆ 447.41ms     │
│ Caida::as-caida20040607.tsv     ┆ 1760      ┆ 449.46ms     │
│ Caida::as-caida20060710.tsv     ┆ 1917      ┆ 454.62ms     │
│ Caida::as-caida20070521.tsv     ┆ 2508      ┆ 457.06ms     │
│ Caida::as-caida20060417.tsv     ┆ 1932      ┆ 458.21ms     │
│ Caida::as-caida20050905.tsv     ┆ 1731      ┆ 458.23ms     │
│ Caida::as-caida20070723.tsv     ┆ 2558      ┆ 458.82ms     │
│ Caida::as-caida20060717.tsv     ┆ 1744      ┆ 467.20ms     │
│ Oregon-1::oregon1_010505.tsv    ┆ 268       ┆ 467.31ms     │
│ Caida::as-caida20040906.tsv     ┆ 1896      ┆ 467.44ms     │
│ Caida::as-caida20060731.tsv     ┆ 2013      ┆ 477.76ms     │
│ Caida::as-caida20060501.tsv     ┆ 1860      ┆ 480.91ms     │
│ Caida::as-caida20040202.tsv     ┆ 1332      ┆ 489.17ms     │
│ Caida::as-caida20060327.tsv     ┆ 1954      ┆ 489.18ms     │
│ Caida::as-caida20060102.tsv     ┆ 1637      ┆ 499.23ms     │
│ Caida::as-caida20060313.tsv     ┆ 1830      ┆ 500.24ms     │
│ Caida::as-caida20051003.tsv     ┆ 1507      ┆ 500.93ms     │
│ Caida::as-caida20061106.tsv     ┆ 1684      ┆ 501.90ms     │
│ Caida::as-caida20060220.tsv     ┆ 1755      ┆ 503.68ms     │
│ Caida::as-caida20050307.tsv     ┆ 1689      ┆ 506.89ms     │
│ Caida::as-caida20040705.tsv     ┆ 1666      ┆ 507.60ms     │
│ Caida::as-caida20041101.tsv     ┆ 1642      ┆ 509.25ms     │
│ Caida::as-caida20061002.tsv     ┆ 1974      ┆ 509.74ms     │
│ Caida::as-caida20050103.tsv     ┆ 1718      ┆ 512.75ms     │
│ Caida::as-caida20060821.tsv     ┆ 1870      ┆ 512.78ms     │
│ Caida::as-caida20060724.tsv     ┆ 1965      ┆ 514.60ms     │
│ Caida::as-caida20060213.tsv     ┆ 1766      ┆ 517.43ms     │
│ Caida::as-caida20051205.tsv     ┆ 1516      ┆ 521.60ms     │
│ Caida::as-caida20050404.tsv     ┆ 1663      ┆ 526.05ms     │
│ Caida::as-caida20040301.tsv     ┆ 1338      ┆ 526.11ms     │
│ Caida::as-caida20061120.tsv     ┆ 1989      ┆ 533.24ms     │
│ Caida::as-caida20060320.tsv     ┆ 1921      ┆ 540.35ms     │
│ Caida::as-caida20070604.tsv     ┆ 2456      ┆ 548.73ms     │
│ Caida::as-caida20070409.tsv     ┆ 2367      ┆ 549.04ms     │
│ Caida::as-caida20041206.tsv     ┆ 1710      ┆ 558.75ms     │
│ Caida::as-caida20060612.tsv     ┆ 1981      ┆ 560.17ms     │
│ Caida::as-caida20050704.tsv     ┆ 1806      ┆ 563.03ms     │
│ Caida::as-caida20040405.tsv     ┆ 1647      ┆ 565.05ms     │
│ Caida::as-caida20060807.tsv     ┆ 1986      ┆ 568.38ms     │
│ Caida::as-caida20060814.tsv     ┆ 2101      ┆ 572.70ms     │
│ Caida::as-caida20070611.tsv     ┆ 2118      ┆ 582.07ms     │
│ Caida::as-caida20060605.tsv     ┆ 1812      ┆ 585.90ms     │
│ Caida::as-caida20071105.tsv     ┆ 2150      ┆ 602.02ms     │
│ Caida::as-caida20060925.tsv     ┆ 2311      ┆ 603.60ms     │
│ Caida::as-caida20060522.tsv     ┆ 2058      ┆ 608.69ms     │
│ Caida::as-caida20050207.tsv     ┆ 1725      ┆ 610.48ms     │
│ Caida::as-caida20070319.tsv     ┆ 2373      ┆ 613.90ms     │
│ Caida::as-caida20071022.tsv     ┆ 2173      ┆ 614.36ms     │
│ Caida::as-caida20070219.tsv     ┆ 2128      ┆ 619.10ms     │
│ Caida::as-caida20060424.tsv     ┆ 1926      ┆ 619.55ms     │
│ Caida::as-caida20060206.tsv     ┆ 1838      ┆ 638.98ms     │
│ Caida::as-caida20060626.tsv     ┆ 1772      ┆ 645.77ms     │
│ Caida::as-caida20061009.tsv     ┆ 2412      ┆ 649.84ms     │
│ Caida::as-caida20061211.tsv     ┆ 2543      ┆ 652.31ms     │
│ Caida::as-caida20070625.tsv     ┆ 2581      ┆ 660.52ms     │
│ Caida::as-caida20061113.tsv     ┆ 461       ┆ 661.84ms     │
│ Caida::as-caida20060410.tsv     ┆ 1760      ┆ 662.34ms     │
│ Caida::as-caida20070813.tsv     ┆ 2263      ┆ 663.24ms     │
│ Caida::as-caida20070514.tsv     ┆ 2457      ┆ 663.61ms     │
│ Caida::as-caida20060306.tsv     ┆ 1955      ┆ 674.81ms     │
│ Caida::as-caida20060619.tsv     ┆ 1932      ┆ 676.33ms     │
│ Caida::as-caida20070312.tsv     ┆ 2166      ┆ 687.45ms     │
│ Caida::as-caida20061127.tsv     ┆ 2254      ┆ 690.81ms     │
│ Caida::as-caida20070205.tsv     ┆ 2249      ┆ 696.87ms     │
│ Caida::as-caida20070430.tsv     ┆ 2397      ┆ 698.23ms     │
│ Caida::as-caida20070212.tsv     ┆ 2413      ┆ 700.18ms     │
│ Caida::as-caida20070402.tsv     ┆ 2345      ┆ 702.49ms     │
│ Caida::as-caida20060227.tsv     ┆ 2121      ┆ 705.20ms     │
│ Caida::as-caida20060130.tsv     ┆ 1999      ┆ 708.63ms     │
│ Caida::as-caida20060703.tsv     ┆ 1730      ┆ 716.64ms     │
│ Caida::as-caida20070226.tsv     ┆ 2218      ┆ 717.81ms     │
│ Caida::as-caida20061030.tsv     ┆ 1984      ┆ 718.08ms     │
│ Caida::as-caida20060918.tsv     ┆ 2063      ┆ 721.29ms     │
│ Caida::as-caida20061204.tsv     ┆ 2029      ┆ 725.04ms     │
│ Caida::as-caida20060116.tsv     ┆ 1707      ┆ 727.01ms     │
│ Caida::as-caida20060515.tsv     ┆ 1831      ┆ 733.86ms     │
│ Caida::as-caida20060911.tsv     ┆ 2311      ┆ 736.03ms     │
│ Caida::as-caida20070122.tsv     ┆ 2592      ┆ 737.66ms     │
│ Caida::as-caida20070730.tsv     ┆ 2536      ┆ 738.74ms     │
│ Caida::as-caida20071008.tsv     ┆ 2320      ┆ 746.87ms     │
│ Caida::as-caida20070101.tsv     ┆ 2258      ┆ 748.60ms     │
│ Caida::as-caida20060828.tsv     ┆ 2349      ┆ 763.64ms     │
│ Caida::as-caida20070716.tsv     ┆ 2368      ┆ 764.12ms     │
│ Caida::as-caida20070305.tsv     ┆ 2283      ┆ 764.57ms     │
│ Caida::as-caida20060123.tsv     ┆ 1712      ┆ 779.57ms     │
│ Caida::as-caida20070903.tsv     ┆ 2091      ┆ 786.07ms     │
│ Caida::as-caida20061225.tsv     ┆ 2424      ┆ 788.48ms     │
│ Caida::as-caida20071001.tsv     ┆ 2135      ┆ 789.02ms     │
│ Caida::as-caida20070820.tsv     ┆ 2269      ┆ 789.45ms     │
│ Caida::as-caida20070702.tsv     ┆ 2572      ┆ 792.04ms     │
│ Caida::as-caida20070709.tsv     ┆ 2639      ┆ 795.46ms     │
│ Caida::as-caida20060904.tsv     ┆ 2292      ┆ 809.36ms     │
│ Caida::as-caida20061218.tsv     ┆ 2221      ┆ 827.46ms     │
│ Caida::as-caida20070416.tsv     ┆ 2426      ┆ 832.80ms     │
│ Caida::as-caida20070827.tsv     ┆ 2241      ┆ 842.71ms     │
│ Caida::as-caida20070507.tsv     ┆ 2003      ┆ 852.81ms     │
│ Caida::as-caida20070618.tsv     ┆ 2266      ┆ 863.17ms     │
│ Caida::as-caida20070423.tsv     ┆ 1966      ┆ 876.78ms     │
│ Caida::as-caida20071015.tsv     ┆ 2368      ┆ 895.62ms     │
│ Caida::as-caida20070108.tsv     ┆ 2624      ┆ 898.82ms     │
│ Caida::as-caida20070528.tsv     ┆ 2441      ┆ 901.50ms     │
│ Caida::as-caida20060529.tsv     ┆ 1926      ┆ 901.72ms     │
│ Caida::as-caida20071112.tsv     ┆ 2026      ┆ 919.40ms     │
│ Caida::as-caida20070924.tsv     ┆ 2580      ┆ 923.10ms     │
│ Caida::as-caida20070806.tsv     ┆ 2525      ┆ 993.55ms     │
│ Caida::as-caida20070115.tsv     ┆ 2713      ┆ 1.00s        │
│ Caida::as-caida20071029.tsv     ┆ 2302      ┆ 1.02s        │
│ Caida::as-caida20070129.tsv     ┆ 2361      ┆ 1.08s        │
│ Caida::as-caida20040105.tsv     ┆ 1111      ┆ 1.14s        │
│ Reddit::soc-redditHyperlinks-b… ┆ 213421    ┆ 1.59s        │
│ Reddit::soc-redditHyperlinks-t… ┆ 1105794   ┆ 8.27s        │
└─────────────────────────────────┴───────────┴──────────────┘ 
```
---

### How to use
```
pip install uv
uv run main.py

# you can use this command additional for help
uv run main.py --help
```

