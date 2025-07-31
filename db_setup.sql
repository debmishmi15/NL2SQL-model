CREATE DATABASE IF NOT EXISTS fraud_detection;
USE fraud_detection;

CREATE TABLE IF NOT EXISTS branches (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_name VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    balance DECIMAL(15, 2),
    open_date DATE
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    amount DECIMAL(12, 2),
    transaction_date DATE,
    location VARCHAR(100),
    is_fraud BOOLEAN,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
