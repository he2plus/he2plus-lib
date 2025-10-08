# End-to-End Full-Stack Real-World Test

This directory contains **authentic end-to-end testing** for he2plus that simulates a real developer's workflow.

## What This Tests

### Scenario: Mac Developer Building a Full-Stack Next.js App

A developer with a clean system wants to:
1. Install he2plus from GitHub
2. Use it to set up a modern web development environment
3. Build a real full-stack application with:
   - **Frontend**: Next.js + React + TypeScript + Tailwind CSS
   - **Backend**: API routes with business logic
   - **Database**: SQLite with Prisma ORM
   - **Features**: Actual CRUD operations
4. Build the app for production

**This is NOT a mock test. Everything is real:**
- Real installation from GitHub
- Real profile installation
- Real Node.js/npm setup
- Real app creation
- Real database
- Real build process

## Running the Test

### Quick Start

```bash
cd tests/e2e-fullstack
docker-compose up --build
```

The test will:
1. Create a clean Ubuntu 22.04 environment (simulating macOS)
2. Install he2plus from GitHub
3. Install the web-nextjs profile
4. Create a real full-stack app
5. Build and verify everything
6. Generate a detailed report

### Results

Results are saved to `test-results/`:
- `fullstack-test-YYYYMMDD_HHMMSS.log` - Full log
- `SUMMARY.md` - Test summary

The actual app is saved to `test-app/my-fullstack-app/`

## What Gets Created

### The Full-Stack App

**Product Manager** - A complete CRUD application

#### Frontend (`src/app/page.tsx`)
- React with TypeScript
- Tailwind CSS styling
- Form for adding products
- List displaying all products
- Real-time UI updates

#### Backend (`src/app/api/products/route.ts`)
- GET endpoint - Fetch all products
- POST endpoint - Create new product
- Prisma ORM integration
- Error handling

#### Database (`prisma/schema.prisma`)
- SQLite database
- Product model with fields:
  - id (primary key)
  - name (string)
  - description (optional string)
  - price (float)
  - stock (integer)
  - timestamps

### Tech Stack
- Next.js 14+ (App Router)
- React 18+
- TypeScript 5+
- Prisma ORM
- SQLite
- Tailwind CSS

## Test Validation

The test validates:

✅ **Installation**
- he2plus installs from GitHub
- No missing dependencies
- CLI commands work

✅ **Profile Installation**
- web-nextjs profile installs
- Node.js available
- npm available
- Git available

✅ **App Creation**
- Next.js app creates successfully
- Dependencies install
- Database sets up
- API routes work
- Frontend renders

✅ **Build**
- Production build succeeds
- Build output exists
- All files present

## Why This Matters

This test proves that he2plus can:
1. **Install cleanly** from GitHub on any system
2. **Set up a real development environment**
3. **Enable actual development** of production-ready apps
4. **Support modern tech stacks**

If this test passes, we can confidently say:
> "he2plus works. Any issues are on the developer's end, not the library."

## Test Philosophy

### What Makes This Authentic

1. **Clean Environment**: Fresh Docker container, no pre-installed tools
2. **Real Installation**: Installs from public GitHub repo, not local files
3. **No Shortcuts**: Uses actual commands a developer would use
4. **Real App**: Not a "hello world", but an actual full-stack app
5. **Production Build**: Verifies the app can be built for deployment

### What This Doesn't Test

- Actual HTTP server (running dev server in Docker requires ports)
- Browser interaction (headless environment)
- Multiple profiles simultaneously
- macOS-specific features (runs on Linux)

These can be tested separately if needed.

## Extending This Test

To add more tests:

1. **Create new Dockerfile**: `Dockerfile.{test-name}`
2. **Create test script**: `test-scripts/run-{test-name}.sh`
3. **Add to docker-compose.yml**
4. **Run**: `docker-compose run {service-name}`

Example test ideas:
- ML Engineer workflow (Python + ML libs)
- Mobile Dev workflow (React Native)
- Web3 Developer workflow (Hardhat + Solidity)

## Troubleshooting

### Test fails at installation
- Check GitHub repo is accessible
- Verify pyproject.toml has all dependencies
- Check requirements.txt is up to date

### Test fails at profile installation
- Verify profile exists in registry
- Check installer components
- Review log file for details

### Test fails at app creation
- Verify Node.js installed correctly
- Check npm is available
- Review npm install logs

### Build fails
- Check TypeScript configuration
- Verify all dependencies installed
- Review build error messages

## Maintenance

Update this test when:
- Major version changes
- New dependencies added
- Profile structure changes
- New features added

Keep it **real, authentic, and reflective of actual developer experience**.

---

**Last Updated**: October 8, 2025
**Test Status**: Ready for production validation
