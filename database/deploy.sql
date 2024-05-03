
--
-- Table structure for table `leagues`
--

DROP TABLE IF EXISTS `leagues`;
CREATE TABLE `leagues` (
  `league_id` bigint unsigned NOT NULL,
  `league_name` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`league_id`),
  UNIQUE KEY `league_id_UNIQUE` (`league_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `matchups`
--

DROP TABLE IF EXISTS `matchups`;
CREATE TABLE `matchups` (
  `matchup_id` bigint unsigned NOT NULL COMMENT 'matchup id from API',
  `league` bigint unsigned DEFAULT NULL,
  `home_team` varchar(50) DEFAULT NULL COMMENT 'name provided for home team from API',
  `away_team` varchar(50) DEFAULT NULL COMMENT 'name provided for away team from API',
  `start_time` datetime DEFAULT NULL COMMENT 'start time of matchup',
  PRIMARY KEY (`matchup_id`),
  UNIQUE KEY `matchup_id_UNIQUE` (`matchup_id`),
  KEY `league_id_idx` (`league`),
  CONSTRAINT `league_id` FOREIGN KEY (`league`) REFERENCES `leagues` (`league_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Holds base information about upcoming matches';

--
-- Table structure for table `odds`
--

DROP TABLE IF EXISTS `odds`;
CREATE TABLE `odds` (
  `matchup_id` bigint unsigned NOT NULL,
  `home` double DEFAULT NULL,
  `draw` double DEFAULT NULL,
  `away` double DEFAULT NULL,
  `time_updated` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `matchup_id_idx` (`matchup_id`),
  CONSTRAINT `matchup_id` FOREIGN KEY (`matchup_id`) REFERENCES `matchups` (`matchup_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;