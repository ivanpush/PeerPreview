#!/usr/bin/env node

/**
 * Test script to verify demo review files are properly structured and loadable
 */

const fs = require('fs');
const path = require('path');

const REVIEWS_DIR = path.join(__dirname, '../frontend-d2/public/reviews');
const FIXTURES_DIR = path.join(__dirname, '../frontend-d2/public/fixtures');

// Expected review files
const expectedReviews = [
  'manuscript_pdf_firstpass.json',
  'manuscript_pdf_fullreview.json',
  'grant_docx_fullreview.json',
  'policy_brief_pdf_fullreview.json'
];

console.log('Testing Demo Review Files\n');
console.log('=' .repeat(50));

// Check if reviews directory exists
if (!fs.existsSync(REVIEWS_DIR)) {
  console.error('❌ Reviews directory not found:', REVIEWS_DIR);
  process.exit(1);
}
console.log('✅ Reviews directory exists');

// Check each expected review file
let allValid = true;
expectedReviews.forEach(filename => {
  const filepath = path.join(REVIEWS_DIR, filename);
  console.log(`\nChecking ${filename}...`);

  if (!fs.existsSync(filepath)) {
    console.error(`  ❌ File not found`);
    allValid = false;
    return;
  }

  try {
    const content = fs.readFileSync(filepath, 'utf8');
    const data = JSON.parse(content);

    // Validate required fields
    const requiredFields = ['review_id', 'document_id', 'document_type', 'depth', 'scopes', 'issues'];
    const missingFields = requiredFields.filter(field => !data[field]);

    if (missingFields.length > 0) {
      console.error(`  ❌ Missing required fields: ${missingFields.join(', ')}`);
      allValid = false;
      return;
    }

    // Check issues structure
    if (!Array.isArray(data.issues)) {
      console.error(`  ❌ Issues is not an array`);
      allValid = false;
      return;
    }

    if (data.issues.length === 0) {
      console.warn(`  ⚠️  No issues in review`);
    } else {
      // Check first issue has required fields
      const firstIssue = data.issues[0];
      const issueFields = ['id', 'scope', 'persona', 'severity'];
      const missingIssueFields = issueFields.filter(field => !firstIssue[field]);

      if (missingIssueFields.length > 0) {
        console.error(`  ❌ First issue missing fields: ${missingIssueFields.join(', ')}`);
        allValid = false;
        return;
      }
    }

    console.log(`  ✅ Valid structure`);
    console.log(`  📊 Stats:`);
    console.log(`     - Review ID: ${data.review_id}`);
    console.log(`     - Depth: ${data.depth}`);
    console.log(`     - Scopes: ${data.scopes.join(', ')}`);
    console.log(`     - Issues: ${data.issues.length}`);

    // Count issues by severity
    const severityCounts = {};
    data.issues.forEach(issue => {
      severityCounts[issue.severity] = (severityCounts[issue.severity] || 0) + 1;
    });
    console.log(`     - By severity: ${Object.entries(severityCounts).map(([k,v]) => `${k}:${v}`).join(', ')}`);

    // Check if persona_summaries exist
    if (data.persona_summaries) {
      console.log(`     - Persona summaries: ${Object.keys(data.persona_summaries).join(', ')}`);
    }

  } catch (err) {
    console.error(`  ❌ Error parsing JSON: ${err.message}`);
    allValid = false;
  }
});

// Check for matching fixtures
console.log('\n' + '=' .repeat(50));
console.log('Checking fixture alignment...\n');

expectedReviews.forEach(reviewFile => {
  const fixtureBase = reviewFile.split('_').slice(0, -1).join('_'); // Remove depth suffix
  const possibleFixtures = [
    `${fixtureBase}.json`,
    `${fixtureBase.replace('_pdf', '.pdf')}.json`,
    `${fixtureBase.replace('_docx', '.docx')}.json`
  ];

  let foundFixture = false;
  for (const fixtureName of possibleFixtures) {
    const fixturePath = path.join(FIXTURES_DIR, fixtureName);
    if (fs.existsSync(fixturePath)) {
      console.log(`✅ ${reviewFile} → ${fixtureName}`);
      foundFixture = true;
      break;
    }
  }

  if (!foundFixture) {
    console.warn(`⚠️  ${reviewFile} → No matching fixture found`);
  }
});

// Final summary
console.log('\n' + '=' .repeat(50));
if (allValid) {
  console.log('✅ All review files are valid and ready for use!');
} else {
  console.log('❌ Some issues found. Please fix them before testing.');
  process.exit(1);
}

console.log('\nTo test in the app:');
console.log('1. Start the frontend: cd demo2/frontend-d2 && npm run dev');
console.log('2. Go to Review Setup screen');
console.log('3. Select "Static Demo" mode');
console.log('4. Choose a document and depth');
console.log('5. Click "Start Review"');