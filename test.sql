-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 23, 2022 at 12:14 AM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.1.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `entertain_booking`
--

CREATE TABLE `entertain_booking` (
  `book_ID` int(11) NOT NULL,
  `user_id` varchar(300) DEFAULT NULL,
  `status` varchar(300) DEFAULT NULL,
  `name` varchar(300) DEFAULT NULL,
  `booking_type` varchar(300) DEFAULT NULL,
  `booking_detail` varchar(700) DEFAULT NULL,
  `booking_time` varchar(300) DEFAULT NULL,
  `phone_number` varchar(300) DEFAULT NULL,
  `book_date` varchar(300) DEFAULT NULL,
  `finish_date` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `entertain_quantities`
--

CREATE TABLE `entertain_quantities` (
  `item_ID` int(11) NOT NULL,
  `item_name` varchar(300) DEFAULT NULL,
  `total` varchar(50) DEFAULT NULL,
  `used` varchar(50) DEFAULT NULL,
  `available` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `entertain_quantities`
--

INSERT INTO `entertain_quantities` (`item_ID`, `item_name`, `total`, `used`, `available`) VALUES
(1, 'billiard_cue', '50', '0', '50'),
(2, 'billiard_helper_cue', '3', '0', '3'),
(3, 'ping_pong_ball', '24', '0', '24'),
(4, 'ping_pong_racket', '6', '0', '6'),
(5, 'small_football', '28', '0', '28'),
(6, 'kayram_wooden_rings', '8', '0', '8'),
(7, 'kayram_plastic_rings', '4', '0', '4'),
(8, 'chess', '6', '0', '6'),
(9, 'dominoes', '6', '0', '6'),
(10, 'wild_cards', '12', '0', '12'),
(11, 'uno', '6', '0', '6'),
(12, 'kayram_powder', '24', '0', '24'),
(13, 'ps4_controller', '6', '0', '6'),
(14, 'usb_cables', '6', '0', '6'),
(15, 'ps4_games', '12', '0', '12');

-- --------------------------------------------------------

--
-- Table structure for table `sale_log`
--

CREATE TABLE `sale_log` (
  `sale_ID` int(11) NOT NULL,
  `item_name` varchar(300) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `sale_type` varchar(50) DEFAULT NULL,
  `date` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `entertain_booking`
--
ALTER TABLE `entertain_booking`
  ADD PRIMARY KEY (`book_ID`);

--
-- Indexes for table `entertain_quantities`
--
ALTER TABLE `entertain_quantities`
  ADD PRIMARY KEY (`item_ID`);

--
-- Indexes for table `sale_log`
--
ALTER TABLE `sale_log`
  ADD PRIMARY KEY (`sale_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `entertain_booking`
--
ALTER TABLE `entertain_booking`
  MODIFY `book_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `entertain_quantities`
--
ALTER TABLE `entertain_quantities`
  MODIFY `item_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `sale_log`
--
ALTER TABLE `sale_log`
  MODIFY `sale_ID` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
