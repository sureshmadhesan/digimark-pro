CREATE TYPE role_name AS ENUM ('Owner', 'Admin', 'Analyst');
CREATE TYPE platform_name AS ENUM ('google', 'meta');

CREATE TABLE organizations (
  id SERIAL PRIMARY KEY,
  business_name VARCHAR(255) NOT NULL,
  gst_number VARCHAR(30),
  billing_address TEXT,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  deleted_at TIMESTAMP
);

CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name role_name UNIQUE NOT NULL
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  organization_id INT REFERENCES organizations(id),
  role_id INT REFERENCES roles(id),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  deleted_at TIMESTAMP
);

CREATE TABLE ad_accounts (
  id SERIAL PRIMARY KEY,
  organization_id INT NOT NULL REFERENCES organizations(id),
  platform platform_name NOT NULL,
  external_account_id VARCHAR(255) NOT NULL,
  encrypted_access_token TEXT NOT NULL,
  encrypted_refresh_token TEXT,
  token_expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  deleted_at TIMESTAMP
);

CREATE TABLE campaigns (
  id SERIAL PRIMARY KEY,
  organization_id INT NOT NULL REFERENCES organizations(id),
  ad_account_id INT NOT NULL REFERENCES ad_accounts(id),
  name VARCHAR(255) NOT NULL,
  goal VARCHAR(100) NOT NULL,
  budget_daily FLOAT NOT NULL,
  status VARCHAR(50) DEFAULT 'draft',
  platform_campaign_id VARCHAR(255),
  wizard_payload JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  deleted_at TIMESTAMP
);

CREATE TABLE creatives (
  id SERIAL PRIMARY KEY,
  campaign_id INT NOT NULL REFERENCES campaigns(id),
  headline VARCHAR(255) NOT NULL,
  body TEXT NOT NULL,
  media_url VARCHAR(512),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  deleted_at TIMESTAMP
);

CREATE TABLE campaign_metrics (
  id SERIAL PRIMARY KEY,
  campaign_id INT NOT NULL REFERENCES campaigns(id),
  metric_date TIMESTAMP NOT NULL,
  impressions INT DEFAULT 0,
  clicks INT DEFAULT 0,
  cpc FLOAT DEFAULT 0,
  spend FLOAT DEFAULT 0
);

CREATE TABLE subscriptions (
  id SERIAL PRIMARY KEY,
  organization_id INT NOT NULL REFERENCES organizations(id),
  razorpay_subscription_id VARCHAR(255) UNIQUE NOT NULL,
  plan_code VARCHAR(100) NOT NULL,
  status VARCHAR(50) DEFAULT 'created',
  current_period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  deleted_at TIMESTAMP
);

CREATE TABLE payment_transactions (
  id SERIAL PRIMARY KEY,
  subscription_id INT NOT NULL REFERENCES subscriptions(id),
  razorpay_payment_id VARCHAR(255) UNIQUE NOT NULL,
  amount FLOAT NOT NULL,
  currency VARCHAR(5) DEFAULT 'INR',
  status VARCHAR(50) NOT NULL,
  raw_payload JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  organization_id INT REFERENCES organizations(id),
  actor_user_id INT REFERENCES users(id),
  event_type VARCHAR(100) NOT NULL,
  payload JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP DEFAULT now()
);
