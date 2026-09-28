-- Sentinel-Ledger: Database Schema
-- Optimized for MySQL InnoDB Engine (ACID Compliant)

CREATE DATABASE IF NOT EXISTS sentinel_ledger;
USE sentinel_ledger;

CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(50) PRIMARY KEY,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT positive_balance CHECK (balance >= 0) -- DB-level invariant preventing negative balance
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(64) PRIMARY KEY,
    sender_id VARCHAR(50) NOT NULL,
    recipient_id VARCHAR(50) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    status ENUM('PENDING', 'SUCCESS', 'FAILED') DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sender (sender_id),
    INDEX idx_recipient (recipient_id),
    FOREIGN KEY (sender_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (recipient_id) REFERENCES accounts(account_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Seed baseline test accounts for benchmarking and reproduction
INSERT INTO accounts (account_id, balance) 
VALUES 
    ('USER_01', 500000.00), 
    ('USER_02', 100000.00),
    ('USER_03', 250000.00),
    ('USER_04', 300000.00)
ON DUPLICATE KEY UPDATE balance=VALUES(balance);
