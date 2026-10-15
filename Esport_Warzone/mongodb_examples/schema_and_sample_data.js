use esport_warzone;
db.teams.insertMany([
 {team_name:"Shadow Strikers",game_name:"Free Fire",captain_name:"Aarav",department:"ECE",contact:"aarav@example.com",created_at:new Date()},
 {team_name:"Pixel Ninjas",game_name:"BGMI",captain_name:"Isha",department:"ECE",contact:"isha@example.com",created_at:new Date()}
]);
db.matches.insertMany([
 {match_name:"Battle Royale Round 1",game_name:"Free Fire",arena:"Bermuda",status:"Upcoming"},
 {match_name:"BGMI Round 1",game_name:"BGMI",arena:"Erangel",status:"Upcoming"}
]);
// Insert a result after replacing these placeholder strings with actual ObjectId values:
db.results.insertOne({
 team_id:ObjectId("REPLACE_WITH_TEAM_OBJECT_ID"),team_name:"Shadow Strikers",
 match_id:ObjectId("REPLACE_WITH_MATCH_OBJECT_ID"),match_name:"Battle Royale Round 1",
 game_name:"Free Fire",placement:1,kills:8,points:20,updated_at:new Date()
});
