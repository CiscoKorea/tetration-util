var fs = require('fs')

var csv_file='dns.csv'
var dic = {}
var dic_id = 1
var resp = {'nodes': [], 'edges': []}
fs.readFile( csv_file, (err,data) => {
    if( err) throw err;
    var lines = data.toString().split('\n')
    var src_id, dst_id;
    for( var i =1 ; i < lines.length; i++) {
        items = lines[i].split(',')
        if( !dic.hasOwnProperty( items[0])) {
            dic[items[0]] = dic_id; 
            resp.nodes.push( {id: dic_id, label: items[0]})
            src_id = dic_id++
        } else {
            src_id = dic[items[0]]
        }
        if( !dic.hasOwnProperty( items[1])) {
            dic[items[1]] = dic_id; 
            resp.nodes.push( {id: dic_id, label: items[1]})
            dst_id = dic_id++
        } else {
            dst_id = dic[ items[1]]
        }
        resp.edges.push( {from: src_id, to: dst_id, arrow: 'to'})
    }
    console.log( resp)
});