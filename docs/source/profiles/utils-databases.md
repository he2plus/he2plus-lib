# Database Development Environment

## Overview

Complete database development environment with PostgreSQL, MySQL, MongoDB, Redis, Neo4j, and comprehensive database tools for development, administration, and monitoring.

## Profile ID
`utils-databases`

## Category
Utils

## System Requirements

- **RAM**: 8.0 GB
- **Disk Space**: 20.0 GB
- **CPU Cores**: 4
- **GPU**: Not required
- **Internet**: Required

## Components (32 total)

### Database Servers
- PostgreSQL 15.4
- MySQL 8.0.35
- MongoDB 7.0.5
- Redis 7.2.3
- Neo4j 5.15.0
- SQLite 3.44.2

### Administration Tools
- pgAdmin 8.2.0
- DBeaver 23.3.0
- MongoDB Compass 1.40.0
- RedisInsight 2.44.0
- Neo4j Browser 5.15.0

### Development Libraries
- SQLAlchemy 2.0.23 (Python ORM)
- psycopg2 2.9.9 (PostgreSQL Python driver)
- PyMongo 4.6.0 (MongoDB Python driver)
- redis-py 5.0.1 (Redis Python client)
- Neo4j Python Driver 5.15.0

### Migration Tools
- Flyway 10.0.1
- Liquibase 4.24.0
- Alembic 1.13.0
- db-migrate 0.11.6

### Monitoring & Backup
- pg_stat_statements
- MongoDB Profiler
- pg_dump
- mysqldump
- mongodump
- HashiCorp Vault 1.15.2
- Cypher Shell

## Quick Start

### PostgreSQL Development
```bash
# Start PostgreSQL
brew services start postgresql  # macOS
sudo systemctl start postgresql  # Linux

# Connect to database
psql -d postgres

# Open pgAdmin
pgadmin4
```

### MongoDB Development
```bash
# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongod  # Linux

# Connect with shell
mongosh

# Open Compass
mongodb-compass
```

### Redis Development
```bash
# Start Redis
brew services start redis  # macOS
sudo systemctl start redis  # Linux

# Connect with CLI
redis-cli

# Open RedisInsight
redis-insight
```

## Database Connections

- **PostgreSQL**: `localhost:5432`
- **MySQL**: `localhost:3306`
- **MongoDB**: `localhost:27017`
- **Redis**: `localhost:6379`
- **Neo4j**: `localhost:7474` (HTTP), `localhost:7687` (Bolt)

## Development Workflow

1. Design database schema
2. Create migrations with Flyway/Liquibase/Alembic
3. Set up development databases
4. Write database integration tests
5. Use GUI tools for administration
6. Monitor performance with built-in tools

## Pro Tips

- Use DBeaver for multi-database management
- Set up automated backups with pg_dump/mysqldump
- Use Testcontainers for integration testing
- Monitor query performance with pg_stat_statements
- Use Vault for secure credential management
- Leverage Redis for caching and session storage

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Redis Documentation](https://redis.io/documentation)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Installation

```bash
he2plus install utils-databases
```

