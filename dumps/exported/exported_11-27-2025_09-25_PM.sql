-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: etrace_revamped
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adminaccount`
--

DROP TABLE IF EXISTS `adminaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) NOT NULL,
  `role` enum('sysad','peso','dean','alumni') NOT NULL,
  `email` varchar(256) NOT NULL,
  `pass_hash` varchar(256) NOT NULL,
  `avatar_filename` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `school_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `school_id` (`school_id`),
  CONSTRAINT `adminaccount_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `sysadschool` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminaccount`
--

LOCK TABLES `adminaccount` WRITE;
/*!40000 ALTER TABLE `adminaccount` DISABLE KEYS */;
INSERT INTO `adminaccount` VALUES (1,'System',NULL,'Administrator','sysad','kdadvincul2004@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$RYgxJiTk3LvX+t+7V+o9Jw$dI1E3D2Gie6xzSn6wLeJCz1va/T150ibPENsdm/3yj0',NULL,'2025-11-26 02:38:25','2025-11-26 02:38:25',1,NULL),(2,'Kyle','','Advincula','peso','daryladvincula2004@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$MSbkvDdmjNF6D+E8p9Ra6w$JcyInYl2OxyRsaX/cOh51uqfkP7zUZ6wj/TPF/3beFc',NULL,'2025-11-26 03:19:30','2025-11-26 03:19:30',1,NULL),(3,'System',NULL,'Administrator','sysad','zaymonnekent17@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$ilEqJcR4bw3BeC9F6H0PYQ$F/iGQVqhDkmHfOvB9bW4EBY8pd5rhf+cNyrQZH0bX8U',NULL,'2025-11-27 10:38:38','2025-11-27 10:38:38',1,NULL);
/*!40000 ALTER TABLE `adminaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminauditlog`
--

DROP TABLE IF EXISTS `adminauditlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminauditlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `action` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `adminauditlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `adminaccount` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminauditlog`
--

