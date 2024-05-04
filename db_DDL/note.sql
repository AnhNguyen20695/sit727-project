CREATE TABLE `note` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` varchar(150) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `note_user_idx` (`user_id`),
  CONSTRAINT `user_note` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci