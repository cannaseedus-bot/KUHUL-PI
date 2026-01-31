#!/usr/bin/env node
'use strict';

/*
 * KUHUL-ES CLI
 * Version Integrity + Trace Artifact
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { program } = require('commander');

// -----------------------------------------------------------------------------
// Version (single source of truth)
// -----------------------------------------------------------------------------
const pkg = require('../package.json');

// -----------------------------------------------------------------------------
// Banner
// -----------------------------------------------------------------------------
console.log(`
╔══════════════════════════════════════╗
║        KUHUL-ES v${pkg.version}               ║
║  ECMAScript syntax, KUHUL semantics  ║
╚══════════════════════════════════════╝
`);

// -----------------------------------------------------------------------------
// CLI Definition
// -----------------------------------------------------------------------------
program
  .name('kuhul-es')
  .description('KUHUL-ES - The Trojan Horse for KUHUL semantics')
  .version(pkg.version);

// -----------------------------------------------------------------------------
// init
// -----------------------------------------------------------------------------
program
  .command('init [project-name]')
  .description('Initialize a new KUHUL-ES project')
  .action((projectName = 'my-kuhul-app') => {
    console.log(`Creating project: ${projectName}`);
    console.log('Use `kuhul-es new <name>` for full scaffold');
    process.exit(0);
  });

// -----------------------------------------------------------------------------
// new (FULL PROJECT SCAFFOLD)
// -----------------------------------------------------------------------------
program
  .command('new <name>')
  .description('Create a new KUHUL-ES project from template')
  .action((name) => {
    console.log(`Creating project: ${name}`);

    fs.mkdirSync(name, { recursive: true });

    const template = `
π config = {
  name: "${name}",
  version: "1.0.0",
  author: "${process.env.USERNAME || 'Developer'}"
};

τ frame = 0;

function* main() {
  yield* Sek('log', \`🚀 Starting \${config.name} v\${config.version}\`);

  @for (let i = 0; i < 5; i++) {
    yield* Sek('log', \`Frame: \${frame}\`);
    frame += 1;
    yield* Sek('wait', 100);
  }

  yield* Sek('log', '✅ Project ready!');
}

main();
`.trim();

    fs.writeFileSync(path.join(name, 'main.kuhules'), template);

    const packageJson = {
      name,
      version: '1.0.0',
      private: true,
      scripts: {
        start: 'kuhul-es run main.kuhules',
        dev: 'kuhul-es run main.kuhules --record'
      },
      dependencies: {
        'kuhul-es': `^${pkg.version}`
      }
    };

    fs.writeFileSync(
      path.join(name, 'package.json'),
      JSON.stringify(packageJson, null, 2)
    );

    console.log(`✓ Project created: ${name}`);
    console.log(`  cd ${name}`);
    console.log(`  npm install`);
    console.log(`  npm start`);
    process.exit(0);
  });

// -----------------------------------------------------------------------------
// compile
// -----------------------------------------------------------------------------
program
  .command('compile <input>')
  .description('Compile KUHUL-ES source file')
  .option('-o, --output <file>', 'Output file')
  .option('-w, --watch', 'Watch for changes')
  .action((input, options) => {
    console.log(`Compiling ${input}...`);

    if (options.output) {
      console.log(`→ Output: ${options.output}`);
    }
    if (options.watch) {
      console.log('Watch mode enabled (stub)');
    }

    console.log('✓ Compile complete (stub)');
    process.exit(0);
  });

// -----------------------------------------------------------------------------
// run
// -----------------------------------------------------------------------------
program
  .command('run <file>')
  .description('Run a KUHUL-ES program')
  .option('--record', 'Record deterministic execution trace')
  .option('--replay <trace>', 'Replay from a recorded trace file')
  .action((file, options) => {
    console.log(`▶ Running: ${file}`);

    if (options.record) {
      console.log('Recording execution');

      const trace = {
        version: pkg.version,
        file,
        argv: process.argv.slice(2),
        cwd: process.cwd(),
        timestamp: new Date().toISOString()
      };

      trace.hash = crypto
        .createHash('sha256')
        .update(JSON.stringify(trace))
        .digest('hex');

      const outPath = path.resolve(process.cwd(), 'trace.json');
      fs.writeFileSync(outPath, JSON.stringify(trace, null, 2));

      console.log('trace.json written');
      console.log(`trace hash: ${trace.hash}`);
    }

    if (options.replay) {
      console.log(`Replaying ${options.replay}`);

      const replayPath = path.resolve(process.cwd(), options.replay);
      const trace = JSON.parse(fs.readFileSync(replayPath, 'utf8'));

      const expectedHash = crypto
        .createHash('sha256')
        .update(JSON.stringify({ ...trace, hash: undefined }))
        .digest('hex');

      if (trace.hash !== expectedHash) {
        console.error('Trace hash mismatch');
        process.exit(1);
      }

      console.log('Trace verified');
      console.log(`trace hash: ${trace.hash}`);
    }

    console.log('Execution complete (stub)');
    process.exit(0);
  });

// -----------------------------------------------------------------------------
// doctor
// -----------------------------------------------------------------------------
program
  .command('doctor')
  .description('Run environment diagnostics for KUHUL-ES')
  .action(() => {
    console.log('KUHUL-ES Doctor\n');

    console.log('Version:', pkg.version);
    console.log('Node:', process.version);
    console.log('Platform:', process.platform);
    console.log('CLI path:', __filename);
    console.log('CWD:', process.cwd());

    try {
      require.resolve('commander');
      console.log('Commander: OK');
    } catch {
      console.log('Commander: MISSING');
      process.exit(1);
    }

    console.log('\nDiagnostics complete');
    process.exit(0);
  });

// -----------------------------------------------------------------------------
// Parse
// -----------------------------------------------------------------------------
program.parse(process.argv);

if (!process.argv.slice(2).length) {
  program.outputHelp();
}
