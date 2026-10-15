-- ESPORT WARZONE | MySQL Workbench schema
-- In MySQL Workbench: open this file, connect to MySQL Server, click the lightning bolt.
CREATE DATABASE IF NOT EXISTS esport_warzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE esport_warzone;

CREATE TABLE IF NOT EXISTS teams (
  id INT AUTO_INCREMENT PRIMARY KEY,
  team_name VARCHAR(100) NOT NULL UNIQUE,
  game_name VARCHAR(80) NOT NULL,
  captain_name VARCHAR(100) NOT NULL,
  contact VARCHAR(40) NOT NULL,
  department VARCHAR(80) NOT NULL DEFAULT 'ECE',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_teams_game_created (game_name, created_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS players (
  id INT AUTO_INCREMENT PRIMARY KEY,
  team_id INT NOT NULL,
  player_name VARCHAR(100) NOT NULL,
  game_uid VARCHAR(100) NOT NULL UNIQUE,
  role VARCHAR(60) NOT NULL DEFAULT 'Player',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_players_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
  INDEX idx_players_team (team_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS matches (
  id INT AUTO_INCREMENT PRIMARY KEY,
  match_name VARCHAR(120) NOT NULL,
  game_name VARCHAR(80) NOT NULL,
  arena VARCHAR(100) NOT NULL,
  start_at DATETIME NULL,
  end_at DATETIME NULL,
  status ENUM('Upcoming','Live','Completed') NOT NULL DEFAULT 'Upcoming',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_matches_game_status (game_name, status),
  INDEX idx_matches_start_at (start_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS player_accounts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  game_name VARCHAR(80) NOT NULL,
  gamer_tag VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_player_accounts_game (game_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS results (
  id INT AUTO_INCREMENT PRIMARY KEY,
  match_id INT NOT NULL,
  team_id INT NOT NULL,
  placement INT NOT NULL DEFAULT 0,
  kills INT NOT NULL DEFAULT 0,
  points INT NOT NULL DEFAULT 0,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_results_match FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
  CONSTRAINT fk_results_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
  UNIQUE KEY uq_result_match_team (match_id, team_id),
  INDEX idx_results_points (points)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS announcements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  body TEXT NOT NULL,
  category ENUM('General','Registration','Schedule','Results','Rules') NOT NULL DEFAULT 'General',
  published TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_announcements_published (published, created_at)
) ENGINE=InnoDB;

-- Starter timetable (insert only if no matches exist, so rerunning does not duplicate demo matches).
INSERT INTO matches (match_name, game_name, arena, start_at, end_at, status)
SELECT demo.match_name, demo.game_name, demo.arena, demo.start_at, demo.end_at, 'Upcoming'
FROM (
  SELECT 'Free Fire Qualifier' match_name, 'Free Fire' game_name, 'Bermuda' arena, '2026-11-02 10:00:00' start_at, '2026-11-02 11:00:00' end_at UNION ALL
  SELECT 'BGMI Squad Qualifier','BGMI','Erangel','2026-11-02 11:30:00','2026-11-02 12:30:00' UNION ALL
  SELECT 'Candy Crush Challenge','Candy Crush Saga','Classic Levels','2026-11-02 13:00:00','2026-11-02 13:30:00' UNION ALL
  SELECT 'Subway Surfers Sprint','Subway Surfers','World Tour','2026-11-02 13:45:00','2026-11-02 14:15:00' UNION ALL
  SELECT 'Temple Run Dash','Temple Run','Jungle Ruins','2026-11-02 14:30:00','2026-11-02 15:00:00' UNION ALL
  SELECT 'Mobile Legends Showdown','Mobile Legends: Bang Bang','Land of Dawn','2026-11-03 10:00:00','2026-11-03 11:00:00' UNION ALL
  SELECT 'Dr. Driving Time Trial','Dr. Driving','City Circuit','2026-11-03 11:30:00','2026-11-03 12:00:00' UNION ALL
  SELECT 'Angry Birds Aim-Off','Angry Birds','Piggy Island','2026-11-03 13:00:00','2026-11-03 13:30:00' UNION ALL
  SELECT 'Bubble Shooter Finals','Bubble Shooter','Arcade Arena','2026-11-03 14:00:00','2026-11-03 14:30:00'
) AS demo
WHERE NOT EXISTS (SELECT 1 FROM matches);

INSERT INTO announcements (title, body, category, published)
SELECT 'Welcome to Esport Warzone', 'Player registration is open. Check the match timetable regularly for schedule updates. Contact the tournament administrator if you need help.', 'Registration', 1
WHERE NOT EXISTS (SELECT 1 FROM announcements);

-- Useful Workbench queries for the DBMS practical:
-- SELECT * FROM matches ORDER BY start_at;
-- SELECT * FROM announcements WHERE published = 1 ORDER BY created_at DESC;
-- SELECT t.team_name, SUM(r.points) AS total_points, SUM(r.kills) AS total_kills
-- FROM results r JOIN teams t ON t.id = r.team_id
-- GROUP BY t.id, t.team_name ORDER BY total_points DESC, total_kills DESC;
