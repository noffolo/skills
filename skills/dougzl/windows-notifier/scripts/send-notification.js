const fs = require('node:fs');
const path = require('node:path');
const { spawnSync, spawn } = require('node:child_process');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function ensureNodeNotifierInstalled(skillDir) {
  const modulePath = path.join(skillDir, 'node_modules', 'node-notifier');
  if (fs.existsSync(modulePath)) return;

  const result = process.platform === 'win32'
    ? spawnSync(process.env.ComSpec || 'cmd.exe', ['/d', '/s', '/c', 'npm.cmd install --no-fund --no-audit'], {
        cwd: skillDir,
        stdio: 'inherit',
        windowsHide: true,
      })
    : spawnSync('npm', ['install', '--no-fund', '--no-audit'], {
        cwd: skillDir,
        stdio: 'inherit',
      });

  if (result.error) {
    throw new Error(`npm install failed: ${result.error.message || String(result.error)}`);
  }

  if (result.status !== 0) {
    throw new Error(`npm install failed with exit code ${result.status ?? 'unknown'}`);
  }
}

function escapePsSingleQuoted(value) {
  return String(value).replace(/'/g, "''");
}

function canUseWpfWindowsDialog() {
  if (process.platform !== 'win32') return false;

  const command = 'powershell.exe';
  const probeScript = [
    "$ErrorActionPreference = 'Stop'",
    'Add-Type -AssemblyName PresentationCore',
    'Add-Type -AssemblyName PresentationFramework',
    'Add-Type -AssemblyName WindowsBase',
    "Write-Output 'WPF_OK'",
  ].join('; ');

  const result = spawnSync(command, [
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-STA',
    '-Command', probeScript,
  ], {
    windowsHide: true,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  return result.status === 0 && String(result.stdout || '').includes('WPF_OK');
}

function showModernWindowsDialog(title, message, appName = 'OpenClaw', wait = false) {
  if (process.platform !== 'win32') {
    throw new Error('modern dialog is only supported on Windows');
  }

  if (!canUseWpfWindowsDialog()) {
    throw new Error('WPF is unavailable in the current Windows session');
  }

  const scriptPath = path.join(__dirname, 'show-modern-dialog.ps1');
  if (!fs.existsSync(scriptPath)) {
    throw new Error('show-modern-dialog.ps1 is missing');
  }

  const command = 'powershell.exe';
  const psArgs = [
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-STA',
    '-File', scriptPath,
    '-Title', title,
    '-Message', message,
    '-AppName', appName,
  ];

  if (wait) {
    const result = spawnSync(command, psArgs, {
      windowsHide: false,
      stdio: 'ignore',
    });

    if (result.status !== 0) {
      throw new Error(`modern dialog failed with exit code ${result.status ?? 'unknown'}`);
    }
    return;
  }

  const innerCommand = `& '${escapePsSingleQuoted(scriptPath)}' -Title '${escapePsSingleQuoted(title)}' -Message '${escapePsSingleQuoted(message)}' -AppName '${escapePsSingleQuoted(appName)}'`;
  const encodedInner = Buffer.from(innerCommand, 'utf16le').toString('base64');
  const launcherScript = `Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-STA', '-EncodedCommand', '${encodedInner}') -WindowStyle Hidden`;
  const result = spawnSync(command, [
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-Command', launcherScript,
  ], {
    windowsHide: true,
    stdio: 'ignore',
  });

  if (result.status !== 0) {
    throw new Error(`modern dialog launcher failed with exit code ${result.status ?? 'unknown'}`);
  }
}

function showNodeNotifier(title, message, appName, wait, timeout, sound, skillDir) {
  ensureNodeNotifierInstalled(skillDir);
  const notifier = require(path.join(skillDir, 'node_modules', 'node-notifier'));

  return new Promise((resolve, reject) => {
    notifier.notify({
      title,
      message,
      wait,
      timeout,
      appID: appName,
      appName,
      sound,
    }, (error) => {
      if (error) {
        reject(error);
        return;
      }
      resolve();
    });
  });
}

(async () => {
  try {
    const skillDir = path.resolve(__dirname, '..');
    const args = parseArgs(process.argv);
    const title = args.title || 'OpenClaw 提醒';
    const message = args.message || '你有一条新的提醒。';
    const appName = args.appName || args.app || 'OpenClaw';
    const timeoutArg = String(args.timeout ?? 'false').toLowerCase();
    const timeout = (timeoutArg === 'false' || timeoutArg === 'permanent' || timeoutArg === 'sticky' || timeoutArg === '0')
      ? false
      : Number(timeoutArg);
    const wait = String(args.wait || 'false').toLowerCase() === 'true';
    const soundArg = String(args.sound || 'true').toLowerCase();
    const sound = !(soundArg === 'false' || soundArg === '0' || soundArg === 'off');
    const modeArg = String(args.mode || '').toLowerCase();
    const wantsModern = modeArg === 'modern' || modeArg === 'card' || modeArg === 'dialog';
    const wantsPersistent = wantsModern || timeout === false;

    if (process.platform === 'win32' && wantsModern) {
      try {
        showModernWindowsDialog(title, message, appName, wait);
        process.exit(0);
        return;
      } catch {
        // Fall through to node-notifier fallback.
      }
    }

    await showNodeNotifier(title, message, appName, wait, timeout, sound, skillDir);
    process.exit(0);
  } catch (error) {
    console.error('WINDOWS_NOTIFY_ERROR');
    console.error(error?.message || String(error));
    process.exit(1);
  }
})();
