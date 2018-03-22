/** Always import Tetration App Lib **/
import com.tetration.apps.IO
import com.tetration.apps.DataTaps
import collection.JavaConverters._
import java.util.Calendar
//import sqlContext.implicits._
/**
retrieve all source ip address from application policy with given destination address  
  - useful for scope expansion with small number of target addresses. 
**/
val sdf = IO.read(sqlContext, "/tetration/flows/", "PARQUET", "LAST24HOURS")
// IO.read( sqlContext, "/tetration/flows/", "PARQUET", "YYYYMMDDHH*", true) 
sdf.registerTempTable("flows24h")
// update here with given destination ip address 
var dest_addrs = "'10.66.237.211', '64.104.123.245', '10.66.239.40'"
val clients = sqlContext.sql(s"select dst_address, src_address, count(*) as src_count from flows24h where dst_address in ($dest_addrs) group by dst_address, src_address order by dst_address, src_count desc")

// just show 100 rows 
clients.show(100) 