-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: nursingdb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `scheduled_member`
--

DROP TABLE IF EXISTS `scheduled_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scheduled_member` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schedule_id` varchar(50) DEFAULT NULL,
  `staff_id` int DEFAULT NULL,
  `schedule_date` int DEFAULT NULL,
  `leave_dates` text,
  `ward` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_staff_id` (`staff_id`),
  CONSTRAINT `fk_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=412 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduled_member`
--

LOCK TABLES `scheduled_member` WRITE;
/*!40000 ALTER TABLE `scheduled_member` DISABLE KEYS */;
INSERT INTO `scheduled_member` VALUES (276,'2026-3',5,31,NULL,'N17'),(277,'2026-3',6,31,NULL,'N17'),(278,'2026-3',7,31,NULL,'N17'),(279,'2026-3',8,31,NULL,'N17'),(280,'2026-3',9,31,NULL,'N17'),(281,'2026-3',10,31,NULL,'N17'),(282,'2026-3',11,31,NULL,'N17'),(283,'2026-3',12,31,NULL,'N17'),(284,'2026-3',13,31,NULL,'N17'),(285,'2026-3',14,31,NULL,'N17'),(286,'2026-3',15,31,NULL,'N17'),(287,'2026-3',16,31,NULL,'N17'),(288,'2026-3',18,31,NULL,'N17'),(289,'2026-3',19,31,NULL,'N17'),(290,'2026-3',20,31,NULL,'N17'),(291,'2026-3',23,31,NULL,'N17'),(292,'2026-3',24,31,NULL,'N17'),(293,'2026-3',25,31,NULL,'N17'),(294,'2026-3',26,31,NULL,'N17'),(295,'2026-3',27,31,NULL,'N17'),(296,'2026-3',28,31,NULL,'N17'),(297,'2026-3',29,31,NULL,'N17'),(298,'2026-3',30,31,NULL,'N17'),(368,'2026-4',5,30,NULL,'N17'),(369,'2026-4',6,30,NULL,'N17'),(370,'2026-4',7,30,NULL,'N17'),(371,'2026-4',8,30,NULL,'N17'),(372,'2026-4',9,30,NULL,'N17'),(373,'2026-4',10,30,NULL,'N17'),(374,'2026-4',11,30,NULL,'N17'),(375,'2026-4',12,30,NULL,'N17'),(376,'2026-4',13,30,NULL,'N17'),(377,'2026-4',14,30,NULL,'N17'),(378,'2026-4',15,30,NULL,'N17'),(379,'2026-4',16,30,NULL,'N17'),(380,'2026-4',18,30,NULL,'N17'),(381,'2026-4',19,30,NULL,'N17'),(382,'2026-4',20,30,NULL,'N17'),(383,'2026-4',23,30,NULL,'N17'),(384,'2026-4',24,30,NULL,'N17'),(385,'2026-4',25,30,NULL,'N17'),(386,'2026-4',26,30,NULL,'N17'),(387,'2026-4',27,30,NULL,'N17'),(388,'2026-4',28,30,NULL,'N17'),(389,'2026-4',29,30,NULL,'N17'),(390,'2026-4',30,30,NULL,'N17'),(391,'2026-5',5,31,NULL,'N17'),(392,'2026-5',6,31,NULL,'N17'),(393,'2026-5',7,31,NULL,'N17'),(394,'2026-5',9,31,NULL,'N17'),(395,'2026-5',10,31,NULL,'N17'),(396,'2026-5',11,31,NULL,'N17'),(397,'2026-5',13,31,NULL,'N17'),(398,'2026-5',14,31,NULL,'N17'),(399,'2026-5',15,31,NULL,'N17'),(400,'2026-5',16,31,NULL,'N17'),(401,'2026-5',18,31,NULL,'N17'),(402,'2026-5',19,31,NULL,'N17'),(403,'2026-5',20,31,NULL,'N17'),(404,'2026-5',23,31,NULL,'N17'),(405,'2026-5',24,31,NULL,'N17'),(406,'2026-5',25,31,NULL,'N17'),(407,'2026-5',26,31,NULL,'N17'),(408,'2026-5',27,31,NULL,'N17'),(409,'2026-5',28,31,NULL,'N17'),(410,'2026-5',29,31,NULL,'N17'),(411,'2026-5',30,31,NULL,'N17');
/*!40000 ALTER TABLE `scheduled_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settingtime`
--

DROP TABLE IF EXISTS `settingtime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settingtime` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ward` varchar(50) NOT NULL,
  `min_shift_interval` decimal(4,1) DEFAULT NULL,
  `min_rest_2w` decimal(4,1) DEFAULT NULL,
  `min_rest_1m` decimal(5,1) DEFAULT NULL,
  `max_hours_1w` decimal(4,1) DEFAULT NULL,
  `max_hours_1d` decimal(4,1) DEFAULT NULL,
  `max_continuous_work` decimal(4,1) DEFAULT NULL,
  `max_shifts_1w` decimal(4,1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settingtime`
--

LOCK TABLES `settingtime` WRITE;
/*!40000 ALTER TABLE `settingtime` DISABLE KEYS */;
INSERT INTO `settingtime` VALUES (1,'N17',1.0,1.0,1.0,1.0,1.0,1.0,1.0);
/*!40000 ALTER TABLE `settingtime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(50) NOT NULL,
  `employee_num` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('IT_Admin','Head_Nurse','Staff_Nurse') NOT NULL,
  `level` enum('N0','N1','N2','N3','N4') DEFAULT NULL,
  `ward` varchar(20) DEFAULT NULL,
  `join_date` date DEFAULT NULL,
  `is_temp_password` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_num` (`employee_num`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'系統管理員','ADM0001','ADM0001','IT_Admin',NULL,NULL,'2026-02-20',1),(3,'護理長N17','HNUR0001','HNUR0001','Head_Nurse',NULL,'N17','2026-02-22',1),(5,'謝O靜','NUR0002','NUR0002','Staff_Nurse','N4','N17','2011-10-18',1),(6,'林O雯','NUR0003','NUR0003','Staff_Nurse','N3','N17','2017-09-04',1),(7,'李O政','NUR0004','NUR0004','Staff_Nurse','N2','N17','2018-04-09',1),(8,'李O庭','NUR0005','NUR0005','Staff_Nurse','N2','N17','2018-07-02',1),(9,'朱O茜','NUR0006','NUR0006','Staff_Nurse','N2','N17','2019-08-10',1),(10,'賴O珍','NUR0007','NUR0007','Staff_Nurse','N2','N17','2020-09-07',1),(11,'林O均','NUR0008','NUR0008','Staff_Nurse','N2','N17','2020-09-07',1),(12,'楊O閔','NUR0009','NUR0009','Staff_Nurse','N2','N17','2021-10-04',1),(13,'譚O慈','NUR0010','NUR0010','Staff_Nurse','N2','N17','2021-10-04',1),(14,'張O研','NUR0011','NUR0011','Staff_Nurse','N2','N17','2022-02-14',1),(15,'吳O儀','NUR0012','NUR0012','Staff_Nurse','N2','N17','2022-07-04',1),(16,'謝O伃','NUR0013','NUR0013','Staff_Nurse','N2','N17','2022-08-08',1),(18,'陳O宸','NUR0014','NUR0014','Staff_Nurse','N2','N17','2022-09-05',1),(19,'江O芸','NUR0015','NUR0015','Staff_Nurse','N2','N17','2022-12-05',1),(20,'張O文','NUR0016','NUR0016','Staff_Nurse','N0','N17','2025-08-04',1),(23,'張O翔','NUR0017','NUR0017','Staff_Nurse','N0','N17','2025-09-01',1),(24,'朱O碩','NUR0018','NUR0018','Staff_Nurse','N0','N17','2026-03-02',1),(25,'王O金','NUR0019','NUR0019','Staff_Nurse','N3','N17','1999-08-02',1),(26,'駱O君','NUR0020','NUR0020','Staff_Nurse','N2','N17','2010-06-21',1),(27,'謝O欣','NUR0021','NUR0021','Staff_Nurse','N2','N17','2013-10-14',1),(28,'廖O婷','NUR0022','NUR0022','Staff_Nurse','N1','N17','2024-04-22',1),(29,'楊O萱','NUR0023','NUR0023','Staff_Nurse','N1','N17','2019-04-08',1),(30,'謝O洵','NUR0024','NUR0024','Staff_Nurse','N2','N17','2021-08-09',1);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_number_schedule`
--

DROP TABLE IF EXISTS `staff_number_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff_number_schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shift` varchar(30) NOT NULL,
  `shift_staff_number` int NOT NULL,
  `staff_id` text,
  `ward` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_number_schedule`
--

LOCK TABLES `staff_number_schedule` WRITE;
/*!40000 ALTER TABLE `staff_number_schedule` DISABLE KEYS */;
INSERT INTO `staff_number_schedule` VALUES (10,'day',6,'','N17'),(11,'night',4,'賴O珍','N17'),(12,'midnight',3,'江O芸','N17');
/*!40000 ALTER TABLE `staff_number_schedule` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-08  0:22:25