LOCK TABLES `adminauditlog` WRITE;
/*!40000 ALTER TABLE `adminauditlog` DISABLE KEYS */;
INSERT INTO `adminauditlog` VALUES (1,'2025-11-26 03:19:30','Assigned daryladvincula2004@gmail.com as a new PESO.',1),(2,'2025-11-26 03:25:31','Verified a company \"GoCrayons\".',2),(3,'2025-11-26 03:26:13','Verified a company \"GoCrayons\".',2),(4,'2025-11-26 16:25:37','Posted a new job \"Game Developer\".',1),(5,'2025-11-26 16:40:34','archived a company \"GoCrayons\".',1),(6,'2025-11-26 16:40:48','restored a company \"GoCrayons\".',1),(7,'2025-11-26 16:47:56','archived a job post \"Game Developer\".',1),(8,'2025-11-26 16:48:08','restored a job post \"Game Developer\".',1),(9,'2025-11-26 17:39:39','Updated a company document \"GoCrayons\".',1);
/*!40000 ALTER TABLE `adminauditlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminpasswordchange`
--

DROP TABLE IF EXISTS `adminpasswordchange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminpasswordchange` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `adminpasswordchange_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `adminaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminpasswordchange`
--

LOCK TABLES `adminpasswordchange` WRITE;
/*!40000 ALTER TABLE `adminpasswordchange` DISABLE KEYS */;
/*!40000 ALTER TABLE `adminpasswordchange` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminpasswordreset`
--

DROP TABLE IF EXISTS `adminpasswordreset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminpasswordreset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `expires_at` datetime NOT NULL,
  `expired` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `adminpasswordreset_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `adminaccount` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminpasswordreset`
--

LOCK TABLES `adminpasswordreset` WRITE;
/*!40000 ALTER TABLE `adminpasswordreset` DISABLE KEYS */;
INSERT INTO `adminpasswordreset` VALUES (1,'d3bf5266-95bb-486b-9e25-0d039ff888f5',2,'2025-11-26 03:24:22','2025-11-26 03:24:22','2025-11-26 03:54:22',0);
/*!40000 ALTER TABLE `adminpasswordreset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminsession`
--

DROP TABLE IF EXISTS `adminsession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminsession` (
  `id` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `expires_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `adminsession_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `adminaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminsession`
--

LOCK TABLES `adminsession` WRITE;
/*!40000 ALTER TABLE `adminsession` DISABLE KEYS */;
INSERT INTO `adminsession` VALUES ('3fb645f1-d0a2-4fdc-9fa2-a7a2a16fa5ec',2,'2025-11-26 03:25:11','2025-11-26 03:25:11','2025-12-26 03:25:11'),('4227f2ee-5051-44c2-9500-8da5bc86e582',2,'2025-11-26 03:24:59','2025-11-26 03:24:59','2025-12-26 03:24:59'),('56dd367f-3fca-4514-b2c3-4202e7b6bef6',1,'2025-11-27 10:53:23','2025-11-27 10:53:23','2025-12-27 10:53:23'),('8ecbceee-88da-4b92-b759-b4bdf9dd7450',1,'2025-11-26 02:38:51','2025-11-26 02:38:51','2025-12-26 02:38:51'),('e5f6659e-dec9-437d-9240-49af5d66eefe',1,'2025-11-26 16:18:35','2025-11-26 16:18:35','2025-12-26 16:18:35');
/*!40000 ALTER TABLE `adminsession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumniaccount`
--

DROP TABLE IF EXISTS `alumniaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumniaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) NOT NULL,
  `role` enum('sysad','peso','dean','alumni') NOT NULL,
  `email` varchar(256) NOT NULL,
  `pass_hash` varchar(256) NOT NULL,
  `avatar_filename` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `activated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumniaccount`
--

LOCK TABLES `alumniaccount` WRITE;
/*!40000 ALTER TABLE `alumniaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumniaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnipasswordchange`
--

DROP TABLE IF EXISTS `alumnipasswordchange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumnipasswordchange` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `alumnipasswordchange_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `alumniaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnipasswordchange`
--

LOCK TABLES `alumnipasswordchange` WRITE;
/*!40000 ALTER TABLE `alumnipasswordchange` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumnipasswordchange` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnipasswordreset`
--

DROP TABLE IF EXISTS `alumnipasswordreset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumnipasswordreset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `expires_at` datetime NOT NULL,
  `expired` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `alumnipasswordreset_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `alumniaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnipasswordreset`
--

LOCK TABLES `alumnipasswordreset` WRITE;
/*!40000 ALTER TABLE `alumnipasswordreset` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumnipasswordreset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnisession`
--

DROP TABLE IF EXISTS `alumnisession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumnisession` (
  `id` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `expires_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `alumnisession_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `alumniaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnisession`
--

LOCK TABLES `alumnisession` WRITE;
/*!40000 ALTER TABLE `alumnisession` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumnisession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sysadcompany`
--

DROP TABLE IF EXISTS `sysadcompany`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysadcompany` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `logo_filename` varchar(255) DEFAULT NULL,
  `letter_of_intent_filename` varchar(255) NOT NULL,
  `company_profile_filename` varchar(255) NOT NULL,
  `business_permit_filename` varchar(255) NOT NULL,
  `sec_filename` varchar(255) NOT NULL,
  `dti_cda_filename` varchar(255) NOT NULL,
  `reg_of_est_filename` varchar(255) NOT NULL,
  `dole_cert_filename` varchar(255) NOT NULL,
  `no_pending_case_cert_filename` varchar(255) NOT NULL,
  `philjob_reg_filename` varchar(255) NOT NULL,
  `validated` tinyint(1) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `sysad_creator_id` int(11) NOT NULL,
  `peso_validator_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sysad_creator_id` (`sysad_creator_id`),
  KEY `peso_validator_id` (`peso_validator_id`),
  CONSTRAINT `sysadcompany_ibfk_1` FOREIGN KEY (`sysad_creator_id`) REFERENCES `adminaccount` (`id`),
  CONSTRAINT `sysadcompany_ibfk_2` FOREIGN KEY (`peso_validator_id`) REFERENCES `adminaccount` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sysadcompany`
--

LOCK TABLES `sysadcompany` WRITE;
/*!40000 ALTER TABLE `sysadcompany` DISABLE KEYS */;
INSERT INTO `sysadcompany` VALUES (1,'GoCrayons','MydTGhYD_11-27-2025_01-30_AM.jpg','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','WEEK-12-SCS-4-2-Noli-Me-Tangere_11-26-2025_10-39_AM.pdf','Rizal Quiz_11-27-2025_01-39_AM.pdf',1,0,'2025-11-26 02:39:14','2025-11-26 02:39:14',1,2);
/*!40000 ALTER TABLE `sysadcompany` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sysadcompanyjob`
--

DROP TABLE IF EXISTS `sysadcompanyjob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysadcompanyjob` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `location` varchar(255) NOT NULL,
  `title` varchar(512) NOT NULL,
  `work_setup` enum('remote','on_site','hybrid') NOT NULL,
  `description` varchar(255) NOT NULL,
  `qualifications` varchar(255) NOT NULL,
  `roles_and_res` varchar(255) NOT NULL,
  `application_steps` varchar(255) NOT NULL,
  `monthly_pay` tinyint(1) NOT NULL,
  `total_vacancies` int(11) NOT NULL,
  `sysad_creator_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id` (`company_id`),
  KEY `sysad_creator_id` (`sysad_creator_id`),
  CONSTRAINT `sysadcompanyjob_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `sysadcompany` (`id`),
  CONSTRAINT `sysadcompanyjob_ibfk_2` FOREIGN KEY (`sysad_creator_id`) REFERENCES `adminaccount` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sysadcompanyjob`
--

LOCK TABLES `sysadcompanyjob` WRITE;
/*!40000 ALTER TABLE `sysadcompanyjob` DISABLE KEYS */;
INSERT INTO `sysadcompanyjob` VALUES (1,1,'2025-11-26 16:25:37','2025-11-26 16:25:37',0,'Silang, Cavite','Game Developer','on_site','Create fun and enjoyable games.','Humihinga','Magcode','And 5, 6, 7, 8',1,10,1);
/*!40000 ALTER TABLE `sysadcompanyjob` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sysadschool`
--

DROP TABLE IF EXISTS `sysadschool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysadschool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sysadschool`
--

LOCK TABLES `sysadschool` WRITE;
/*!40000 ALTER TABLE `sysadschool` DISABLE KEYS */;
/*!40000 ALTER TABLE `sysadschool` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 21:25:49
