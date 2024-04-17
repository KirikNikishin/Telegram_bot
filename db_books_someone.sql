/*
 Navicat Premium Data Transfer

 Source Server         : MariaDataBase
 Source Server Type    : MariaDB
 Source Server Version : 101102 (10.11.2-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : db_books

 Target Server Type    : MariaDB
 Target Server Version : 101102 (10.11.2-MariaDB)
 File Encoding         : 65001

 Date: 21/04/2023 04:40:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for authors
-- ----------------------------
DROP TABLE IF EXISTS `authors`;
CREATE TABLE `authors`  (
  `Code_author` int(11) NOT NULL,
  `name_author` char(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Birthday` date NULL DEFAULT NULL,
  PRIMARY KEY (`Code_author`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of authors
-- ----------------------------
INSERT INTO `authors` VALUES (1, 'Erich Maria Remarque', '1898-06-22');
INSERT INTO `authors` VALUES (2, 'George Orwell', '1903-06-25');
INSERT INTO `authors` VALUES (3, 'Lev Nikolayevich Tolstoy', '1828-09-09');
INSERT INTO `authors` VALUES (4, 'Jules Verne', '1828-02-08');
INSERT INTO `authors` VALUES (5, 'Fyodor Mikhailovich Dostoyevsky', '1821-11-11');

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books`  (
  `Code_book` int(11) NOT NULL,
  `Title_book` char(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'BLANK',
  `Code_author` int(11) NULL DEFAULT NULL,
  `Pages` int(11) NULL DEFAULT NULL,
  `Code_publish` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`Code_book`) USING BTREE,
  INDEX `Code_author`(`Code_author`) USING BTREE,
  INDEX `Code_publish`(`Code_publish`) USING BTREE,
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`Code_author`) REFERENCES `authors` (`Code_author`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `books_ibfk_2` FOREIGN KEY (`Code_publish`) REFERENCES `publishing_house` (`Code_publish`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `CONSTRAINT_1` CHECK (`Pages` >= 5)
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of books
-- ----------------------------
INSERT INTO `books` VALUES (1, '1984', 2, 358, 4);
INSERT INTO `books` VALUES (2, 'Around the World in Eighty Days', 4, 383, 1);
INSERT INTO `books` VALUES (3, 'War and peace', 3, 832, 5);
INSERT INTO `books` VALUES (4, 'The Night in Lisbon', 5, 295, 2);
INSERT INTO `books` VALUES (5, 'Arch of Triumph', 1, 221, 1);

-- ----------------------------
-- Table structure for deliveries
-- ----------------------------
DROP TABLE IF EXISTS `deliveries`;
CREATE TABLE `deliveries`  (
  `Code_delivery` int(11) NOT NULL,
  `Name_delivery` char(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Name_company` char(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Address` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Phone` bigint(20) NULL DEFAULT NULL,
  `OGRN` bigint(13) NULL DEFAULT NULL,
  PRIMARY KEY (`Code_delivery`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of deliveries
-- ----------------------------
INSERT INTO `deliveries` VALUES (1, 'DHL', 'Arvesso', 'Malaya Bronnaya St, 78', 79155590507, 1082615134117);
INSERT INTO `deliveries` VALUES (2, 'DPD', 'Thrivematrix', 'Ulitsa Ostozhenka, 63', 79255508819, 4065305163447);
INSERT INTO `deliveries` VALUES (3, 'IML', 'Synerys', 'Taganskaya Ulitsa, 28', 79355556771, 2152451466726);
INSERT INTO `deliveries` VALUES (4, 'Pickpoint', 'Veloxainc', 'New Arbat Ave, 64', 79255508819, 7028885742868);
INSERT INTO `deliveries` VALUES (5, 'EMS', 'Lumosia', 'Sarinskiy Proyezd, 49', 79355556771, 3082925110892);

-- ----------------------------
-- Table structure for publishing_house
-- ----------------------------
DROP TABLE IF EXISTS `publishing_house`;
CREATE TABLE `publishing_house`  (
  `Code_publish` int(11) NOT NULL,
  `Publish` char(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `City` char(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Code_publish`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of publishing_house
-- ----------------------------
INSERT INTO `publishing_house` VALUES (1, 'AST Publishing Group', 'Moscow');
INSERT INTO `publishing_house` VALUES (2, 'Prosveshcheniye', 'Moscow');
INSERT INTO `publishing_house` VALUES (3, 'Rosman Publishing', 'Moscow');
INSERT INTO `publishing_house` VALUES (4, 'Izdatelstvo VES MIR', 'Moscow');
INSERT INTO `publishing_house` VALUES (5, 'Text Publishers', 'Moscow');

-- ----------------------------
-- Table structure for purchases
-- ----------------------------
DROP TABLE IF EXISTS `purchases`;
CREATE TABLE `purchases`  (
  `Code_purchase` int(11) NOT NULL,
  `Code_book` int(11) NULL DEFAULT NULL,
  `Date_order` date NULL DEFAULT NULL,
  `Code_delivery` int(11) NULL DEFAULT NULL,
  `Type_purchase` int(1) NULL DEFAULT NULL,
  `Cost` float NOT NULL,
  `Amount` float NOT NULL,
  PRIMARY KEY (`Code_purchase`) USING BTREE,
  INDEX `Code_book`(`Code_book`) USING BTREE,
  INDEX `Code_delivery`(`Code_delivery`) USING BTREE,
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`Code_book`) REFERENCES `books` (`Code_book`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`Code_delivery`) REFERENCES `deliveries` (`Code_delivery`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of purchases
-- ----------------------------
INSERT INTO `purchases` VALUES (1, 5, '2013-07-07', 2, 1, 207.95, 1600.68);
INSERT INTO `purchases` VALUES (2, 1, '2021-07-18', 4, 1, 634.28, 799.54);
INSERT INTO `purchases` VALUES (3, 3, '2000-02-08', 4, 1, 482.23, 2900.29);
INSERT INTO `purchases` VALUES (4, 3, '2021-06-28', 5, 1, 214.97, 230.81);
INSERT INTO `purchases` VALUES (5, 1, '2002-09-23', 3, 1, 416.08, 472.87);

-- ----------------------------
-- Function structure for AddInAuthors
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInAuthors`;
delimiter ;;
CREATE FUNCTION `AddInAuthors`(IN value_name_author CHAR(30), value_birthday DATETIME)
 RETURNS int(11)
BEGIN
	DECLARE counter INT;
	SELECT COUNT(Code_author) INTO counter FROM authors;
	SET counter = counter + 1;
	INSERT INTO authors (Code_author, name_author, Birthday)
	VALUES (counter, value_name_author, value_birthday);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInBooks
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInBooks`;
delimiter ;;
CREATE FUNCTION `AddInBooks`(IN value_title_book CHAR(40), IN value_code_author INT(11), IN value_pages INT(11), value_code_publish INT(11))
 RETURNS int(11)
BEGIN
	DECLARE counter INT;
	SELECT COUNT(Code_book) INTO counter FROM books;
	SET counter = counter + 1;
	INSERT INTO books (Code_book, title_book, code_author, pages, code_publish)
	VALUES (counter, value_title_book, value_code_author, value_pages, value_code_publish);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInDeliveries
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInDeliveries`;
delimiter ;;
CREATE FUNCTION `AddInDeliveries`(IN value_name_delivery CHAR(30), IN value_name_company CHAR(20), IN value_address VARCHAR(100), IN value_phone BIGINT(20), IN value_OGRN BIGINT(13))
 RETURNS int(11)
BEGIN
	DECLARE counter INT;
	SELECT COUNT(Code_delivery) INTO counter FROM deliveries;
	SET counter = counter + 1;
	INSERT INTO deliveries (Code_delivery, Name_delivery, Name_company, Address, Phone, OGRN)
	VALUES (counter, value_name_delivery, value_name_company, value_address, value_phone, value_OGRN);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInPublishingHouse
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInPublishingHouse`;
delimiter ;;
CREATE FUNCTION `AddInPublishingHouse`(IN value_publish CHAR(30), IN value_city CHAR(20))
 RETURNS int(11)
BEGIN
	DECLARE counter INT;
	
	SELECT COUNT(Code_publish) INTO counter FROM publishing_house;
	
	SET counter = counter + 1;
	
	INSERT INTO publishing_house (Code_publish, Publish, City)
	VALUES (counter, value_publish, value_city);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddInPurchases
-- ----------------------------
DROP FUNCTION IF EXISTS `AddInPurchases`;
delimiter ;;
CREATE FUNCTION `AddInPurchases`(IN value_code_book INT(11), IN value_date_order DATE, IN value_code_delivery INT(11), IN value_type_purchase INT(1), IN value_cost FLOAT, IN value_amount FLOAT)
 RETURNS int(11)
BEGIN
	DECLARE counter INT;
	
	SELECT COUNT(Code_purchase) INTO counter FROM purchases;
	
	SET counter = counter + 1;
	
	INSERT INTO purchases (Code_purchase, Code_book, Date_order, Code_delivery, Type_purchase, Cost, Amount)
	
	VALUES (counter, value_code_book, value_date_order, value_code_delivery, value_type_purchase, value_cost, value_amount);
	
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for CountDeliveries
-- ----------------------------
DROP FUNCTION IF EXISTS `CountDeliveries`;
delimiter ;;
CREATE FUNCTION `CountDeliveries`()
 RETURNS int(11)
BEGIN
	DECLARE counter INT;
	SELECT COUNT(Code_delivery) INTO counter FROM deliveries;
	IF counter > 5 OR counter <=> 1 THEN
		RETURN counter;
	END IF;
	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for CounterDeliveries
-- ----------------------------
DROP PROCEDURE IF EXISTS `CounterDeliveries`;
delimiter ;;
CREATE PROCEDURE `CounterDeliveries`()
BEGIN
	DECLARE counter INT;
	SELECT COUNT(Code_delivery) INTO counter FROM deliveries;
	
	IF counter > 5 OR (counter <=> 1) THEN
		SET @counter = CONVERT(counter, CHAR(30));
		SELECT CONCAT('В таблице ', @counter, ' поставщиков');
	END IF;
	
END
;;
delimiter ;

-- ----------------------------
-- Function structure for FindAvg
-- ----------------------------
DROP FUNCTION IF EXISTS `FindAvg`;
delimiter ;;
CREATE FUNCTION `FindAvg`()
 RETURNS float
BEGIN
	DECLARE avg FLOAT(10,2);
	SELECT AVG(Cost) INTO avg FROM purchases;
	SET avg = avg * 123.34; 
	RETURN avg;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for FindSum
-- ----------------------------
DROP FUNCTION IF EXISTS `FindSum`;
delimiter ;;
CREATE FUNCTION `FindSum`()
 RETURNS float
BEGIN
	DECLARE sum_books FLOAT(10,2);
	SELECT SUM(Amount) INTO sum_books FROM purchases;
	RETURN sum_books;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for publish_count
-- ----------------------------
DROP FUNCTION IF EXISTS `publish_count`;
delimiter ;;
CREATE FUNCTION `publish_count`()
 RETURNS float
BEGIN
	DECLARE publishing_house_counter INT;
	SELECT COUNT(Code_publish) INTO publishing_house_counter FROM publishing_house;
	
	IF publishing_house_counter <=> 0 THEN
		SET publishing_house_counter = 1;
	END IF;
	
	WHILE publishing_house_counter <= 20 DO
		INSERT INTO publishing_house
		VALUES (publishing_house_counter, 'is unknown', NULL);
		SET publishing_house_counter = publishing_house_counter + 1;
END WHILE;

	RETURN 0;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for WorkWithDate
-- ----------------------------
DROP FUNCTION IF EXISTS `WorkWithDate`;
delimiter ;;
CREATE FUNCTION `WorkWithDate`()
 RETURNS date
BEGIN
	DECLARE Date1 DATETIME;
	
	set Date1 = '2006-12-31 11:11:11';

	RETURN Date1;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for WorkWithText
-- ----------------------------
DROP PROCEDURE IF EXISTS `WorkWithText`;
delimiter ;;
CREATE PROCEDURE `WorkWithText`(IN text_source TEXT, OUT counter_letter_a INT, OUT counter_letter_v INT, OUT counter_letter_i INT, OUT counter_letter_p INT)
BEGIN
	-- SET @text_source = '';
	DECLARE counter INT;
	DECLARE letter CHAR(1);
	 -- DECLARE counter_letter_a INT;
	 -- DECLARE counter_letter_v INT;
	 -- DECLARE counter_letter_i INT;
	 -- DECLARE counter_letter_p INT;
	
	
	SET letter = 'a';
	SET counter = 0;
	SET counter_letter_a = 0;
	SET counter_letter_v = 0;
	SET counter_letter_i = 0;
	SET counter_letter_p = 0;


	WHILE counter <= LENGTH(text_source) DO
		SET letter = SUBSTR(text_source, counter, 1);
		
		IF(letter = 'a') THEN
			SET counter_letter_a = counter_letter_a + 1;
		END IF;
		
		IF(letter = 'v') THEN
			SET counter_letter_v = counter_letter_v + 1;
		END IF;
		
		IF(letter = 'i') THEN
			SET counter_letter_i = counter_letter_i + 1;
		END IF;
		
		IF(letter = 'p') THEN
			SET counter_letter_p = counter_letter_p + 1;
		END IF;
		
		SET counter = counter + 1;
	END WHILE;

	-- SELECT counter_letter_a, counter_letter_v, counter_letter_i, counter_letter_p;

END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
