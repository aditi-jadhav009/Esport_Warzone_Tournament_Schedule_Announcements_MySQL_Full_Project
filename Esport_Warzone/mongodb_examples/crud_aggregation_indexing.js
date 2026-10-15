// Esport Warzone — MongoDB CRUD, logical operators, aggregation and indexes
use esport_warzone;

// CREATE
db.teams.insertOne({team_name:"Shadow Strikers",game_name:"Free Fire",captain_name:"Demo Captain",department:"ECE",contact:"demo@example.com",created_at:new Date()});

// READ + logical operators
db.teams.find({$or:[{game_name:"Free Fire"},{game_name:"BGMI"}]});
db.teams.find({$and:[{department:"ECE"},{game_name:{$ne:"Candy Crush Saga"}}]});
db.teams.find({game_name:{$in:["BGMI","Free Fire"]}});

// UPDATE
db.teams.updateOne({team_name:"Shadow Strikers"},{$set:{game_name:"BGMI",captain_name:"Updated Captain"}});

// Save-style upsert. Old db.collection.save() is deprecated/removed in modern shells.
db.teams.replaceOne({team_name:"Shadow Strikers"},{team_name:"Shadow Strikers",game_name:"Free Fire",captain_name:"Demo Captain"},{upsert:true});

// DELETE
db.teams.deleteOne({team_name:"Shadow Strikers"});

// AGGREGATION
db.results.aggregate([{$group:{_id:"$game_name",totalPoints:{$sum:"$points"},totalKills:{$sum:"$kills"},resultCount:{$sum:1}}},{$sort:{totalPoints:-1}}]);

// INDEXING
db.teams.createIndex({game_name:1,team_name:1});
db.players.createIndex({game_uid:1},{unique:true});
db.results.createIndex({game_name:1,points:-1});
db.teams.getIndexes();
db.teams.find({game_name:"BGMI"}).explain("executionStats");
