#!/usr/bin/env node

/**
 * he2plus - Professional Development Environment Manager
 * Node.js wrapper for the Python CLI
 */

const { spawn } = require('cross-spawn');
const which = require('which');
const chalk = require('chalk');

/**
 * Check if Python is available
 */
function checkPython() {
  try {
    // Try python3 first, then python
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

/**
 * Check if he2plus Python package is installed
 */
function checkHe2plus(pythonCmd) {
  return new Promise((resolve) => {
    const proc = spawn(pythonCmd, ['-m', 'pip', 'show', 'he2plus'], {
      stdio: 'pipe'
    });
    
    proc.on('close', (code) => {
      resolve(code === 0);
    });
    
    proc.on('error', () => {
      resolve(false);
    });
  });
}

/**
 * Run he2plus command
 */
async function runHe2plus(args) {
  const pythonCmd = checkPython();
  
  if (!pythonCmd) {
    console.error(chalk.red('❌ Error: Python is not installed or not in PATH'));
    console.error(chalk.yellow('   Please install Python 3.8 or higher:'));
    console.error(chalk.cyan('   - macOS: brew install python3'));
    console.error(chalk.cyan('   - Ubuntu/Debian: sudo apt install python3'));
    console.error(chalk.cyan('   - Windows: https://www.python.org/downloads/'));
    process.exit(1);
  }

  const he2plusInstalled = await checkHe2plus(pythonCmd);
  
  if (!he2plusInstalled) {
    console.error(chalk.yellow('⚠️  he2plus Python package is not installed'));
    console.error(chalk.cyan('   Please install it using one of these methods:\n'));
    console.error(chalk.cyan('   Option 1 (Recommended): Using pipx'));
    console.error(chalk.white('     brew install pipx'));
    console.error(chalk.white('     pipx install git+https://github.com/he2plus/he2plus-lib.git\n'));
    console.error(chalk.cyan('   Option 2: Using pip with --user'));
    console.error(chalk.white('     pip3 install --user git+https://github.com/he2plus/he2plus-lib.git\n'));
    console.error(chalk.cyan('   Option 3: Using virtual environment'));
    console.error(chalk.white('     python3 -m venv ~/.he2plus-venv'));
    console.error(chalk.white('     source ~/.he2plus-venv/bin/activate'));
    console.error(chalk.white('     pip install git+https://github.com/he2plus/he2plus-lib.git\n'));
    console.error(chalk.cyan('   After installation, run the command again.'));
    process.exit(1);
  }

  // Run the actual he2plus command
  const proc = spawn('he2plus', args, {
    stdio: 'inherit',
    shell: true
  });

  proc.on('error', (error) => {
    console.error(chalk.red('❌ Error running he2plus:'), error.message);
    process.exit(1);
  });

  proc.on('close', (code) => {
    process.exit(code || 0);
  });
}

/**
 * Export for programmatic use
 */
module.exports = {
  checkPython,
  checkHe2plus,
  runHe2plus,
  
  /**
   * Execute he2plus command programmatically
   */
  exec: function(command, options = {}) {
    return new Promise((resolve, reject) => {
      const pythonCmd = checkPython();
      
      if (!pythonCmd) {
        reject(new Error('Python not found'));
        return;
      }

      const args = command.split(' ');
      const proc = spawn('he2plus', args, {
        stdio: options.silent ? 'pipe' : 'inherit',
        shell: true
      });

      let stdout = '';
      let stderr = '';

      if (options.silent) {
        proc.stdout.on('data', (data) => {
          stdout += data.toString();
        });
        
        proc.stderr.on('data', (data) => {
          stderr += data.toString();
        });
      }

      proc.on('close', (code) => {
        if (code === 0) {
          resolve({ code, stdout, stderr });
        } else {
          reject(new Error(`Command failed with code ${code}`));
        }
      });

      proc.on('error', (error) => {
        reject(error);
      });
    });
  }
};

// Run CLI if called directly
if (require.main === module) {
  const args = process.argv.slice(2);
  runHe2plus(args);
}
