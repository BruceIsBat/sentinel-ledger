-- Sentinel-Ledger: Database Schema
-- Optimized for MySQL InnoDB Engine (ACID Compliant)

CREATE DATABASE IF NOT EXISTS sentinel_db;
USE sentinel_db;

CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(50) PRIMARY KEY,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT positive_balance CHECK (balance >= 0) -- Prevents overdraft at DB level
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id VARCHAR(50),
    recipient_id VARCHAR(50),
    amount DECIMAL(15, 2) NOT NULL,
    status ENUM('PENDING', 'SUCCESS', 'FAILED') DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES accounts(account_id),
    FOREIGN KEY (recipient_id) REFERENCES accounts(account_id)
) ENGINE=InnoDB;

INSERT INTO accounts (account_id, balance) VALUES ('USER_01', 5000.00), ('USER_02', 1000.00);