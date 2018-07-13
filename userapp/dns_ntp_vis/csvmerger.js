var fs = require('fs')

var args = process.argv.slice(2)
var path = args[0]
var csv_file = args[1]
fs.readdir( path, (err, files) => {
    if( err) throw Error;
    fs.writeFileSync( csv_file, "src_address,dst_address,flow_count\n")
    files.forEach( buf => {
        file = buf.toString()
        if( file.indexOf("part-") == 0) {
            fs.readFile( path + '\\' + file, (err, buf) => {
                lines = buf.toString().split('\n')
                for( var i =1; i < lines.length && lines[i].length > 2; i++)
                    fs.appendFileSync( csv_file, lines[i]+'\n')
            });
        }
    });
});


