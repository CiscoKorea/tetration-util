# tetration-util
Utility code for Tetration 


# generating normalized json formatted SLB configuration 
please check slb_sample.csv format 
```
#> python slbconv.py -i "input csv file" -o "output json file" 
```

# upload korean user annotation to tetration cluster 
please prepare your inventory file and make it sure inventory file as UTF-8 encoding. 
update all_key.json from API Key creation menu ( Gear > Maintenace > API KEYS), including user_data_upload capability
```
#> python userannotation.py -h "https://tetration-cluster-ip-address" -i "utf8_inventory_file" -s "scope_name_for_userannotation"  
```
