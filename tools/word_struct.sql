-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: words
-- ------------------------------------------------------
-- Server version	5.6.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `lasthot`
--

DROP TABLE IF EXISTS `lasthot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lasthot` (
  `uid` varchar(100) NOT NULL,
  `word` varchar(1) NOT NULL,
  `hotness` float NOT NULL,
  PRIMARY KEY (`uid`,`word`),
  KEY `lasthot_fk` (`word`),
  KEY `lasthot_hotness_IDX` (`hotness`) USING BTREE,
  CONSTRAINT `lasthot_fk` FOREIGN KEY (`word`) REFERENCES `word` (`word`),
  CONSTRAINT `lasthot_fk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan`
--

DROP TABLE IF EXISTS `plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan` (
  `pid` bigint(20) NOT NULL AUTO_INCREMENT,
  `uid` varchar(100) NOT NULL,
  `word` varchar(1) NOT NULL,
  `date` date NOT NULL,
  `learned` tinyint(1) NOT NULL,
  PRIMARY KEY (`pid`),
  KEY `plan_fk` (`uid`),
  KEY `plan_fk_1` (`word`),
  KEY `plan_date_IDX` (`date`) USING BTREE,
  CONSTRAINT `plan_fk` FOREIGN KEY (`uid`) REFERENCES `user` (`id`),
  CONSTRAINT `plan_fk_1` FOREIGN KEY (`word`) REFERENCES `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=271 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `record` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(1) NOT NULL,
  `uid` varchar(100) NOT NULL,
  `time` datetime NOT NULL,
  `tag` int(11) NOT NULL DEFAULT '0',
  `date` date NOT NULL,
  `from` enum('query','plan','explore','review') NOT NULL,
  PRIMARY KEY (`rid`),
  KEY `rid_fk` (`word`),
  KEY `rid_fk_1` (`uid`),
  KEY `record_time_IDX` (`time`) USING BTREE,
  KEY `record_date_IDX` (`date`) USING BTREE,
  CONSTRAINT `rid_fk` FOREIGN KEY (`word`) REFERENCES `word` (`word`),
  CONSTRAINT `rid_fk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `lasthotdate` date DEFAULT NULL,
  `count` int(11) NOT NULL DEFAULT '10',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `word`
--

DROP TABLE IF EXISTS `word`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `word` (
  `id` int(11) NOT NULL,
  `word` varchar(1) NOT NULL,
  `pinyin` varchar(10) NOT NULL,
  `level` int(11) NOT NULL,
  `strokes` int(11) NOT NULL,
  `radicals` varchar(1) NOT NULL,
  PRIMARY KEY (`word`),
  KEY `word_id_IDX` (`id`,`level`) USING BTREE,
  KEY `word_pinyin_IDX` (`pinyin`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'words'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-24 20:26:26
