
# coding: utf-8

# In[10]:

# Simple read based on the py _sql context
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)


# In[11]:

# Import a bunch of useful libraries for manipulating data and plotting data
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')  # For graph styling
import matplotlib.patches as mpatches


# # Exploring Machine Data
# Load the data and print some stats

# In[12]:

flows = sc._jvm.com.tetration.apps.IO.read(sqlContext._ssql_ctx, "/tetration/flows/", "PARQUET", "LAST24HOURS")
flows.registerTempTable("flows24h")


# In[45]:

fws = sqlContext.sql("""SELECT src_address,dst_address,dst_port,proto,sum(fwd_bytes) as fwd_bytes, sum(rev_bytes) as rev_bytes 
    FROM flows24h 
    WHERE proto in ('UDP','TCP') 
    GROUP BY src_address,dst_address,dst_port,proto 
    ORDER BY fwd_bytes  """)
#print( fws.count())
data = fws.toPandas()


# In[46]:

print( data[['fwd_bytes','rev_bytes']].describe( percentiles=[0.03, 0.05, 0.5, 0.75, 0.95, 0.97]))


# In[47]:

data['fwd_cumsum'] = data['fwd_bytes'].cumsum()
data['fwd_cum_perc'] = data['fwd_cumsum'] / data['fwd_bytes'].sum()
data['rev_cumsum'] = data['rev_bytes'].cumsum()
data['rev_cum_perc'] = data['rev_cumsum'] / data['rev_bytes'].sum()


# In[48]:

print( data[['fwd_bytes', 'fwd_cumsum', 'fwd_cum_perc']])


# In[9]:

get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(16,9))
plt.xlim(-100, 8510646492)
#mybin = [0, 1024, 2048, 4096, 8196, 16392, 32784, 65568, 131136, 262272,524544,1049088,20988176,41976352,83952704, 167905408, 335810816,671621632, 8510646493]
n, bins, patches = plt.hist([data['fwd_bytes'], data['rev_bytes']], bins=50, color=['red','blue'], label=['Fwd Bytes','Rev Bytes'], histtype='bar', log=True)
plt.legend()
print( plt.xlim())
plt.show()


# In[34]:

np.random.seed(19680801)
N_points = 100000
n_bins = 20

# Generate a normal distribution, center at x=0 and y=5
x = np.random.randn(N_points)
y = .4 * x + np.random.randn(100000) + 5

fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# We can set the number of bins with the `bins` kwarg
axs[0].hist(x, bins=n_bins)
axs[1].hist(y, bins=n_bins)


# # Exploring NTP/DNS Data

# In[17]:

# extract NTP/DNS provider and register temp table 
comm = sqlContext.sql("""SELECT dst_address, dst_port, sum(fwd_bytes) as tot_fwd_bytes, sum(rev_bytes) as tot_rev_bytes, count(*) as flow_count
    FROM flows24h 
    WHERE dst_port in ( 123, 53) and proto='UDP' 
    GROUP BY dst_address, dst_port
    ORDER BY flow_count desc """)
comm.registerTempTable("flows24h_comm")


# In[22]:

# it shows how many endpoints really related on DNS or NTP service 
# join two tables DNS case 
dns = sqlContext.sql(""" SELECT a.src_address, a.dst_address, count(*) flow_count 
    FROM flows24h a, flows24h_comm b 
    WHERE a.src_address = b.dst_address and a.dst_port = 53 and b.dst_port = 53 and b.tot_rev_bytes > 0
    GROUP BY a.src_address, a.dst_address 
    ORDER BY flow_count desc """)
dns_data = dns.toPandas();


# In[31]:

print(comm_d.query( 'dst_port == 53'))


# In[ ]:



