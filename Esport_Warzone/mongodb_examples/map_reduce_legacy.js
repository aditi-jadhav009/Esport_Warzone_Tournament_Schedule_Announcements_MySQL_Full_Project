// Syllabus demonstration only: mapReduce is deprecated starting MongoDB 5.0.
// Run the legacy call only if your installed MongoDB version supports it.
use esport_warzone;
var mapFunction = function(){ emit(this.game_name,{points:this.points||0,kills:this.kills||0,count:1}); };
var reduceFunction = function(game,values){
  var total={points:0,kills:0,count:0};
  values.forEach(function(v){total.points+=v.points;total.kills+=v.kills;total.count+=v.count;});
  return total;
};
// Legacy syntax when supported:
// db.results.mapReduce(mapFunction,reduceFunction,{out:"game_totals_map_reduce"});

// Modern recommended aggregation equivalent:
db.results.aggregate([
 {$group:{_id:"$game_name",totalResults:{$sum:1},totalPoints:{$sum:"$points"},totalKills:{$sum:"$kills"}}},
 {$sort:{totalPoints:-1}},
 {$out:"game_totals_aggregation"}
]);
