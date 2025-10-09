#!/usr/bin/env node

/**
 * Basic tests for he2plus npm package
 */

const assert = require('assert');
const { spawn } = require('cross-spawn');
const which = require('which');
const chalk = require('chalk');

console.log(chalk.cyan('🧪 Running he2plus npm package tests...\n'));

let testsRun = 0;
let testsPassed = 0;
let testsFailed = 0;

function test(name, fn) {
  testsRun++;
  try {
    fn();
    testsPassed++;
    console.log(chalk.green(`✅ ${name}`));
    return true;
  } catch (error) {
    testsFailed++;
    console.error(chalk.red(`❌ ${name}`));
    console.error(chalk.red(`   ${error.message}`));
    return false;
  }
}

function asyncTest(name, fn) {
  testsRun++;
  return fn()
    .then(() => {
      testsPassed++;
      console.log(chalk.green(`✅ ${name}`));
      return true;
    })
    .catch((error) => {
      testsFailed++;
      console.error(chalk.red(`❌ ${name}`));
      console.error(chalk.red(`   ${error.message}`));
      return false;
    });
}

// Test 1: Check if main module exists
test('Main module exports', () => {
  const he2plus = require('../index.js');
  assert(typeof he2plus === 'object', 'Module should export an object');
  assert(typeof he2plus.exec === 'function', 'Module should export exec function');
  assert(typeof he2plus.checkPython === 'function', 'Module should export checkPython function');
});

// Test 2: Check if Python is available
test('Python availability check', () => {
  const he2plus = require('../index.js');
  const pythonCmd = he2plus.checkPython();
  
  if (!pythonCmd) {
    throw new Error('Python not found - required for he2plus');
  }
  
  assert(['python', 'python3'].includes(pythonCmd), `Python command should be python or python3, got: ${pythonCmd}`);
});

// Test 3: Check if bin file exists and is executable
test('CLI bin file exists', () => {
  const fs = require('fs');
  const path = require('path');
  const binPath = path.join(__dirname, '..', 'bin', 'he2plus.js');
  
  assert(fs.existsSync(binPath), 'Bin file should exist');
  
  const stats = fs.statSync(binPath);
  assert(stats.isFile(), 'Bin path should be a file');
});

// Test 4: Check package.json
test('Package.json is valid', () => {
  const pkg = require('../package.json');
  
  assert(pkg.name === 'he2plus', 'Package name should be he2plus');
  assert(pkg.version === '0.3.0', 'Package version should be 0.3.0');
  assert(pkg.bin && pkg.bin.he2plus, 'Package should have bin entry');
  assert(pkg.main === 'index.js', 'Package main should be index.js');
});

// Test 5: Check dependencies
test('Required dependencies present', () => {
  const pkg = require('../package.json');
  const requiredDeps = ['chalk', 'commander', 'cross-spawn', 'which'];
  
  requiredDeps.forEach(dep => {
    assert(pkg.dependencies[dep], `Dependency ${dep} should be present`);
  });
});

// Test 6: Try to spawn Python
async function testPythonSpawn() {
  return new Promise((resolve, reject) => {
    const pythonCmd = require('../index.js').checkPython();
    
    if (!pythonCmd) {
      reject(new Error('Python not available'));
      return;
    }
    
    const proc = spawn(pythonCmd, ['--version'], {
      stdio: 'pipe'
    });
    
    let output = '';
    proc.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    proc.stderr.on('data', (data) => {
      output += data.toString();
    });
    
    proc.on('close', (code) => {
      if (code === 0 && output.includes('Python')) {
        resolve();
      } else {
        reject(new Error(`Python version check failed: ${output}`));
      }
    });
    
    proc.on('error', (error) => {
      reject(error);
    });
  });
}

// Run async tests
async function runAsyncTests() {
  await asyncTest('Python spawns correctly', testPythonSpawn);
  
  // Summary
  console.log('');
  console.log(chalk.cyan('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'));
  console.log(chalk.cyan(`Tests run: ${testsRun}`));
  console.log(chalk.green(`Passed: ${testsPassed}`));
  
  if (testsFailed > 0) {
    console.log(chalk.red(`Failed: ${testsFailed}`));
    console.log(chalk.red('❌ Some tests failed'));
    process.exit(1);
  } else {
    console.log(chalk.green('✅ All tests passed!'));
    process.exit(0);
  }
}

runAsyncTests();
