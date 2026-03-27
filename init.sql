-- INDpay Database Schema
-- Run this on a fresh MySQL instance
-- Auto-run via Docker entrypoint on first deploy

CREATE DATABASE IF NOT EXISTS INDpay CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE INDpay;

-- ─────────────────────────────────────────
-- USERS TABLE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `users` (
  `id`         INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name`       VARCHAR(80)   NOT NULL,
  `email`      VARCHAR(80)   NOT NULL UNIQUE,
  `username`   VARCHAR(25)   NOT NULL UNIQUE,
  `password`   VARCHAR(255)  NOT NULL,
  `balance`    DECIMAL(15,2) NOT NULL DEFAULT 0.00,
  `is_admin`   TINYINT(1)    NOT NULL DEFAULT 0,
  `is_active`  TINYINT(1)    NOT NULL DEFAULT 1,
  `created_at` DATETIME      DEFAULT CURRENT_TIMESTAMP,
  `last_login` DATETIME      DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────
-- TRANSACTIONS TABLE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `transactions` (
  `id`        INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `sender`    VARCHAR(25)   NOT NULL,
  `receiver`  VARCHAR(25)   NOT NULL,
  `amount`    DECIMAL(15,2) NOT NULL,
  `note`      VARCHAR(255)  DEFAULT NULL,
  `timestamp` DATETIME      DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_sender   (`sender`),
  INDEX idx_receiver (`receiver`),
  INDEX idx_timestamp(`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────
-- BLOCKCHAIN TABLE (kept for compatibility)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `blockchain` (
  `number`   VARCHAR(30)  DEFAULT NULL,
  `hash`     VARCHAR(68)  DEFAULT NULL,
  `previous` VARCHAR(68)  DEFAULT NULL,
  `data`     VARCHAR(255) DEFAULT NULL,
  `nonce`    VARCHAR(30)  DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────
-- DEFAULT ADMIN USER
-- Password: Admin@123  (change after first login!)
-- Hash generated with sha256_crypt
-- ─────────────────────────────────────────
INSERT IGNORE INTO `users` (name, email, username, password, balance, is_admin, is_active)
VALUES (
  'Administrator',
  'admin@indpay.local',
  'admin',
  '$5$rounds=535000$dBScgWgL/LgcWAl0$3EbwOlFGUwgQ1oKpeqGak/T306cQGkuX1Xtb5rWlz79',
  10000.00,
  1,
  1
);
