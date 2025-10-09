#!/usr/bin/env node

/**
 * Post-install script
 * Checks Python and optionally installs he2plus Python package
 */

const { spawn } = require('cross-spawn');
const which = require('which');
const chalk = require('chalk');

function checkPython() {
  try {
    try {
      which.sync('python3');
      return 'python3';
    } catch (e) {
      which.sync('python');
      return 'python';
    }
  } catch (error) {
    return null;
  }
}

async function main() {
  console.log(chalk.cyan('🔍 Checking he2plus dependencies...'));
  
  const pythonCmd = checkPython();
  
  if (!pythonCmd) {
    console.log(chalk.yellow('⚠️  Python not found. Please install Python 3.8+'));
    console.log(chalk.cyan('   he2plus requires Python to be installed.'));
    console.log(chalk.cyan('   - macOS: brew install python3'));
    console.log(chalk.cyan('   - Ubuntu/Debian: sudo apt install python3'));
    console.log(chalk.cyan('   - Windows: https://www.python.org/downloads/'));
    console.log('');
    console.log(chalk.yellow('   The Python package will be installed on first use.'));
    return;
  }

  console.log(chalk.green(`✅ Found ${pythonCmd}`));
  
  // Check if he2plus is already installed
  const checkProc = spawn(pythonCmd, ['-m', 'pip', 'show', 'he2plus'], {
    stdio: 'pipe'
  });
  
  checkProc.on('close', (code) => {
    if (code === 0) {
      console.log(chalk.green('✅ he2plus Python package already installed'));
      console.log('');
      console.log(chalk.cyan('🎉 Setup complete!'));
      console.log(chalk.cyan('   Run: he2plus --help'));
    } else {
      console.log(chalk.yellow('⚠️  he2plus Python package not found'));
      console.log('');
      console.log(chalk.cyan('📦 Installation Required:'));
      console.log(chalk.white('   Install he2plus Python package using one of these methods:\n'));
      console.log(chalk.cyan('   Option 1 (Recommended): Using pipx'));
      console.log(chalk.white('     brew install pipx  # if not already installed'));
      console.log(chalk.white('     pipx install git+https://github.com/he2plus/he2plus-lib.git\n'));
      console.log(chalk.cyan('   Option 2: Using pip with --user'));
      console.log(chalk.white('     pip3 install --user git+https://github.com/he2plus/he2plus-lib.git\n'));
      console.log(chalk.cyan('   Option 3: Using venv'));
      console.log(chalk.white('     python3 -m venv ~/.he2plus-venv'));
      console.log(chalk.white('     source ~/.he2plus-venv/bin/activate'));
      console.log(chalk.white('     pip install git+https://github.com/he2plus/he2plus-lib.git\n'));
      console.log(chalk.cyan('   After installation, run: he2plus --help'));
    }
  });
}

main().catch(console.error);
