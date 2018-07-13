var fs = require('fs')

var args = process.argv.slice(2)

var json_file = args[0]
var out_csv_file = args[1]

var head;
fs.readFile( json_file, (err, buf) => {
	if( err) throw Error;
	items = JSON.parse(buf.toString())
	head = Object.keys( items[0])
	//console.log(head)
	//console.log( Object.values(items[0]))
	fs.writeFileSync( out_csv_file, head.join(',') + '\n')
	items.forEach( item => {
		fs.appendFileSync( out_csv_file, Object.values(item).join(',')+'\n')
	});
});
