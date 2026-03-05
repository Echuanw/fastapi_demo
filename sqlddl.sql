create schema jwt_demo;

-- users 表：核心用户认证信息
CREATE TABLE jwt_demo.users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  username VARCHAR(50),
  password_hash VARCHAR(255) NOT NULL,  -- 存 bcrypt/scrypt/argon2 哈希
  role VARCHAR(20) NOT NULL DEFAULT 'user', -- 如 'user','admin'
  is_email_verified BOOLEAN NOT NULL DEFAULT FALSE,
  last_login_at TIMESTAMP NULL,
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 1) 注册（示例：应用层先验证 email/username 唯一并对密码做 bcrypt）
INSERT INTO jwt_demo.users (email, username, password_hash)
VALUES ('alice@example.com', 'alice', '<bcrypt_hash>')
RETURNING id, created_at;