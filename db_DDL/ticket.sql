CREATE TABLE `ticket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` varchar(150) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ticket_user_idx` (`user_id`),
  CONSTRAINT `user_ticket` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci