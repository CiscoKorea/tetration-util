# Simple read based on the py _sql context
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)


flow_data = sc._jvm.com.tetration.apps.IO.read(sqlContext._ssql_ctx, "/tetration/flows/", "PARQUET", "LASTHOUR")
flow_data.registerTempTable("flowtab")

# show the unique src_address and dst_address pairs
df = sqlContext.sql("select src_address, dst_address from flowtab where dst_address like '10.66.239.%' group by src_address, dst_address order by dst_address")
df.show(1000)

# show the unique dst_addresses
df = sqlContext.sql("select dst_address from flowtab where dst_address like '10.66.239.%' group by dst_address order by dst_address")
df.show(1000)

# show the sum of fwd_bytes of each dst_address
dstIPs = df.rdd.map(lambda p: "" + p.dst_address).collect()
for dstip in dstIPs:
    sql = "select src_address, dst_address, sum(fwd_bytes) from flowtab where dst_address like \'" + dstip + "\' group by src_address, dst_address"
    print(sql)
    sqlContext.sql(sql).show()

