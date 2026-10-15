document.addEventListener("DOMContentLoaded", () => {
 const add = document.getElementById("add-player");
 const players = document.getElementById("players");
 if (add && players) add.addEventListener("click", () => {
   const count = players.querySelectorAll(".player-row").length;
   if (count >= 6) { alert("Maximum 6 players per team in this demo."); return; }
   const row = document.createElement("div");
   row.className = "player-row";
   row.innerHTML = `<span class="player-number">${String(count+1).padStart(2,"0")}</span><input name="player_name[]" aria-label="Player name" placeholder="Player name"><input name="game_uid[]" aria-label="Player ID" placeholder="Game UID / player ID"><select name="role[]" aria-label="Player role"><option>Player</option><option>Captain</option><option>Support</option><option>Attacker</option><option>Defender</option></select>`;
   players.appendChild(row);
 });
});
