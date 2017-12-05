# tetration-util
Utility code for Tetration 


# generating normalized json formatted SLB configuration 
please check slb_sample.csv format 
```
#> python slbconv.py -i "input csv file" -o "output json file" 
```

# upload korean user annotation to tetration cluster 
please see test.csv and make sure file as UTF-8 encoding. 
create all_api.json from API Key creation menu,including user annotation capability
Update scope name in your case. 
```
#> python userannotation.py 
```
