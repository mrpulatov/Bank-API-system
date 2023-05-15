-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 15, 2023 at 06:51 PM
-- Server version: 8.0.30
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `accounts`
--


-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `balance` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `credit`
--

CREATE TABLE `credit` (
  `id` int NOT NULL,
  `account_id` int DEFAULT NULL,
  `total_amount` decimal(10,0) DEFAULT NULL,
  `interest` decimal(10,0) DEFAULT NULL,
  `final_price` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `credit`
--


-- --------------------------------------------------------

--
-- Table structure for table `credit_allocations`
--

CREATE TABLE `credit_allocations` (
  `credit_id` int DEFAULT NULL,
  `deposit_client_id` int DEFAULT NULL,
  `credit_client_id` int DEFAULT NULL,
  `amount_allocated` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `credit_allocations`
--

-- --------------------------------------------------------

--
-- Table structure for table `credit_clients`
--

CREATE TABLE `credit_clients` (
  `client_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `balance` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `credit_clients`
--

-- --------------------------------------------------------

--
-- Table structure for table `deposit_clients`
--

CREATE TABLE `deposit_clients` (
  `client_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `score` int DEFAULT NULL,
  `interest_rate` decimal(10,0) DEFAULT NULL,
  `balance_working` decimal(10,0) DEFAULT NULL,
  `balance_wait` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `deposit_clients`
--

-- --------------------------------------------------------

--
-- Table structure for table `repayment_schedule`
--

CREATE TABLE `repayment_schedule` (
  `credit_id` int DEFAULT NULL,
  `credit_client_id` int DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `credit_amount_due` decimal(10,0) DEFAULT NULL,
  `interest_amount_due` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `repayment_schedule`
--

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int NOT NULL,
  `account_id` int DEFAULT NULL,
  `amount` decimal(10,0) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transactions`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `credit`
--
ALTER TABLE `credit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_id` (`account_id`);

--
-- Indexes for table `credit_allocations`
--
ALTER TABLE `credit_allocations`
  ADD KEY `credit_id` (`credit_id`),
  ADD KEY `deposit_client_id` (`deposit_client_id`),
  ADD KEY `credit_client_id` (`credit_client_id`);

--
-- Indexes for table `credit_clients`
--
ALTER TABLE `credit_clients`
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `deposit_clients`
--
ALTER TABLE `deposit_clients`
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `repayment_schedule`
--
ALTER TABLE `repayment_schedule`
  ADD KEY `credit_id` (`credit_id`),
  ADD KEY `credit_client_id` (`credit_client_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_id` (`account_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT for table `credit`
--
ALTER TABLE `credit`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `credit`
--
ALTER TABLE `credit`
  ADD CONSTRAINT `credit_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`);

--
-- Constraints for table `credit_allocations`
--
ALTER TABLE `credit_allocations`
  ADD CONSTRAINT `credit_allocations_ibfk_1` FOREIGN KEY (`credit_id`) REFERENCES `credit` (`id`),
  ADD CONSTRAINT `credit_allocations_ibfk_2` FOREIGN KEY (`deposit_client_id`) REFERENCES `deposit_clients` (`client_id`),
  ADD CONSTRAINT `credit_allocations_ibfk_3` FOREIGN KEY (`credit_client_id`) REFERENCES `credit_clients` (`client_id`);

--
-- Constraints for table `credit_clients`
--
ALTER TABLE `credit_clients`
  ADD CONSTRAINT `credit_clients_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `accounts` (`id`);

--
-- Constraints for table `deposit_clients`
--
ALTER TABLE `deposit_clients`
  ADD CONSTRAINT `deposit_clients_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `accounts` (`id`);

--
-- Constraints for table `repayment_schedule`
--
ALTER TABLE `repayment_schedule`
  ADD CONSTRAINT `repayment_schedule_ibfk_1` FOREIGN KEY (`credit_id`) REFERENCES `credit` (`id`),
  ADD CONSTRAINT `repayment_schedule_ibfk_2` FOREIGN KEY (`credit_client_id`) REFERENCES `credit_clients` (`client_id`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
