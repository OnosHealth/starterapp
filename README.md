# Django Multi-Tenant Application with Subtenants

A Django application with django-tenants support and Django Ninja API. Each tenant corresponds to a health insurance company with subtenants (e.g., regional divisions) and members. Using django-tenants, the tenant data is isolated in separate database schemas.

## Prerequisites

- Docker
- Python 3.10+
- Access to modify your host file (for domain routing)

## Quick Start

```bash
# Clone and navigate to the repository
git clone <repository-url>
cd onos-test

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL with Docker
docker compose up -d

# Apply migrations
python manage.py migrate_schemas --shared

# Create a public tenant
python manage.py create_tenant --schema_name=public --name="Public Tenant" --domain-domain=localhost --domain-is_primary=True

# Create a tenant (example: UHC)
python manage.py create_tenant --schema_name=uhc --name="UHC" --domain-domain=uhc.localhost --domain-is_primary=True

# Create a superuser for the public schema
python manage.py createsuperuser

# Create a superuser for the tenant schema
python manage.py create_tenant_superuser --schema=uhc

# Run the development server
python manage.py runserver
```

## Host File Configuration

To access tenant-specific domains, you need to modify your hosts file:

### On macOS/Linux:
```bash
sudo nano /etc/hosts
```

### On Windows:
Open Notepad as Administrator and open:
```
C:\Windows\System32\drivers\etc\hosts
```

### Add the following lines:
```
127.0.0.1 localhost
127.0.0.1 uhc.localhost
# Add additional tenant domains as needed
```

## Admin Access

### Public Schema Admin
- URL: `http://localhost:8000/admin/`
- Login with the superuser credentials created for the public schema
- Here you can manage Clients (tenants), Domains, and Subtenants

### Tenant Admin
- URL: `http://uhc.localhost:8000/admin/` (replace 'uhc' with your tenant's domain)
- Login with the tenant superuser credentials
- Here you can manage tenant-specific data (Members)

## Managing Subtenants

Subtenants are managed in the public schema admin:

1. Login to `http://localhost:8000/admin/`
2. Navigate to "Sub tenants" under the SHARED_APP section
3. Click "Add Sub tenant"
4. Select the Client/Tenant (e.g., UHC)
5. Enter a name for the subtenant (e.g., "ny" for New York)
6. Save

## API Documentation and Endpoints

### API Documentation
- Public Schema API Docs: `http://localhost:8000/api/docs`
- Tenant API Docs: `http://uhc.localhost:8000/api/docs` (replace 'uhc' with your tenant's domain)

### Shared API (Public Schema)
- `GET http://localhost:8000/api/clients` - List all tenants
- `GET http://localhost:8000/api/domains` - List all domains

### No longer functional - Tenant API (Tenant-specific)
- `GET http://uhc.localhost:8000/api/members` - List all members
- `POST http://uhc.localhost:8000/api/members` - Create a member
- `GET http://uhc.localhost:8000/api/members/{id}` - Get member details
- `PUT http://uhc.localhost:8000/api/members/{id}` - Update a member
- `DELETE http://uhc.localhost:8000/api/members/{id}` - Delete a member

### New Implementation - Subtenant API (Subtenant-specific)
- `GET http://uhc.localhost:8000/api/members/{subtenant_name}` - List members for a subtenant
- `POST http://uhc.localhost:8000/api/members/{subtenant_name}` - Create a member for a subtenant
- `GET http://uhc.localhost:8000/api/members/{subtenant_name}/{id}` - Get subtenant member details
- `PUT http://uhc.localhost:8000/api/members/{subtenant_name}/{id}` - Update a subtenant member
- `DELETE http://uhc.localhost:8000/api/members/{subtenant_name}/{id}` - Delete a subtenant member

Example: `http://uhc.localhost:8000/api/members/ny` will return members associated with the "ny" subtenant.

## Project Structure

- `shared_app` - Contains shared models in the public schema (Client, Domain, SubTenant)
- `tenant_app` - Contains tenant-specific models (e.g., Member) and API endpoints
- `starterapp` - Contains project settings and URL configurations

## Advanced Usage

### Creating a Tenant and Superuser in One Step

To create a tenant and its superuser in a single workflow:

```bash
# Create tenant
python manage.py create_tenant --schema_name=aetna --name="Aetna" --domain-domain=aetna.localhost --domain-is_primary=True

# Create tenant superuser
python manage.py create_tenant_superuser --schema=aetna
```

### Typical Workflow

1. Create a tenant in the public schema admin or via command
2. Create a superuser for the tenant
3. Configure host file to include the tenant domain
4. Create subtenants in the public schema admin
5. Access tenant admin and API using the tenant domain
6. Use subtenant-specific API endpoints to manage data by subtenant

## Testing

This project uses pytest for automated testing with test isolation between tenants.

```bash
# Run all tests
pytest

# Run specific test file
pytest tenant_app/tests/test_integration_members.py
```

## Troubleshooting

- **404 Error when accessing tenant admin**: Ensure your hosts file is configured correctly and you're using the right domain format (`tenant.localhost:8000`)
- **Tenant superuser login fails**: Make sure you created a superuser for that specific tenant schema
- **API returns empty data**: Verify you're accessing the correct tenant domain and that subtenant names are correct
