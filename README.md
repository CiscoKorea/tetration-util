# tetration-util
Utility code for Tetration 


# generating normalized json formatted SLB configuration 
please check slb_sample.csv format 
```
#> python slbconv.py -i "input csv file" -o "output json file" 
```

# upload korean user annotation to tetration cluster 
please prepare your inventory file and make it sure inventory file as UTF-8 encoding. 
update all_key.json from API Key creation menu (Gear > Maintenance > API KEYS), including user_data_upload capability
```
#> python userannotation.py -h "https://tetration-cluster-ip-address" -i "utf8_inventory_file" -s "scope_name_for_userannotation"  
```

# generate application cluster information for customer's review 
For customer's review for application cluster, just generate CSV format file with cluster name and endpoint ip & hostname. 
This can help your customer to review and give a right cluster name for Tetration application dependency mapping. 
Please see the sample mapping file which named {app-name}_server_list.csv.
```
#> python app_detail.py -h "https://tetration-cluster-ip-address"
```
After above command, app_detail.py will generate {appName}-App-{version}.csv files for related API KEY capability. 
Just fill out new cluster name with guided ip address and hostname with production environment ( prod or dev)
