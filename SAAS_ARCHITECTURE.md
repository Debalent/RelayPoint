# RelayPoint — Full Enterprise SaaS Architecture

**Version:** 2.0 Production Design  
**Date:** February 23, 2026  
**Status:** Authoritative Architecture Specification  
**Classification:** Enterprise Internal

---

## Table of Contents

1. [Executive System Overview](#1-executive-system-overview)
2. [Full SaaS System Architecture](#2-full-saas-system-architecture)
3. [Database Schema](#3-database-schema)
4. [Component Map](#4-component-map)
5. [Page Map](#5-page-map)
6. [Pricing Table](#6-pricing-table)
7. [Billing Logic Breakdown](#7-billing-logic-breakdown)
8. [Contract Logic Model](#8-contract-logic-model)
9. [Deployment Roadmap](#9-deployment-roadmap)
10. [Scaling Roadmap](#10-scaling-roadmap)

---

## 1. Executive System Overview

RelayPoint is a multi-tenant, subscription-driven SaaS platform purpose-built for hospitality and service industry operations. It eliminates operational breakdowns — missed handoffs, scheduling conflicts, incident delays, compliance drift, and communication failures — across restaurants, hotels, bars, event venues, cleaning services, maintenance teams, and multi-location hospitality groups.

### Core Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Multi-Tenancy** | Schema-per-tenant PostgreSQL isolation + tenant_id row-level security on all shared tables |
| **API-First** | All features exposed via versioned REST + GraphQL APIs; no server-side rendering logic |
| **Mobile-First** | React Native Web single codebase; touch-first UI components; offline-first PWA |
| **Zero Trust Security** | JWT + Auth0; RBAC at API, DB, and UI layers; per-resource ACL |
| **Subscription-Native** | Stripe Billing with metered usage, tier gating, contract terms, and proration logic built into core |
| **Serverless Compatible** | FastAPI deployed on AWS Lambda via Mangum adapter or as containerized ECS/Kubernetes service |
| **GitOps Deployment** | GitHub Actions → Docker → ECS/K8s; frontend static export to GitHub Pages / Cloudflare Pages |

---

## 2. Full SaaS System Architecture

### 2.1 System Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Web App     │  │  iOS App     │  │  Android App         │  │
│  │  (Next.js    │  │  (RN Native) │  │  (RN Native)         │  │
│  │   static)    │  │              │  │                      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │              │
└─────────┼─────────────────┼──────────────────────┼─────────────┘
          │                 │                      │
          ▼                 ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CDN / EDGE LAYER                           │
│            Cloudflare CDN · GitHub Pages · WAF                   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API GATEWAY LAYER                            │
│         AWS API Gateway · Kong · Rate Limiting · Auth            │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  REST API v1     │   │  WebSocket       │   │  Webhook         │
│  FastAPI/Python  │   │  Server          │   │  Processor       │
│  (Mangum/ECS)    │   │  (Redis Pub/Sub) │   │  (Celery)        │
└────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  PostgreSQL 15   │  │  Redis 7         │  │  S3 / R2         │
│  Multi-schema    │  │  Cache + PubSub  │  │  File Storage    │
│  TimescaleDB     │  │  Session Store   │  │  Photo/Video     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────────────────┐
│                  BACKGROUND SERVICES LAYER                    │
│  Celery Beat · Task Scheduler · Billing Sync · Email/SMS      │
│  Stripe Webhooks · Contract Renewal Engine · Audit Logger    │
└──────────────────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────────────────┐
│                OBSERVABILITY STACK                            │
│  Prometheus + Grafana · Sentry · Structlog · Datadog         │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 Tech Stack Specification

#### Frontend

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | Next.js 14 (App Router, static export) | SSG for GitHub Pages; RSC for performance |
| **Cross-Platform** | React Native Web | Single codebase → iOS, Android, Web |
| **State Management** | Redux Toolkit + RTK Query | Normalized cache, optimistic updates |
| **Component Library** | shadcn/ui + Tailwind CSS | Accessible, composable, theme-able |
| **Forms** | React Hook Form + Zod | Type-safe validation, no re-renders |
| **Real-Time** | Socket.IO client / native WebSocket | Live notifications, task updates |
| **Offline & PWA** | Workbox + next-pwa | Service worker, background sync |
| **Charts** | Recharts + Victory Native | Unified charting web + mobile |
| **Drag & Drop** | dnd-kit | Accessible, performant scheduling UI |
| **Date/Time** | date-fns + react-day-picker | Lightweight, tree-shakeable |
| **Authentication** | Auth0 React SDK | PKCE flow, SSO, MFA |
| **File Upload** | react-dropzone + S3 presigned URLs | Direct-to-S3 upload, no server bottleneck |
| **Internationalization** | next-intl | Dynamic locale loading |
| **Build** | Turbopack / Webpack 5 | Module federation, code splitting |
| **CI/CD** | GitHub Actions | Static export → GitHub Pages / Cloudflare |

#### Backend

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | FastAPI 0.110 + Python 3.12 | Async-native, auto-OpenAPI, performance |
| **ORM** | SQLAlchemy 2.0 (async) | Type-safe, compiled queries |
| **Migrations** | Alembic | Versioned schema with tenant provisioning hooks |
| **Auth** | Auth0 + python-jose | JWT validation, JWKS caching |
| **Task Queue** | Celery 5 + Redis broker | Background jobs, scheduling, billing cron |
| **WebSockets** | FastAPI WebSocket + Redis Pub/Sub | Fan-out to tenant channels |
| **Email** | SendGrid API | Transactional email, dunning sequences |
| **SMS** | Twilio API | Shift alerts, incident escalation |
| **Push Notifications** | Firebase Cloud Messaging | Mobile push for tasks/incidents |
| **Payments** | Stripe Billing + Connect | Subscriptions, invoices, contract terms |
| **File Processing** | AWS S3 + boto3 | Presigned upload/download, lifecycle rules |
| **Rate Limiting** | slowapi + Redis | Per-tenant, per-IP sliding window |
| **Observability** | Structlog + Prometheus + Sentry | Production error tracking + metrics |
| **Serverless Adapter** | Mangum | Deploy FastAPI to AWS Lambda |

#### Infrastructure

| Layer | Technology |
|-------|-----------|
| **Containerization** | Docker + Docker Compose |
| **Orchestration** | Kubernetes (EKS) / Docker Swarm (smaller) |
| **Helm Charts** | `/helm/relaypoint/` (existing) |
| **IaC** | Terraform (AWS provider) |
| **Secrets** | AWS Secrets Manager / HashiCorp Vault |
| **DNS** | Cloudflare |
| **CDN** | Cloudflare CDN + GitHub Pages |
| **Database** | AWS RDS PostgreSQL 15 + TimescaleDB extension |
| **Cache** | AWS ElastiCache Redis 7 |
| **Object Storage** | AWS S3 / Cloudflare R2 |
| **Monitoring** | Prometheus + Grafana (existing `/docker/prometheus/`) |
| **Logging** | CloudWatch Logs + Elasticsearch |

### 2.3 Multi-Tenant Architecture

RelayPoint uses a **hybrid multi-tenancy model**:

- **Shared schema** for platform-level tables (tenants, subscriptions, plans, billing)
- **Row-Level Security (RLS)** enforced via `tenant_id` foreign keys on all operational tables
- **PostgreSQL RLS policies** set `app.current_tenant_id` session variable at connection checkout
- **Schema isolation available** for Enterprise-tier tenants (dedicated schema per org)

```sql
-- Session-variable based tenant isolation
SET app.current_tenant_id = '{{tenant_uuid}}';

-- RLS Policy Example
CREATE POLICY tenant_isolation ON tasks
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

**Connection pooling:** PgBouncer with transaction-mode pooling. Tenant context injected via connection checkout hook in SQLAlchemy's `event.listen("connect")`.

### 2.4 Feature Flag & Tier Gating

All API endpoints check subscription tier against a feature registry:

```python
FEATURE_GATES = {
    "shift_handoff":        ["free","team","pro","enterprise"],
    "task_automation":      ["team","pro","enterprise"],
    "incident_management":  ["pro","enterprise"],
    "sop_hub":              ["pro","enterprise"],
    "analytics_advanced":   ["pro","enterprise"],
    "scheduling":           ["team","pro","enterprise"],
    "api_access":           ["enterprise"],
    "multi_location":       ["enterprise"],
    "custom_automation":    ["enterprise"],
    "white_label":          ["enterprise"],
    "contract_5yr":         ["enterprise"],
    "qr_incident_reporting":["pro","enterprise"],
    "payroll_export":       ["pro","enterprise"],
    "ai_forecasting":       ["pro","enterprise"],
    "sso":                  ["enterprise"],
    "audit_logs_90d":       ["pro","enterprise"],
    "audit_logs_unlimited": ["enterprise"],
    "priority_support":     ["enterprise"],
}
```

---

## 3. Database Schema

### 3.1 Schema Namespace

```
public/                     ← Platform tables (tenants, billing, auth)
  tenants
  plans
  subscriptions
  contracts
  invoices
  invoice_items
  payment_methods
  seats
  locations
  feature_flags

operational/                ← Per-tenant data (RLS applied)
  users
  roles
  role_permissions
  teams
  team_members
  shift_handoffs
  handoff_items
  handoff_attachments
  tasks
  task_assignments
  task_escalations
  incidents
  incident_attachments
  incident_comments
  maintenance_tickets
  schedules
  shifts
  shift_swaps
  availability_submissions
  messages
  channels
  channel_members
  message_reads
  announcements
  sop_documents
  sop_acknowledgments
  sop_versions
  audit_logs
  analytics_events (TimescaleDB hypertable)
```

### 3.2 Core Platform Tables

```sql
-- ─────────────────────────────────────────────────
-- TENANTS
-- ─────────────────────────────────────────────────
CREATE TABLE tenants (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                        VARCHAR(255)    NOT NULL,
    slug                        VARCHAR(100)    UNIQUE NOT NULL,
    domain                      VARCHAR(255)    UNIQUE,
    industry                    VARCHAR(50)     NOT NULL DEFAULT 'hospitality',
    status                      VARCHAR(20)     NOT NULL DEFAULT 'trial'
                                    CHECK (status IN ('trial','active','suspended','cancelled','pending')),
    plan_tier                   VARCHAR(20)     NOT NULL DEFAULT 'free'
                                    CHECK (plan_tier IN ('free','team','pro','enterprise','custom')),
    
    -- Stripe
    stripe_customer_id          VARCHAR(100)    UNIQUE,
    stripe_subscription_id      VARCHAR(100)    UNIQUE,
    
    -- Trial
    trial_ends_at               TIMESTAMPTZ,
    
    -- Subscription window
    subscription_starts_at      TIMESTAMPTZ,
    subscription_ends_at        TIMESTAMPTZ,
    
    -- Quotas
    max_seats                   INTEGER         NOT NULL DEFAULT 5,
    max_locations               INTEGER         NOT NULL DEFAULT 1,
    max_storage_gb              INTEGER         NOT NULL DEFAULT 5,
    max_api_requests_per_day    INTEGER         NOT NULL DEFAULT 1000,
    
    -- Current usage
    current_seats               INTEGER         NOT NULL DEFAULT 0,
    current_locations           INTEGER         NOT NULL DEFAULT 0,
    current_storage_gb          NUMERIC(10,2)   NOT NULL DEFAULT 0,
    
    -- White-label / branding
    branding                    JSONB           NOT NULL DEFAULT '{}',
    
    -- Settings
    settings                    JSONB           NOT NULL DEFAULT '{}',
    timezone                    VARCHAR(64)     NOT NULL DEFAULT 'UTC',
    locale                      VARCHAR(10)     NOT NULL DEFAULT 'en-US',
    
    -- Metadata
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    deleted_at                  TIMESTAMPTZ
);

CREATE INDEX idx_tenants_slug     ON tenants(slug);
CREATE INDEX idx_tenants_status   ON tenants(status);
CREATE INDEX idx_tenants_plan     ON tenants(plan_tier);
CREATE INDEX idx_tenants_stripe   ON tenants(stripe_customer_id);

-- ─────────────────────────────────────────────────
-- PLANS
-- ─────────────────────────────────────────────────
CREATE TABLE plans (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                        VARCHAR(100)    NOT NULL,
    tier                        VARCHAR(20)     NOT NULL
                                    CHECK (tier IN ('free','team','pro','enterprise','custom')),
    
    -- Base pricing (monthly)
    base_price_monthly          NUMERIC(10,2)   NOT NULL DEFAULT 0,
    price_per_seat_monthly      NUMERIC(10,2)   NOT NULL DEFAULT 0,
    price_per_location_monthly  NUMERIC(10,2)   NOT NULL DEFAULT 0,
    
    -- Annual pricing (pre-discounted)
    base_price_annual           NUMERIC(10,2)   NOT NULL DEFAULT 0,
    price_per_seat_annual       NUMERIC(10,2)   NOT NULL DEFAULT 0,
    price_per_location_annual   NUMERIC(10,2)   NOT NULL DEFAULT 0,
    
    -- Included quotas
    included_seats              INTEGER         NOT NULL DEFAULT 5,
    included_locations          INTEGER         NOT NULL DEFAULT 1,
    included_storage_gb         INTEGER         NOT NULL DEFAULT 5,
    
    -- Stripe price IDs
    stripe_price_id_monthly     VARCHAR(100),
    stripe_price_id_annual      VARCHAR(100),
    
    -- Feature flags (JSON array of feature keys)
    features                    JSONB           NOT NULL DEFAULT '[]',
    
    is_active                   BOOLEAN         NOT NULL DEFAULT TRUE,
    is_public                   BOOLEAN         NOT NULL DEFAULT TRUE,
    sort_order                  INTEGER         NOT NULL DEFAULT 0,
    
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────────────
-- SUBSCRIPTIONS
-- ─────────────────────────────────────────────────
CREATE TABLE subscriptions (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id                   UUID            NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    plan_id                     UUID            NOT NULL REFERENCES plans(id),
    
    -- Stripe
    stripe_subscription_id      VARCHAR(100)    UNIQUE,
    stripe_customer_id          VARCHAR(100),
    
    status                      VARCHAR(30)     NOT NULL DEFAULT 'active'
                                    CHECK (status IN ('trialing','active','past_due','canceled','unpaid','paused')),
    
    billing_cycle               VARCHAR(20)     NOT NULL DEFAULT 'monthly'
                                    CHECK (billing_cycle IN ('monthly','annual','2year','3year','5year')),
    
    -- Seat & location counts
    seat_count                  INTEGER         NOT NULL DEFAULT 1,
    location_count              INTEGER         NOT NULL DEFAULT 1,
    
    -- Pricing snapshot at time of subscription
    effective_monthly_rate      NUMERIC(10,2)   NOT NULL DEFAULT 0,
    
    -- Contract fields
    contract_term_months        INTEGER,        -- NULL = month-to-month
    contract_start_date         TIMESTAMPTZ,
    contract_end_date           TIMESTAMPTZ,
    auto_renew                  BOOLEAN         NOT NULL DEFAULT TRUE,
    
    -- Discount
    discount_percent            NUMERIC(5,2)    NOT NULL DEFAULT 0,
    discount_reason             VARCHAR(255),
    
    -- Billing dates
    current_period_start        TIMESTAMPTZ,
    current_period_end          TIMESTAMPTZ,
    cancel_at_period_end        BOOLEAN         NOT NULL DEFAULT FALSE,
    canceled_at                 TIMESTAMPTZ,
    
    -- Volume pricing thresholds applied
    volume_discount_percent     NUMERIC(5,2)    NOT NULL DEFAULT 0,
    
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_tenant     ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_status     ON subscriptions(status);
CREATE INDEX idx_subscriptions_stripe     ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_subscriptions_contract_end ON subscriptions(contract_end_date);

-- ─────────────────────────────────────────────────
-- CONTRACTS (Enterprise long-term)
-- ─────────────────────────────────────────────────
CREATE TABLE contracts (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id                   UUID            NOT NULL REFERENCES tenants(id),
    subscription_id             UUID            NOT NULL REFERENCES subscriptions(id),
    
    contract_type               VARCHAR(30)     NOT NULL DEFAULT 'standard'
                                    CHECK (contract_type IN ('standard','enterprise','custom','pilot')),
    term_months                 INTEGER         NOT NULL,   -- 12, 24, 36, 60
    
    start_date                  TIMESTAMPTZ     NOT NULL,
    end_date                    TIMESTAMPTZ     NOT NULL,
    
    -- Financial terms
    total_contract_value        NUMERIC(12,2)   NOT NULL,
    annual_contract_value       NUMERIC(12,2)   NOT NULL,
    monthly_effective_rate      NUMERIC(10,2)   NOT NULL,
    discount_percent            NUMERIC(5,2)    NOT NULL DEFAULT 0,
    
    -- Early termination
    early_termination_fee_type  VARCHAR(30)     NOT NULL DEFAULT 'remaining_balance_50pct'
                                    CHECK (early_termination_fee_type IN
                                        ('flat_fee','remaining_balance_50pct','remaining_balance_100pct','none')),
    early_termination_fee_flat  NUMERIC(10,2),
    
    -- Renewal
    auto_renew                  BOOLEAN         NOT NULL DEFAULT TRUE,
    renewal_notice_days         INTEGER         NOT NULL DEFAULT 90,
    renewal_term_months         INTEGER,        -- if different from original term
    renewal_locked_rate         BOOLEAN         NOT NULL DEFAULT FALSE,
    renewal_rate_increase_cap   NUMERIC(5,2),   -- max % increase on renewal
    
    -- Signed state
    status                      VARCHAR(20)     NOT NULL DEFAULT 'pending'
                                    CHECK (status IN ('draft','pending','active','expired','terminated','renewed')),
    signed_at                   TIMESTAMPTZ,
    signed_by_user_id           UUID,
    countersigned_at            TIMESTAMPTZ,
    
    -- Document storage
    contract_document_url       VARCHAR(1024),
    
    -- Metadata
    notes                       TEXT,
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contracts_tenant         ON contracts(tenant_id);
CREATE INDEX idx_contracts_end_date       ON contracts(end_date);
CREATE INDEX idx_contracts_status         ON contracts(status);

-- ─────────────────────────────────────────────────
-- LOCATIONS (Per-tenant, but platform-managed)
-- ─────────────────────────────────────────────────
CREATE TABLE locations (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id                   UUID            NOT NULL REFERENCES tenants(id),
    name                        VARCHAR(255)    NOT NULL,
    slug                        VARCHAR(100)    NOT NULL,
    address                     JSONB,
    timezone                    VARCHAR(64)     NOT NULL DEFAULT 'UTC',
    is_active                   BOOLEAN         NOT NULL DEFAULT TRUE,
    settings                    JSONB           NOT NULL DEFAULT '{}',
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, slug)
);

CREATE INDEX idx_locations_tenant ON locations(tenant_id);

-- ─────────────────────────────────────────────────
-- INVOICES
-- ─────────────────────────────────────────────────
CREATE TABLE invoices (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id                   UUID            NOT NULL REFERENCES tenants(id),
    subscription_id             UUID            REFERENCES subscriptions(id),
    stripe_invoice_id           VARCHAR(100)    UNIQUE,
    
    status                      VARCHAR(20)     NOT NULL DEFAULT 'draft'
                                    CHECK (status IN ('draft','open','paid','uncollectible','void')),
    
    amount_due                  NUMERIC(10,2)   NOT NULL,
    amount_paid                 NUMERIC(10,2)   NOT NULL DEFAULT 0,
    amount_remaining            NUMERIC(10,2)   NOT NULL,
    currency                    VARCHAR(3)      NOT NULL DEFAULT 'usd',
    
    invoice_date                TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    due_date                    TIMESTAMPTZ,
    paid_at                     TIMESTAMPTZ,
    
    billing_period_start        TIMESTAMPTZ,
    billing_period_end          TIMESTAMPTZ,
    
    -- Tax
    tax_percent                 NUMERIC(5,2)    NOT NULL DEFAULT 0,
    tax_amount                  NUMERIC(10,2)   NOT NULL DEFAULT 0,
    
    -- PDF
    invoice_pdf_url             VARCHAR(1024),
    
    -- Dunning
    last_payment_attempt        TIMESTAMPTZ,
    payment_attempt_count       INTEGER         NOT NULL DEFAULT 0,
    next_payment_attempt        TIMESTAMPTZ,
    
    metadata                    JSONB,
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_invoices_tenant  ON invoices(tenant_id);
CREATE INDEX idx_invoices_status  ON invoices(status);
CREATE INDEX idx_invoices_due     ON invoices(due_date);
```

### 3.3 Operational Tables (Row-Level Security Applied)

```sql
-- ─────────────────────────────────────────────────
-- USERS (extended from existing model)
-- ─────────────────────────────────────────────────
CREATE TABLE users (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID        NOT NULL REFERENCES tenants(id),
    location_id             UUID        REFERENCES locations(id),
    
    email                   VARCHAR(255) NOT NULL,
    phone                   VARCHAR(20),
    name                    VARCHAR(255) NOT NULL,
    avatar_url              VARCHAR(1024),
    
    auth0_user_id           VARCHAR(255) UNIQUE,
    
    status                  VARCHAR(20) NOT NULL DEFAULT 'active'
                                CHECK (status IN ('active','inactive','suspended','pending_invite')),
    
    role_id                 UUID        REFERENCES roles(id),
    department              VARCHAR(100),
    job_title               VARCHAR(100),
    
    -- Notification preferences
    notifications_email     BOOLEAN     NOT NULL DEFAULT TRUE,
    notifications_sms       BOOLEAN     NOT NULL DEFAULT FALSE,
    notifications_push      BOOLEAN     NOT NULL DEFAULT TRUE,
    
    -- Seat billing tracking
    seat_type               VARCHAR(20) NOT NULL DEFAULT 'full'
                                CHECK (seat_type IN ('full','limited','manager','viewer')),
    
    last_active_at          TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at              TIMESTAMPTZ,
    
    UNIQUE (tenant_id, email)
);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- ─────────────────────────────────────────────────
-- ROLES & PERMISSIONS
-- ─────────────────────────────────────────────────
CREATE TABLE roles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES tenants(id),
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(50)  NOT NULL,
    is_system_role  BOOLEAN     NOT NULL DEFAULT FALSE,
    permissions     JSONB       NOT NULL DEFAULT '[]',
    color           VARCHAR(7),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, slug)
);

-- System roles seeded on tenant creation:
-- owner, admin, manager, staff, viewer, maintenance, housekeeping, front_desk

-- ─────────────────────────────────────────────────
-- SHIFT HANDOFFS
-- ─────────────────────────────────────────────────
CREATE TABLE shift_handoffs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID        NOT NULL REFERENCES tenants(id),
    location_id         UUID        NOT NULL REFERENCES locations(id),
    
    submitted_by        UUID        NOT NULL REFERENCES users(id),
    received_by         UUID        REFERENCES users(id),
    
    shift_date          DATE        NOT NULL,
    shift_start         TIMESTAMPTZ NOT NULL,
    shift_end           TIMESTAMPTZ,
    shift_type          VARCHAR(50) NOT NULL,  -- morning, afternoon, night, etc.
    department          VARCHAR(100),
    
    status              VARCHAR(20) NOT NULL DEFAULT 'open'
                            CHECK (status IN ('open','acknowledged','completed','flagged')),
    
    overall_notes       TEXT,
    priority_level      VARCHAR(10) NOT NULL DEFAULT 'normal'
                            CHECK (priority_level IN ('low','normal','high','critical')),
    
    has_incidents       BOOLEAN     NOT NULL DEFAULT FALSE,
    guest_count         INTEGER,
    occupancy_percent   NUMERIC(5,2),
    
    template_id         UUID,
    
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE handoff_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    handoff_id      UUID        NOT NULL REFERENCES shift_handoffs(id) ON DELETE CASCADE,
    tenant_id       UUID        NOT NULL,
    
    category        VARCHAR(50) NOT NULL,   -- task, incident, note, guest_request
    content         TEXT        NOT NULL,
    priority_tag    VARCHAR(20),
    is_resolved     BOOLEAN     NOT NULL DEFAULT FALSE,
    requires_followup BOOLEAN   NOT NULL DEFAULT FALSE,
    assigned_to     UUID        REFERENCES users(id),
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE handoff_attachments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    handoff_id      UUID        NOT NULL REFERENCES shift_handoffs(id) ON DELETE CASCADE,
    tenant_id       UUID        NOT NULL,
    uploader_id     UUID        NOT NULL REFERENCES users(id),
    
    file_type       VARCHAR(20) NOT NULL CHECK (file_type IN ('image','video','document')),
    file_url        VARCHAR(1024) NOT NULL,
    file_size_bytes INTEGER,
    caption         TEXT,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────────────
-- TASKS
-- ─────────────────────────────────────────────────
CREATE TABLE tasks (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID        NOT NULL REFERENCES tenants(id),
    location_id         UUID        REFERENCES locations(id),
    
    title               VARCHAR(500) NOT NULL,
    description         TEXT,
    
    type                VARCHAR(30) NOT NULL DEFAULT 'one_time'
                            CHECK (type IN ('one_time','recurring','checklist','approval')),
    status              VARCHAR(20) NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','in_progress','blocked','completed','cancelled','overdue')),
    priority            VARCHAR(10) NOT NULL DEFAULT 'normal'
                            CHECK (priority IN ('low','normal','high','critical')),
    
    created_by          UUID        NOT NULL REFERENCES users(id),
    assigned_to_user_id UUID        REFERENCES users(id),
    assigned_to_role_id UUID        REFERENCES roles(id),
    
    -- Scheduling / recurrence
    due_date            TIMESTAMPTZ,
    starts_at           TIMESTAMPTZ,
    recurrence_rule     TEXT,    -- iCalendar RRULE string
    recurrence_parent_id UUID    REFERENCES tasks(id),
    
    -- Context
    department          VARCHAR(100),
    guest_room          VARCHAR(50),
    guest_name          VARCHAR(255),
    guest_impact        BOOLEAN     NOT NULL DEFAULT FALSE,
    
    -- Escalation
    escalation_threshold_minutes INTEGER,
    escalated_at        TIMESTAMPTZ,
    escalated_to        UUID        REFERENCES users(id),
    
    -- Completion
    completed_by        UUID        REFERENCES users(id),
    completed_at        TIMESTAMPTZ,
    verified_by         UUID        REFERENCES users(id),
    verified_at         TIMESTAMPTZ,
    
    -- Manager approval
    requires_approval   BOOLEAN     NOT NULL DEFAULT FALSE,
    approved_by         UUID        REFERENCES users(id),
    approved_at         TIMESTAMPTZ,
    
    tags                TEXT[],
    metadata            JSONB       NOT NULL DEFAULT '{}',
    
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON tasks
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

CREATE INDEX idx_tasks_tenant         ON tasks(tenant_id);
CREATE INDEX idx_tasks_status         ON tasks(status);
CREATE INDEX idx_tasks_due            ON tasks(due_date);
CREATE INDEX idx_tasks_assigned_user  ON tasks(assigned_to_user_id);
CREATE INDEX idx_tasks_location       ON tasks(location_id);

-- ─────────────────────────────────────────────────
-- INCIDENTS
-- ─────────────────────────────────────────────────
CREATE TABLE incidents (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID        NOT NULL REFERENCES tenants(id),
    location_id             UUID        NOT NULL REFERENCES locations(id),
    
    title                   VARCHAR(500) NOT NULL,
    description             TEXT,
    
    category                VARCHAR(50) NOT NULL,
                                -- maintenance, safety, guest_complaint, equipment,
                                -- cleaning, security, medical, other
    severity                VARCHAR(10) NOT NULL DEFAULT 'medium'
                                CHECK (severity IN ('low','medium','high','critical')),
    status                  VARCHAR(20) NOT NULL DEFAULT 'open'
                                CHECK (status IN ('open','assigned','in_progress','resolved','closed')),
    
    reported_by             UUID        REFERENCES users(id),
    reported_via            VARCHAR(20) NOT NULL DEFAULT 'app'
                                CHECK (reported_via IN ('app','qr_code','email','phone','api')),
    
    assigned_to             UUID        REFERENCES users(id),
    
    -- Location context
    area                    VARCHAR(255),    -- Room 214, Pool Area, Kitchen
    qr_code_id              VARCHAR(100),    -- If reported via QR
    
    -- Escalation
    escalation_timer_minutes INTEGER,
    escalated_at            TIMESTAMPTZ,
    escalated_to            UUID        REFERENCES users(id),
    escalation_count        INTEGER     NOT NULL DEFAULT 0,
    
    -- Resolution
    resolved_by             UUID        REFERENCES users(id),
    resolved_at             TIMESTAMPTZ,
    resolution_notes        TEXT,
    
    -- SLA tracking
    response_due_at         TIMESTAMPTZ,
    resolution_due_at       TIMESTAMPTZ,
    first_response_at       TIMESTAMPTZ,
    
    tags                    TEXT[],
    metadata                JSONB       NOT NULL DEFAULT '{}',
    
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE incidents ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON incidents
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

CREATE INDEX idx_incidents_tenant       ON incidents(tenant_id);
CREATE INDEX idx_incidents_status       ON incidents(status);
CREATE INDEX idx_incidents_severity     ON incidents(severity);
CREATE INDEX idx_incidents_location     ON incidents(location_id);

-- ─────────────────────────────────────────────────
-- SCHEDULING
-- ─────────────────────────────────────────────────
CREATE TABLE schedules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES tenants(id),
    location_id     UUID        NOT NULL REFERENCES locations(id),
    name            VARCHAR(255) NOT NULL,
    week_start      DATE        NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'draft'
                        CHECK (status IN ('draft','published','locked')),
    published_by    UUID        REFERENCES users(id),
    published_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE shifts (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID        NOT NULL REFERENCES tenants(id),
    schedule_id         UUID        NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
    location_id         UUID        NOT NULL REFERENCES locations(id),
    
    user_id             UUID        NOT NULL REFERENCES users(id),
    role_id             UUID        REFERENCES roles(id),
    
    shift_date          DATE        NOT NULL,
    start_time          TIMESTAMPTZ NOT NULL,
    end_time            TIMESTAMPTZ NOT NULL,
    break_minutes       INTEGER     NOT NULL DEFAULT 0,
    
    -- Labor cost
    hourly_rate         NUMERIC(8,2),
    total_hours         NUMERIC(5,2),
    estimated_cost      NUMERIC(10,2),
    
    status              VARCHAR(20) NOT NULL DEFAULT 'scheduled'
                            CHECK (status IN ('scheduled','confirmed','declined','swapped','no_show','completed')),
    
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE shift_swaps (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID        NOT NULL REFERENCES tenants(id),
    original_shift_id   UUID        NOT NULL REFERENCES shifts(id),
    requesting_user_id  UUID        NOT NULL REFERENCES users(id),
    target_user_id      UUID        REFERENCES users(id),
    status              VARCHAR(20) NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','approved','rejected','cancelled')),
    reason              TEXT,
    approved_by         UUID        REFERENCES users(id),
    approved_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────────────
-- MESSAGING
-- ─────────────────────────────────────────────────
CREATE TABLE channels (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES tenants(id),
    location_id     UUID        REFERENCES locations(id),
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    type            VARCHAR(20) NOT NULL DEFAULT 'public'
                        CHECK (type IN ('public','private','direct','announcement','role_based')),
    role_id         UUID        REFERENCES roles(id),
    is_archived     BOOLEAN     NOT NULL DEFAULT FALSE,
    created_by      UUID        REFERENCES users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, name)
);

CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES tenants(id),
    channel_id      UUID        NOT NULL REFERENCES channels(id),
    sender_id       UUID        NOT NULL REFERENCES users(id),
    
    content         TEXT,
    type            VARCHAR(20) NOT NULL DEFAULT 'text'
                        CHECK (type IN ('text','image','file','voice','system','announcement')),
    
    file_url        VARCHAR(1024),
    file_type       VARCHAR(50),
    file_size_bytes INTEGER,
    voice_duration_seconds INTEGER,
    
    reply_to_id     UUID        REFERENCES messages(id),
    is_edited       BOOLEAN     NOT NULL DEFAULT FALSE,
    edited_at       TIMESTAMPTZ,
    is_deleted      BOOLEAN     NOT NULL DEFAULT FALSE,
    deleted_at      TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE message_reads (
    user_id         UUID NOT NULL REFERENCES users(id),
    channel_id      UUID NOT NULL REFERENCES channels(id),
    last_read_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, channel_id)
);

-- ─────────────────────────────────────────────────
-- SOP LIBRARY
-- ─────────────────────────────────────────────────
CREATE TABLE sop_documents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES tenants(id),
    location_id     UUID        REFERENCES locations(id),
    
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    category        VARCHAR(100),
    role_ids        UUID[],      -- Which roles this applies to
    
    current_version INTEGER     NOT NULL DEFAULT 1,
    status          VARCHAR(20) NOT NULL DEFAULT 'draft'
                        CHECK (status IN ('draft','published','archived')),
    
    content_url     VARCHAR(1024),
    video_url       VARCHAR(1024),
    
    requires_acknowledgment BOOLEAN NOT NULL DEFAULT FALSE,
    acknowledgment_due_days INTEGER,
    
    created_by      UUID        REFERENCES users(id),
    published_at    TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sop_versions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sop_id          UUID        NOT NULL REFERENCES sop_documents(id) ON DELETE CASCADE,
    version         INTEGER     NOT NULL,
    content_url     VARCHAR(1024),
    change_notes    TEXT,
    created_by      UUID        REFERENCES users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (sop_id, version)
);

CREATE TABLE sop_acknowledgments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES tenants(id),
    sop_id          UUID        NOT NULL REFERENCES sop_documents(id),
    user_id         UUID        NOT NULL REFERENCES users(id),
    version         INTEGER     NOT NULL,
    acknowledged_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip_address      INET,
    UNIQUE (user_id, sop_id, version)
);

-- ─────────────────────────────────────────────────
-- ANALYTICS EVENTS (TimescaleDB)
-- ─────────────────────────────────────────────────
CREATE TABLE analytics_events (
    time            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tenant_id       UUID        NOT NULL,
    location_id     UUID,
    user_id         UUID,
    event_type      VARCHAR(100) NOT NULL,
    event_category  VARCHAR(50)  NOT NULL,
    properties      JSONB        NOT NULL DEFAULT '{}',
    session_id      VARCHAR(100)
);

-- Convert to hypertable (TimescaleDB)
SELECT create_hypertable('analytics_events', 'time');
CREATE INDEX idx_analytics_tenant_time ON analytics_events(tenant_id, time DESC);

-- ─────────────────────────────────────────────────
-- AUDIT LOGS
-- ─────────────────────────────────────────────────
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES tenants(id),
    user_id         UUID        REFERENCES users(id),
    
    action          VARCHAR(100) NOT NULL,
    resource_type   VARCHAR(50)  NOT NULL,
    resource_id     VARCHAR(100),
    
    changes         JSONB,
    ip_address      INET,
    user_agent      TEXT,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_tenant_time ON audit_logs(tenant_id, created_at DESC);
```

---

## 4. Component Map

### 4.1 Frontend Component Tree

```
src/
├── app/                                    ← Next.js App Router
│   ├── (auth)/
│   │   ├── login/
│   │   ├── signup/
│   │   ├── forgot-password/
│   │   └── accept-invite/
│   ├── (dashboard)/
│   │   ├── layout.tsx                      ← Shell: Sidebar + TopBar + Notifications
│   │   ├── page.tsx                        ← Dashboard home (role-based)
│   │   ├── handoffs/
│   │   ├── tasks/
│   │   ├── incidents/
│   │   ├── schedule/
│   │   ├── messages/
│   │   ├── sop/
│   │   ├── analytics/
│   │   └── settings/
│   ├── (admin)/
│   │   ├── billing/
│   │   ├── team/
│   │   ├── locations/
│   │   └── contracts/
│   └── api/                                ← Next.js API routes (webhook proxies only)

├── components/
│   ├── ui/                                 ← shadcn/ui base components
│   │   ├── Button, Input, Select, Badge
│   │   ├── Dialog, Sheet, Drawer
│   │   ├── Card, Table, DataGrid
│   │   ├── Tabs, Accordion, Popover
│   │   ├── Toast, Alert, Skeleton
│   │   └── Avatar, Badge, Tooltip
│   │
│   ├── layout/
│   │   ├── Sidebar.tsx                     ← Role-aware navigation
│   │   ├── TopBar.tsx                      ← Search + Notifications + Avatar
│   │   ├── MobileNav.tsx                   ← Bottom tab bar (mobile)
│   │   ├── LocationSwitcher.tsx            ← Multi-location dropdown
│   │   └── CommandPalette.tsx              ← Global search (⌘K)
│   │
│   ├── auth/
│   │   ├── LoginForm.tsx                   ← Auth0 login flow
│   │   ├── InviteAcceptForm.tsx
│   │   ├── MFASetup.tsx
│   │   └── ProtectedRoute.tsx
│   │
│   ├── handoffs/
│   │   ├── HandoffCard.tsx                 ← Summary card with priority indicator
│   │   ├── HandoffForm.tsx                 ← Multi-step shift report form
│   │   ├── HandoffTimeline.tsx             ← Chronological history
│   │   ├── HandoffDetail.tsx               ← Full view with items + attachments
│   │   ├── HandoffAttachmentUploader.tsx   ← Photo/file upload with preview
│   │   ├── HandoffTemplateSelector.tsx
│   │   └── HandoffSearchFilter.tsx
│   │
│   ├── tasks/
│   │   ├── TaskKanban.tsx                  ← Drag-and-drop board (dnd-kit)
│   │   ├── TaskList.tsx                    ← Table/list view
│   │   ├── TaskCard.tsx                    ← Kanban card with priority + assignee
│   │   ├── TaskCreateModal.tsx
│   │   ├── TaskDetail.tsx                  ← Full task with comments + history
│   │   ├── TaskRecurrenceForm.tsx          ← RRULE builder UI
│   │   ├── TaskEscalationBadge.tsx
│   │   ├── TaskApprovalWorkflow.tsx
│   │   └── TaskFilters.tsx
│   │
│   ├── incidents/
│   │   ├── IncidentFeed.tsx                ← Real-time incident list
│   │   ├── IncidentCard.tsx
│   │   ├── IncidentReportForm.tsx          ← Photo + text report
│   │   ├── IncidentDetail.tsx
│   │   ├── IncidentQRScanner.tsx           ← Camera QR code reader
│   │   ├── IncidentEscalationTimer.tsx     ← Countdown to escalation
│   │   ├── IncidentStatusPipeline.tsx      ← Visual status pipeline
│   │   └── IncidentFilters.tsx
│   │
│   ├── schedule/
│   │   ├── WeeklyCalendar.tsx              ← Drag-and-drop schedule grid
│   │   ├── ShiftBlock.tsx                  ← Individual shift card on grid
│   │   ├── ShiftForm.tsx
│   │   ├── ShiftSwapRequest.tsx
│   │   ├── AvailabilityForm.tsx
│   │   ├── OverTimeAlert.tsx
│   │   ├── LaborCostSidebar.tsx            ← Live labor cost as you schedule
│   │   └── PayrollExportButton.tsx
│   │
│   ├── messages/
│   │   ├── ChannelList.tsx
│   │   ├── MessageThread.tsx               ← Virtualized message list
│   │   ├── MessageInput.tsx                ← Text + file + voice note
│   │   ├── VoiceNoteRecorder.tsx
│   │   ├── MessageReadReceipts.tsx
│   │   ├── BroadcastComposer.tsx           ← Manager-only broadcast
│   │   └── DirectMessageModal.tsx
│   │
│   ├── sop/
│   │   ├── SOPLibrary.tsx                  ← Role-filtered document list
│   │   ├── SOPDocument.tsx                 ← Reader with video embed
│   │   ├── SOPAcknowledgmentPrompt.tsx
│   │   ├── SOPVersionHistory.tsx
│   │   ├── SOPUploadForm.tsx
│   │   └── SOPComplianceReport.tsx
│   │
│   ├── analytics/
│   │   ├── AnalyticsDashboard.tsx          ← Overview with KPI cards
│   │   ├── TaskCompletionChart.tsx         ← Recharts bar chart
│   │   ├── IncidentHeatmap.tsx
│   │   ├── LaborEfficiencyChart.tsx
│   │   ├── LocationComparisonTable.tsx
│   │   ├── ResponseTimeMetrics.tsx
│   │   ├── ForecastingCard.tsx             ← AI staffing forecast (existing)
│   │   └── ExportReportButton.tsx
│   │
│   ├── billing/
│   │   ├── PricingTable.tsx                ← Public pricing page
│   │   ├── SubscriptionCard.tsx            ← Current plan + usage
│   │   ├── UpgradeModal.tsx
│   │   ├── InvoiceList.tsx
│   │   ├── InvoiceDetail.tsx
│   │   ├── ContractSummary.tsx             ← Enterprise contract view
│   │   ├── SeatManager.tsx                 ← Add/remove seats
│   │   ├── LocationBillingBreakdown.tsx
│   │   └── PaymentMethodForm.tsx           ← Stripe Elements
│   │
│   ├── onboarding/
│   │   ├── OnboardingWizard.tsx            ← Multi-step new tenant setup
│   │   ├── LocationSetupStep.tsx
│   │   ├── TeamInviteStep.tsx
│   │   ├── RoleSetupStep.tsx
│   │   └── PlanSelectionStep.tsx
│   │
│   └── shared/
│       ├── EmptyState.tsx
│       ├── LoadingSpinner.tsx
│       ├── ErrorBoundary.tsx
│       ├── OfflineBanner.tsx               ← PWA offline indicator
│       ├── NotificationCenter.tsx          ← Bell dropdown
│       ├── RichTextEditor.tsx              ← TipTap editor
│       ├── FileUploader.tsx
│       └── QRCodeGenerator.tsx            ← For incident report QR

├── hooks/
│   ├── useAuth.ts
│   ├── useTenant.ts
│   ├── useLocation.ts
│   ├── usePermissions.ts
│   ├── useRealtime.ts                      ← WebSocket subscription
│   ├── useOfflineSync.ts                   ← PWA background sync
│   ├── useTierGate.ts                      ← Feature flag check
│   └── useAnalyticsTrack.ts

├── store/                                  ← Redux Toolkit
│   ├── index.ts
│   ├── slices/
│   │   ├── authSlice.ts
│   │   ├── tenantSlice.ts
│   │   ├── notificationsSlice.ts
│   │   └── realtimeSlice.ts
│   └── api/                                ← RTK Query endpoints
│       ├── authApi.ts
│       ├── handoffsApi.ts
│       ├── tasksApi.ts
│       ├── incidentsApi.ts
│       ├── scheduleApi.ts
│       ├── messagesApi.ts
│       ├── sopApi.ts
│       ├── analyticsApi.ts
│       └── billingApi.ts

└── lib/
    ├── auth0.ts
    ├── stripe.ts
    ├── api-client.ts                       ← Axios with JWT interceptor
    ├── websocket.ts
    ├── permissions.ts
    └── formatters.ts
```

---

## 5. Page Map

### 5.1 Public Pages (No Auth Required)

| Route | Page | Description |
|-------|------|-------------|
| `/` | Landing Page | Hero, features, social proof, pricing preview |
| `/pricing` | Pricing Page | Full interactive pricing table with tier comparison |
| `/features` | Features Page | Detailed feature breakdown per module |
| `/industries` | Industries Page | Hospitality verticals (hotels, restaurants, venues) |
| `/enterprise` | Enterprise Page | Contract terms, SLA, security, SSO, custom |
| `/login` | Login | Auth0 Universal Login redirect |
| `/signup` | Signup | Plan selection → Auth0 signup → onboarding |
| `/accept-invite/:token` | Accept Invite | Team member joining via invite link |
| `/demo` | Request Demo | Lead capture form for enterprise prospects |
| `/qr/:qr_code_id` | QR Incident Report | Public QR landing → guest/staff issue report |
| `/docs` | API Docs | Swagger/Redoc embed for API-tier tenants |

### 5.2 Onboarding Flow (Post-Signup)

| Route | Page | Step |
|-------|------|------|
| `/onboarding/plan` | Plan Selection | Choose Free / Team / Pro / Enterprise |
| `/onboarding/organization` | Org Setup | Name, slug, industry, timezone |
| `/onboarding/location` | First Location | Name, address, timezone |
| `/onboarding/team` | Team Invite | Email invites with role assignment |
| `/onboarding/roles` | Role Config | Confirm or customize default roles |
| `/onboarding/complete` | Launch | Welcome screen → Dashboard |

### 5.3 Dashboard Pages (Auth Required)

#### Shared / All Roles

| Route | Page |
|-------|------|
| `/dashboard` | Role-based home dashboard |
| `/dashboard/notifications` | Notification center |
| `/dashboard/profile` | User profile + notification preferences |

#### Handoffs Module

| Route | Page |
|-------|------|
| `/dashboard/handoffs` | Handoff feed — list of shift reports |
| `/dashboard/handoffs/new` | Create shift handoff report |
| `/dashboard/handoffs/:id` | View / acknowledge handoff |
| `/dashboard/handoffs/search` | Search + filter history |

#### Tasks Module

| Route | Page |
|-------|------|
| `/dashboard/tasks` | Task board (Kanban default + List toggle) |
| `/dashboard/tasks/new` | Create task (+ recurrence builder) |
| `/dashboard/tasks/:id` | Task detail + comments + audit trail |
| `/dashboard/tasks/my-tasks` | Filtered: assigned to current user |
| `/dashboard/tasks/overdue` | Escalation-priority queue |

#### Incidents Module

| Route | Page |
|-------|------|
| `/dashboard/incidents` | Incident feed + severity filter |
| `/dashboard/incidents/new` | Report incident (photo + text) |
| `/dashboard/incidents/:id` | Incident detail + timeline + comments |
| `/dashboard/incidents/map` | Heatmap by area/location |

#### Schedule Module

| Route | Page |
|-------|------|
| `/dashboard/schedule` | Weekly schedule calendar |
| `/dashboard/schedule/my-shifts` | Personal shift view |
| `/dashboard/schedule/swaps` | Pending swap requests |
| `/dashboard/schedule/availability` | Submit availability |
| `/dashboard/schedule/labor-cost` | Labor cost report |
| `/dashboard/schedule/export` | Payroll-ready export |

#### Messages Module

| Route | Page |
|-------|------|
| `/dashboard/messages` | Channel list |
| `/dashboard/messages/:channel_id` | Message thread |
| `/dashboard/messages/direct/:user_id` | Direct message |
| `/dashboard/messages/announcements` | Broadcast-only feed |

#### SOP Hub

| Route | Page |
|-------|------|
| `/dashboard/sop` | SOP library (role-filtered) |
| `/dashboard/sop/:id` | Document reader + video |
| `/dashboard/sop/:id/acknowledge` | Acknowledgment confirmation |
| `/dashboard/sop/compliance` | Manager compliance report |

#### Analytics

| Route | Page |
|-------|------|
| `/dashboard/analytics` | KPI overview |
| `/dashboard/analytics/tasks` | Task completion metrics |
| `/dashboard/analytics/incidents` | Incident frequency + response time |
| `/dashboard/analytics/labor` | Labor efficiency + cost |
| `/dashboard/analytics/locations` | Multi-location comparison |
| `/dashboard/analytics/forecasting` | AI staffing forecast |
| `/dashboard/analytics/export` | Report export center |

### 5.4 Admin Pages (Owner / Admin Roles)

| Route | Page |
|-------|------|
| `/admin/team` | User management + invites |
| `/admin/roles` | Role editor + permissions matrix |
| `/admin/locations` | Location management |
| `/admin/locations/:id/settings` | Per-location config |
| `/admin/billing` | Subscription + plan |
| `/admin/billing/invoices` | Invoice history |
| `/admin/billing/invoices/:id` | Invoice detail + PDF |
| `/admin/billing/seats` | Seat management + cost estimate |
| `/admin/billing/contract` | Contract details + term |
| `/admin/billing/upgrade` | Plan upgrade flow |
| `/admin/settings` | Org settings: branding, timezone, SSO |
| `/admin/settings/sso` | SAML/OIDC SSO config (Enterprise) |
| `/admin/settings/api` | API key management (Enterprise) |
| `/admin/settings/webhooks` | Webhook config (Enterprise) |
| `/admin/audit-log` | Full audit trail with export |

### 5.5 Super Admin Pages (RelayPoint Internal)

| Route | Page |
|-------|------|
| `/superadmin/tenants` | All tenant management |
| `/superadmin/tenants/:id` | Tenant detail + impersonate |
| `/superadmin/billing` | All subscriptions + MRR dashboard |
| `/superadmin/contracts` | Enterprise contract management |
| `/superadmin/plans` | Plan editor + Stripe sync |
| `/superadmin/impersonate` | Tenant impersonation tool |
| `/superadmin/feature-flags` | Global feature flag editor |
| `/superadmin/metrics` | Platform health dashboard |

---

## 6. Pricing Table

### 6.1 Tier Overview

| | **Free** | **Team** | **Pro** | **Enterprise** |
|--|----------|----------|---------|---------------|
| **Target** | Solo operators, trial | Small teams ≤15 staff | Mid-size operations | Multi-location groups |
| **Monthly (per seat)** | $0 | $12 | $22 | Custom |
| **Annual (per seat/mo)** | — | $10 | $18 | Custom |
| **Included Seats** | 5 | 5 + overage | 5 + overage | Negotiated |
| **Locations** | 1 | 1 | Up to 3 | Unlimited |
| **Storage** | 1 GB | 10 GB | 50 GB | 500 GB+ |

### 6.2 Full Monthly Pricing

#### Free Tier — $0/mo

- 5 seats maximum (hard cap)
- 1 location
- Shift handoffs (25/month limit)
- Tasks (50 active limit)
- 1 GB storage
- No SLA
- Community support only
- RelayPoint branding visible

#### Team Tier — Base $29/mo + $12/seat/mo

- Everything in Free, unlimited
- Full task automation engine
- Drag-and-drop scheduling
- Shift swaps + availability
- Real-time messaging (channels + DMs)
- Basic analytics dashboard
- Read receipts + file uploads
- Mobile apps (iOS + Android)
- Email + push notifications
- 10 GB storage
- Overage seats: $12/seat/mo
- Email support (48h SLA)

#### Pro Tier — Base $79/mo + $22/seat/mo

- Everything in Team
- Incident & maintenance management
- QR code incident reporting
- SOP & compliance hub
- Advanced analytics + response time metrics
- Manager approval workflows
- Voice notes in messaging
- Payroll-ready export
- AI staffing forecasting
- SMS alerts
- Up to 3 locations (additional: $39/location/mo)
- 50 GB storage
- Audit logs (90 days)
- Overage seats: $22/seat/mo
- Priority email support (12h SLA)

#### Enterprise Tier — Custom Pricing (minimum $499/mo)

- Everything in Pro
- Unlimited locations
- Multi-location dashboard + comparison
- Custom automation rules
- REST API access + webhook management
- SSO (SAML/OIDC)
- White-label branding
- Audit logs (unlimited)
- 500 GB+ storage (expandable)
- Custom SOP templates
- Dedicated customer success manager
- SLA 99.9% uptime guarantee
- Phone + Slack support channel
- Onboarding + training package
- Custom contract terms (see Section 7)
- Up to 5-year contract term

### 6.3 Annual & Multi-Year Discount Schedule

#### Standard (Team + Pro)

| Billing Cycle | Discount | Effective Per-Seat Multiplier |
|---------------|----------|-------------------------------|
| Monthly | 0% | 1.00x |
| Annual (12 mo) | 17% | 0.83x |

#### Enterprise Contract Terms

| Term | Discount Off Monthly Rate | Lock-In Incentive |
|------|--------------------------|-------------------|
| Monthly | 0% | None |
| Annual (12 mo) | 15% | Standard SLA |
| 2-Year (24 mo) | 22% | Priority onboarding |
| 3-Year (36 mo) | 28% | Dedicated CSM included |
| 5-Year (60 mo) | 35% | Locked rate + free seats |

**Example Enterprise calculation (3-year, 50 seats, 5 locations):**

```
Base rate:              $499/mo flat
Seats (50):             50 × $18/seat/mo = $900/mo  (using annual equiv.)
Locations (5):          5 × $39/location/mo = $195/mo  (pro equiv.)
Monthly subtotal:       $1,594/mo

3-Year discount (28%):  $1,594 × 0.72 = $1,148/mo
Annual contract value:  $1,148 × 12 = $13,773/yr
Total contract value:   $1,148 × 36 = $41,318 over 3 years
```

### 6.4 Volume Pricing Thresholds

| Seats | Additional Discount |
|-------|-------------------|
| 1–24 seats | 0% |
| 25–49 seats | 5% additional |
| 50–99 seats | 10% additional |
| 100–199 seats | 15% additional |
| 200+ seats | 20% additional (custom negotiation) |

| Locations | Additional Discount |
|-----------|-------------------|
| 1–4 locations | Base rate |
| 5–9 locations | 10% off location add-on |
| 10–24 locations | 20% off location add-on |
| 25+ locations | Flat negotiated rate |

---

## 7. Billing Logic Breakdown

### 7.1 Stripe Architecture

```
Stripe Customer
  └── Payment Methods (default + backup)
  └── Subscriptions
        ├── Plan Item (base price)
        ├── Seat Item (quantity = seat_count, metered or licensed)
        └── Location Item (quantity = location_count)
  └── Invoices (auto-generated)
  └── Invoice Items (prorations, one-time charges)
```

**Stripe Products & Prices:**

| Product | Price ID Pattern | Type |
|---------|-----------------|------|
| RelayPoint Team (Base) | `price_team_base_monthly` | Recurring fixed |
| RelayPoint Team (Seat) | `price_team_seat_monthly` | Per-unit licensed |
| RelayPoint Pro (Base) | `price_pro_base_monthly` | Recurring fixed |
| RelayPoint Pro (Seat) | `price_pro_seat_monthly` | Per-unit licensed |
| RelayPoint Pro (Location) | `price_pro_location_monthly` | Per-unit licensed |
| Enterprise (Custom) | Created via Stripe API per deal | Custom |

### 7.2 Subscription Lifecycle

```
TRIAL (14 days)
  │
  ▼
TRIALING → stripe.subscription.status = 'trialing'
  │         Card collection deferred (trial_end webhook triggers)
  │
  ▼
ACTIVE → stripe.subscription.status = 'active'
  │       Invoice auto-generated each billing cycle
  │       Webhooks: invoice.paid, invoice.payment_succeeded
  │
  ├──── UPGRADE → Immediate proration; new higher tier activates instantly
  │               stripe.subscription.update() with proration_behavior='create_prorations'
  │
  ├──── DOWNGRADE → At period end; tier gates enforced immediately
  │                  cancel_at_period_end behavior on removed items
  │
  ├──── SEAT ADD → Prorated immediately to current period end
  │
  ├──── SEAT REMOVE → At period end (to avoid usage abuse)
  │
  └──── CANCEL → cancel_at_period_end = true (access until period end)

PAST_DUE → Payment failed; retry logic initiated
  │         Grace period: 7 days
  │         Email dunning sequence triggered
  │
  ▼
UNPAID → Full feature lock after 7 days past_due
  │       Data retained 30 days before scheduled deletion
  │
  ▼
CANCELED → Access revoked; data in retention window
```

### 7.3 Proration Logic

```python
# Upgrade proration
def calculate_upgrade_proration(
    current_plan_price: Decimal,
    new_plan_price: Decimal,
    days_remaining: int,
    days_in_period: int
) -> Decimal:
    daily_current = current_plan_price / days_in_period
    daily_new = new_plan_price / days_in_period
    credit = daily_current * days_remaining      # Refund unused
    charge = daily_new * days_remaining          # Charge new plan
    return charge - credit  # Net proration charge

# Seat proration (immediate)
def calculate_seat_addition_proration(
    price_per_seat: Decimal,
    seats_added: int,
    days_remaining: int,
    days_in_period: int
) -> Decimal:
    daily_rate = price_per_seat / days_in_period
    return daily_rate * days_remaining * seats_added
```

All proration is handled via Stripe's native proration engine. RelayPoint stores the `proration_date` and reconciles against Stripe invoice line items.

### 7.4 Dunning Management

```
Day 0:   Payment failed → Stripe retries immediately
Day 1:   Email: "We couldn't process your payment — please update your card"
Day 3:   Email: "Reminder — your account is past due"
         Stripe auto-retry
Day 5:   Email: "Urgent — account features will be suspended in 48 hours"
         SMS alert (if phone on file)
Day 7:   SUSPENSION — Feature access locked
         Email: "Your account has been suspended"
Day 14:  Email: "Final notice — account will be deleted in 16 days"
Day 30:  CANCELLATION — Data deletion scheduled (30-day retention window)
Day 60:  DATA DELETION — Tenant data permanently removed
```

Dunning is implemented via **Celery Beat** scheduled tasks polling Stripe webhook events + invoice state.

### 7.5 Seat Billing Logic

```python
# Seat types and billing weights
SEAT_BILLING_WEIGHTS = {
    "full":     Decimal("1.00"),   # Counts as 1 full seat
    "manager":  Decimal("1.00"),   # Manager = 1 full seat
    "limited":  Decimal("0.50"),   # Limited = 0.5 seat (half price)
    "viewer":   Decimal("0.25"),   # Viewer = 0.25 seat (read-only)
}

def calculate_billable_seats(users: List[User]) -> Decimal:
    return sum(
        SEAT_BILLING_WEIGHTS.get(u.seat_type, Decimal("1.00"))
        for u in users if u.status == "active"
    )
```

### 7.6 Tax Handling

- Tax collection delegated to **Stripe Tax** (automatic tax calculation)
- Tax behavior: `inclusive` for B2C, `exclusive` for B2B
- Tax IDs collected for EU VAT reverse charge
- US nexus states computed via Stripe Tax engine

### 7.7 Invoice Generation

Invoices are generated automatically by Stripe at period end. RelayPoint:
1. Listens to `invoice.finalized` webhook
2. Stores invoice in local `invoices` table
3. Generates branded PDF via **Stripe's hosted invoice** or custom PDF renderer
4. Emails invoice PDF to billing contact
5. For Enterprise contracts: includes itemized breakdown of seats + locations

---

## 8. Contract Logic Model

### 8.1 Contract Term Engine

```python
from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta

TERM_DISCOUNT_MAP = {
    1:   Decimal("0.00"),   # Monthly — no discount
    12:  Decimal("0.15"),   # Annual — 15% off
    24:  Decimal("0.22"),   # 2-Year — 22% off
    36:  Decimal("0.28"),   # 3-Year — 28% off
    60:  Decimal("0.35"),   # 5-Year — 35% off (maximum term)
}

VOLUME_SEAT_DISCOUNTS = {
    (0, 24):   Decimal("0.00"),
    (25, 49):  Decimal("0.05"),
    (50, 99):  Decimal("0.10"),
    (100, 199):Decimal("0.15"),
    (200, None):Decimal("0.20"),
}

VOLUME_LOCATION_DISCOUNTS = {
    (1, 4):    Decimal("0.00"),
    (5, 9):    Decimal("0.10"),
    (10, 24):  Decimal("0.20"),
    (25, None):Decimal("0.30"),
}

def compute_volume_discount(seats: int, thresholds: dict) -> Decimal:
    for (low, high), discount in thresholds.items():
        if high is None and seats >= low:
            return discount
        elif low <= seats <= high:
            return discount
    return Decimal("0.00")

def calculate_contract_pricing(
    base_monthly:        Decimal,
    seat_price_monthly:  Decimal,
    location_price_monthly: Decimal,
    seat_count:          int,
    location_count:      int,
    term_months:         int,
) -> dict:
    term_discount    = TERM_DISCOUNT_MAP.get(term_months, Decimal("0.00"))
    seat_vol_disc    = compute_volume_discount(seat_count, VOLUME_SEAT_DISCOUNTS)
    loc_vol_disc     = compute_volume_discount(location_count, VOLUME_LOCATION_DISCOUNTS)

    # Apply discounts to components
    effective_base   = base_monthly * (1 - term_discount)
    effective_seat   = seat_price_monthly * seat_count * (1 - term_discount) * (1 - seat_vol_disc)
    effective_loc    = location_price_monthly * location_count * (1 - term_discount) * (1 - loc_vol_disc)

    monthly_total    = effective_base + effective_seat + effective_loc
    annual_value     = monthly_total * 12
    tcv              = monthly_total * term_months

    return {
        "monthly_rate":          monthly_total.quantize(Decimal("0.01")),
        "annual_contract_value": annual_value.quantize(Decimal("0.01")),
        "total_contract_value":  tcv.quantize(Decimal("0.01")),
        "term_months":           term_months,
        "term_discount_pct":     float(term_discount * 100),
        "seat_volume_discount":  float(seat_vol_disc * 100),
        "location_volume_discount": float(loc_vol_disc * 100),
        "start_date":            date.today().isoformat(),
        "end_date":              (date.today() + relativedelta(months=term_months)).isoformat(),
    }
```

### 8.2 Early Termination Fee Logic

```python
def calculate_etf(
    contract: Contract,
    termination_date: date,
    etf_type: str = "remaining_balance_50pct"
) -> Decimal:
    end = contract.end_date.date()
    months_remaining = max(0,
        (end.year - termination_date.year) * 12
        + (end.month - termination_date.month)
    )
    remaining_value = contract.monthly_effective_rate * months_remaining

    match etf_type:
        case "remaining_balance_100pct":
            return remaining_value
        case "remaining_balance_50pct":
            return (remaining_value * Decimal("0.50")).quantize(Decimal("0.01"))
        case "flat_fee":
            return contract.early_termination_fee_flat
        case "none":
            return Decimal("0.00")
```

- **Monthly contracts:** No ETF — cancels at period end
- **Annual contracts:** 50% of remaining balance
- **2-Year contracts:** 50% of remaining balance
- **3-Year contracts:** 50% of remaining balance
- **5-Year contracts:** Negotiated (typically 50% remaining, minimum 3 months)
- Enterprise contracts may include custom ETF terms in signed agreement

### 8.3 Contract Renewal Automation

```
T-90 days:  Renewal notification email to billing contact + owner
            "Your contract expires in 90 days — here are your renewal options"
            
T-60 days:  CSM outreach triggered (Enterprise tier)
            Renewal quote generated at locked rate (if renewal_locked_rate = TRUE)
            
T-30 days:  Second notification with urgency
            If no response: auto-renew flagged for processing
            
T-7 days:   Final notification
            
T-0:        
  if auto_renew = TRUE:
    → Generate new contract with same or updated terms
    → Stripe subscription updated with new period
    → New contract record created (status: active)
    → Invoice generated for first period
    
  if auto_renew = FALSE:
    → Subscription reverts to month-to-month at current monthly rate
    → No ETF applies at this point
    → User notified of rate change (monthly > annual equivalent)
```

### 8.4 Contract Record State Machine

```
DRAFT → PENDING → ACTIVE → EXPIRED  →  (RENEWED | LAPSED)
                         ↘ TERMINATED   (ETF triggered)
```

All state transitions are logged in `audit_logs` with user ID and timestamp.

---

## 9. Deployment Roadmap

### Phase 1: Foundation (Weeks 1–4)

**Infrastructure**
- [ ] Provision AWS RDS PostgreSQL 15 (Multi-AZ)
- [ ] Provision ElastiCache Redis 7 cluster
- [ ] Create S3 buckets: `relaypoint-uploads-prod`, `relaypoint-backups`
- [ ] Configure Cloudflare domain + WAF rules
- [ ] Set up GitHub Actions CI/CD pipeline
- [ ] Build and push Docker images to ECR

**Backend**
- [ ] Apply TimescaleDB extension to `analytics_events`
- [ ] Run all Alembic migrations (schema + RLS policies)
- [ ] Configure PgBouncer for connection pooling
- [ ] Deploy FastAPI to ECS Fargate (2 tasks, auto-scale)
- [ ] Deploy Celery workers (2 tasks) + Celery Beat (1 task)
- [ ] Configure Redis Pub/Sub for WebSocket fan-out
- [ ] Integrate Auth0 tenant (production)
- [ ] Integrate Stripe (live mode keys)
- [ ] Verify SendGrid + Twilio transactional credentials

**Frontend**
- [ ] Configure `next.config.js` for static export (`output: 'export'`)
- [ ] Set up GitHub Pages deployment workflow (`.github/workflows/deploy.yml`)
- [ ] Configure CDN rewrites for SPA routing
- [ ] Validate PWA manifest + service worker
- [ ] End-to-end Auth0 login flow test

**Milestone:** Core auth + task creation working in production

---

### Phase 2: Core Features (Weeks 5–10)

- [ ] Shift Handoff module (create, acknowledge, attach photos)
- [ ] Task Engine (create, assign, recurrence, escalation, approval)
- [ ] Incident reporting (form, photo upload, QR code generation)
- [ ] Real-time messaging (channels, DMs, read receipts)
- [ ] Weekly scheduling (drag-and-drop, publish, swap requests)
- [ ] Push notification integration (FCM)
- [ ] Email notification templates (SendGrid dynamic templates)
- [ ] Multi-location selector + location-scoped data

**Milestone:** Full operational feature set live

---

### Phase 3: Billing & Subscriptions (Weeks 11–14)

- [ ] Stripe Products + Prices creation (all tiers)
- [ ] Subscription creation flow (signup → Stripe customer → plan)
- [ ] Trial management (14-day trial, card capture at T-0)
- [ ] Webhook handler for 15+ Stripe events
- [ ] Upgrade/downgrade proration logic
- [ ] Seat management UI + billable seat calculation
- [ ] Invoice generation + PDF + email delivery
- [ ] Dunning email sequence (SendGrid drip)
- [ ] Admin billing dashboard (MRR, churn, ARR)
- [ ] Feature tier gating enforcement across all API endpoints

**Milestone:** Full self-serve billing live

---

### Phase 4: Enterprise & Analytics (Weeks 15–20)

- [ ] SOP Hub (upload, version, publish, acknowledge)
- [ ] Advanced analytics dashboard (Recharts, multi-location)
- [ ] AI staffing forecasting (existing LightGBM model) production-ready
- [ ] Contract management system (create, sign, auto-renew)
- [ ] Enterprise contract pricing engine
- [ ] ETF calculation API
- [ ] SSO configuration page (SAML/OIDC via Auth0 Actions)
- [ ] API key management (JWT-scoped, per-tenant)
- [ ] Audit log viewer + CSV export
- [ ] Payroll export (CSV + ADP-compatible format)
- [ ] Multi-location comparison analytics

**Milestone:** Enterprise tier feature-complete

---

### Phase 5: Production Hardening (Weeks 21–24)

- [ ] Penetration testing (OWASP Top 10 audit)
- [ ] Load testing (k6: 10,000 concurrent users)
- [ ] SOC 2 Type I evidence collection
- [ ] Backup verification (daily RDS snapshots, 30-day retention)
- [ ] Disaster recovery runbook + failover test
- [ ] Rate limiting tuning per tier
- [ ] CDN cache warming + performance audit (<3s LCP)
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Mobile app submission to App Store + Google Play
- [ ] Runbook documentation for on-call team

**Milestone:** Production launch — GA ready

---

### GitHub Actions CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: RelayPoint Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/app/tests/ --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v4

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci
      - run: cd frontend && npm test -- --watchAll=false
      - run: cd frontend && npm run build

  deploy-frontend:
    needs: [test-frontend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/out

  deploy-backend:
    needs: [test-backend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/amazon-ecr-login@v2
      - run: |
          docker build -t relaypoint-backend ./backend
          docker tag relaypoint-backend:latest $ECR_REGISTRY/relaypoint-backend:$GITHUB_SHA
          docker push $ECR_REGISTRY/relaypoint-backend:$GITHUB_SHA
      - run: |
          aws ecs update-service \
            --cluster relaypoint-prod \
            --service relaypoint-api \
            --force-new-deployment
```

---

## 10. Scaling Roadmap

### 10.1 Current Architecture Limits (Single Region)

| Component | Current Config | Estimated Capacity |
|-----------|---------------|-------------------|
| FastAPI (ECS Fargate) | 2 tasks × 2 vCPU / 4GB | ~500 req/sec |
| PostgreSQL (RDS r6g.large) | 2 vCPU, 16 GB, Multi-AZ | ~5,000 tenants |
| Redis (ElastiCache r6g.large) | 13 GB | ~100K concurrent WS |
| S3 Storage | Unlimited | Unlimited |
| CDN (Cloudflare) | Global edge | ~100K concurrent |

### 10.2 Horizontal Scaling Triggers

| Metric | Scale-Out Trigger | Action |
|--------|------------------|--------|
| API CPU > 70% | 3 minutes sustained | Add 2 ECS tasks |
| API latency p95 > 500ms | 5 minutes sustained | Add 2 ECS tasks |
| DB connections > 80% | Immediate | Add read replica |
| Redis memory > 75% | Immediate | Upgrade instance class |

### 10.3 Database Scaling Strategy

**Stage 1 (0–1,000 tenants): Single Primary**
- RDS PostgreSQL Multi-AZ (automatic failover)
- PgBouncer connection pooling (transaction mode)
- Read replicas for analytics queries

**Stage 2 (1,000–5,000 tenants): Read Scaling**
- Add 2x read replicas
- Direct analytics + reporting queries to read replicas
- TimescaleDB compression policies for `analytics_events` (compress segments > 7 days)
- Partition `audit_logs` by month

**Stage 3 (5,000–20,000 tenants): Shard by Tenant**
- Introduce tenant sharding: SHA hash of `tenant_id` → shard key
- Deploy 4–8 PostgreSQL shards via **Citus** (distributed PostgreSQL)
- Routing middleware in FastAPI: `ShardRouter` resolves connection pool by `tenant_id`

**Stage 4 (20,000+ tenants): Dedicated DB per Enterprise**
- Enterprise-tier tenants: dedicated RDS instance (schema isolation)
- Standard-tier tenants: remain on shared shard cluster
- Automated provisioning via Terraform module triggered by Enterprise contract creation

### 10.4 Kubernetes Migration Path

The existing `/helm/relaypoint/` charts support a migration from ECS to EKS:

```
ECS Fargate (Stage 1-2)       EKS + Karpenter (Stage 3+)
─────────────────────         ──────────────────────────
Easy managed scaling          Pod autoscaling (HPA + VPA)
No k8s ops overhead           Bin-packing, spot instances
Limited customization         Full observability stack
$0.04048/vCPU-hour            40–60% cost reduction via spot
```

**EKS deployment targets:**
- API pods: HPA on CPU + queue depth  
- Celery workers: KEDA autoscale on Redis queue length
- Celery Beat: Single replica with leader election
- WebSocket servers: Sticky sessions via NLB

### 10.5 Multi-Region Strategy

**Phase A: Active-Passive (Year 1)**
```
Primary:  us-east-1 (AWS)
DR:       us-west-2 (AWS)

RDS:      Cross-region read replica (30s RPO)
S3:       Cross-region replication
Route53:  Health-check failover records
```

**Phase B: Active-Active (Year 2+)**
```
Region 1: us-east-1 (North America)
Region 2: eu-west-1 (Europe — GDPR data residency)
Region 3: ap-southeast-1 (Asia-Pacific)

Each region:
  ├── EKS cluster (API + WebSocket + Celery)
  ├── RDS PostgreSQL primary
  ├── ElastiCache Redis
  └── CloudFront/Cloudflare edge

Routing: Cloudflare Geolocation → nearest region
Data residency: Tenant provisioned to GDPR-region if EU billing address
```

### 10.6 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Page Load (LCP) | < 2.5s | Core Web Vitals |
| API p50 latency | < 100ms | Datadog APM |
| API p95 latency | < 300ms | Datadog APM |
| API p99 latency | < 1,000ms | Datadog APM |
| WebSocket connect | < 500ms | Synthetic monitor |
| Uptime SLA (Team/Pro) | 99.5% | Status page |
| Uptime SLA (Enterprise) | 99.9% | Contractual SLA |
| RTO (Recovery Time) | < 30 min | DR runbook |
| RPO (Recovery Point) | < 5 min | Continuous WAL archiving |

### 10.7 Cost Optimization at Scale

| Strategy | Estimated Saving |
|----------|-----------------|
| Spot instances for Celery workers | 60–70% |
| Reserved instances for DB + Redis (1yr) | 30–40% |
| S3 Intelligent Tiering for old files | 40–60% on cold storage |
| TimescaleDB compression (analytics) | 90% storage reduction |
| Cloudflare R2 (no egress fees) vs S3 | 30% on transfer costs |
| Aurora Serverless v2 for dev/staging | $0 when idle |

---

## Appendix A: API Versioning Strategy

```
/api/v1/   ← Current stable (in production)
/api/v2/   ← Next version (GraphQL + WebSocket upgrades)
/api/internal/  ← Super-admin only (isolated auth)

Versioning rules:
- Breaking changes → bump major version
- Additive changes → no version bump
- Deprecated endpoints → 6-month sunset window
- ETag + conditional requests on all GET endpoints
- Cursor-based pagination on all list endpoints
```

## Appendix B: Security Architecture

| Layer | Control |
|-------|---------|
| Network | VPC private subnets, no public DB, Security Groups |
| API | Rate limiting (slowapi), WAF (Cloudflare), DDoS protection |
| Auth | Auth0 PKCE flow, RS256 JWT, JWKS rotation |
| Authorization | RBAC via `role.permissions` JSONB + RLS policies |
| Data | TLS 1.3 in transit; AES-256 at rest (RDS + S3) |
| Secrets | AWS Secrets Manager, no secrets in code/env files in prod |
| Audit | Immutable audit log; all mutations recorded |
| GDPR | Right-to-erasure endpoint; data export API; DPA available |
| SOC 2 | Evidence collection via Vanta; Type I in progress |
| PCI DSS | Card data never touches RelayPoint servers (Stripe.js only) |

## Appendix C: QR Code Incident Reporting Flow

```
1. Admin generates QR code for location area (e.g., "Room 214")
   → POST /api/v1/incidents/qr-codes
   → Returns QR PNG + unique qr_code_id

2. Print QR code and mount in area

3. Guest/staff scans QR code with any camera app
   → Redirects to: app.relaypoint.io/qr/{qr_code_id}
   → No login required for submission

4. Public form renders (incident title, description, photo)
   → Pre-populated: location, area from QR code metadata
   → Captcha validation (Cloudflare Turnstile)

5. Submission
   → POST /api/v1/incidents/public-report
   → Incident created with reported_via = 'qr_code'
   → Auto-assigned to maintenance role for that location
   → Escalation timer started (configurable per location)
   → Push + SMS to on-duty maintenance staff

6. Reporting user receives:
   → Confirmation reference number
   → Optional email receipt if provided
```

---

*Architecture document maintained by RelayPoint Engineering. Last updated: February 23, 2026.*
