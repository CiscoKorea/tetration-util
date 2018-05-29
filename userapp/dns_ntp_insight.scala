/** Always import Tetration App Lib **/
import com.tetration.apps.IO
import com.tetration.apps.DataTaps
import collection.JavaConverters._
import java.util.Calendar


/** Read 1day data **/
val sdf = IO.read(sqlContext, "/tetration/flows/", "PARQUET", "LAST24HOURS") 
sdf.registerTempTable("flows24h")

/** extract NTP/DNS provider and register temp table **/
var commdf = sqlContext.sql("""select dst_address, dst_port, count(*) flow_count from flows24h where dst_port in ( 123, 53) group by dst_address, dst_port order by flow_count desc """)
commdf.registerTempTable("flows24h_comm")
commdf.show(30,false)

/** it shows how many endpoints really related on DNS or NTP service **/
/** join two tables DNS case **/
sqlContext.sql("""select a.src_address, a.dst_address, count(*) flow_count from flows24h a, flows24h_comm b 
where a.src_address = b.dst_address and a.dst_port = 53 and b.dst_port = 53 group by a.src_address, a.dst_address order by flow_count desc""").show(30, false)

/** join two tables NTP case **/
sqlContext.sql("""select a.src_address, a.dst_address, count(*) flow_count from flows24h a, flows24h_comm b 
where a.src_address = b.dst_address and a.dst_port = 123 and b.dst_port = 123 group by a.src_address, a.dst_address order by flow_count desc""").show(30, false)
