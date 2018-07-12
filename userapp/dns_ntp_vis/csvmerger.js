var fs = require('fs')

var args = process.argv.slice(2)
var path = args[0]
fs.readdir( path, (err, files) => {
    if( err) throw Error;
    fs.writeFileSync( 'merged.cvs', "src_address,dst_address,dst_port,proto,tot_fwd_bytes,tot_rev_bytes\n")
    files.forEach( buf => {
        file = buf.toString()
        if( file.indexOf("part-") == 0) {
            fs.readFile( path + '/' + file, (err, buf) => {
                lines = buf.toString().split('\n')
                for( var i =1; i < lines.length; i++)
                    fs.appendFileSync( 'merged.cvs', lines[i]+'\n')
            });
        }
    });
});

