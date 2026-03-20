#!/usr/bin/env node
// wallet-ops.mjs — signer/executor dispatcher for AgentWork wallet operations.

import { existsSync, readFileSync } from 'node:fs';
import { randomUUID } from 'node:crypto';

const SIGNER_MODULES = {
  'ethers-keystore': './signers/ethers-keystore.mjs',
  agentkit: './signers/agentkit.mjs',
};

const EXECUTOR_MODULES = {
  'local-rpc': './executors/local-rpc.mjs',
  'onchainos-gateway': './executors/onchainos-gateway.mjs',
  'x402-cdp': './executors/x402.mjs',
  'x402-okx': './executors/x402.mjs',
};

function error(code, message, details = {}) {
  process.stderr.write(JSON.stringify({ error: code, message, details }) + '\n');
  process.exit(1);
}

function output(data) {
  process.stdout.write(JSON.stringify(data) + '\n');
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (!argv[i].startsWith('--')) continue;
    const key = argv[i].slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      args[key] = next;
      i += 1;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function requireArg(args, name) {
  if (!args[name]) {
    error('MISSING_ARG', `--${name} is required`);
  }
  return args[name];
}

function requireAmountMinorArg(args) {
  const amountMinor = args['amount-minor'] ?? args.amount;
  if (!amountMinor) {
    error('MISSING_ARG', '--amount-minor is required');
  }
  return amountMinor;
}

function readOptionalString(value) {
  if (typeof value !== 'string') return null;
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : null;
}

function requirePositiveIntegerInput(rawValue, missingMessage, invalidMessage) {
  const normalized = readOptionalString(rawValue);
  if (!normalized) {
    error('MISSING_EIP3009_CONFIG', missingMessage);
  }
  if (!/^[1-9][0-9]*$/.test(normalized)) {
    error('INVALID_EIP3009_CONFIG', invalidMessage, { value: rawValue });
  }
  return Number.parseInt(normalized, 10);
}

function resolveEip3009Domain(args) {
  const chainId = requirePositiveIntegerInput(
    args['chain-id'] ?? process.env.CHAIN_ID,
    '--chain-id or CHAIN_ID is required for transfer_with_authorization',
    '--chain-id or CHAIN_ID must be a positive integer for transfer_with_authorization',
  );
  const tokenName = readOptionalString(args['token-name'] ?? process.env.CHAIN_TOKEN_EIP3009_NAME);
  if (!tokenName) {
    error(
      'MISSING_EIP3009_CONFIG',
      '--token-name or CHAIN_TOKEN_EIP3009_NAME is required for transfer_with_authorization',
    );
  }
  const tokenVersion = readOptionalString(args['token-version'] ?? process.env.CHAIN_TOKEN_EIP3009_VERSION);
  if (!tokenVersion) {
    error(
      'MISSING_EIP3009_CONFIG',
      '--token-version or CHAIN_TOKEN_EIP3009_VERSION is required for transfer_with_authorization',
    );
  }

  return {
    chainId,
    tokenName,
    tokenVersion,
  };
}

function resolveSignerName(args) {
  return args.signer ?? process.env.AGENTWORK_SIGNER ?? 'ethers-keystore';
}

function resolveExecutorName(args) {
  return args.executor ?? process.env.AGENTWORK_EXECUTOR ?? 'local-rpc';
}

async function loadSignerModule(args) {
  const signerName = resolveSignerName(args);
  const modulePath = SIGNER_MODULES[signerName];
  if (!modulePath) {
    error('UNKNOWN_SIGNER', `Unknown signer: ${signerName}`, { valid: Object.keys(SIGNER_MODULES) });
  }
  return await import(modulePath);
}

async function loadExecutorModule(args) {
  const executorName = resolveExecutorName(args);
  const modulePath = EXECUTOR_MODULES[executorName];
  if (!modulePath) {
    error('UNKNOWN_EXECUTOR', `Unknown executor: ${executorName}`, { valid: Object.keys(EXECUTOR_MODULES) });
  }
  return await import(modulePath);
}

function readSignerMeta(args) {
  if (args['wallet-meta']) {
    try {
      return JSON.parse(args['wallet-meta']);
    } catch (e) {
      error('INVALID_WALLET_META', `Cannot parse --wallet-meta JSON: ${e.message}`);
    }
  }
  if (process.env.AGENTWORK_WALLET_META) {
    try {
      return JSON.parse(process.env.AGENTWORK_WALLET_META);
    } catch (e) {
      error('INVALID_WALLET_META', `Cannot parse AGENTWORK_WALLET_META JSON: ${e.message}`);
    }
  }
  return null;
}

function signerNeedsKeystore(signer) {
  return signer.requiresKeystore !== false;
}

function resolveSignerInputs(args, signer, options = {}) {
  const requireKeystore = options.requireKeystore ?? signerNeedsKeystore(signer);
  const requireExisting = options.requireExisting ?? false;
  const meta = options.meta ?? readSignerMeta(args);

  let keystore = args.keystore;
  if (requireKeystore) {
    keystore = requireArg(args, 'keystore');
    if (requireExisting && !existsSync(keystore)) {
      error('KEYSTORE_NOT_FOUND', `No keystore at ${keystore}`);
    }
  }

  return {
    ...(keystore ? { keystore } : {}),
    meta,
  };
}

function buildWalletBindingFields(args, signer, meta) {
  return {
    wallet_provider: signer.provider ?? resolveSignerName(args),
    wallet_signer_type: signer.signerType ?? (signerNeedsKeystore(signer) ? 'local-keystore' : 'agentkit-managed'),
    ...(meta ? { wallet_meta: meta } : {}),
  };
}

function buildRegistrationMessage(name, address, ttlMinutes) {
  const expiresAt = new Date(Date.now() + ttlMinutes * 60 * 1000);
  return [
    'agentwork:register',
    `name:${name}`,
    `address:${address}`,
    `Expiration Time:${expiresAt.toISOString()}`,
  ].join('\n');
}

function readApiKey(args) {
  let apiKey = args['api-key'];
  if (args['api-key-file']) {
    try {
      apiKey = readFileSync(args['api-key-file'], 'utf8').trim();
    } catch (e) {
      error('FILE_READ_FAILED', `Cannot read --api-key-file: ${e.message}`);
    }
  } else if (!apiKey && process.env.AGENTWORK_API_KEY) {
    apiKey = process.env.AGENTWORK_API_KEY;
  }
  if (!apiKey) {
    error('MISSING_ARG', '--api-key-file, AGENTWORK_API_KEY env, or --api-key is required');
  }
  return apiKey;
}

function readRecoveryCode(args) {
  let recoveryCode = args['recovery-code'];
  if (args['recovery-code-file']) {
    try {
      recoveryCode = readFileSync(args['recovery-code-file'], 'utf8').trim();
    } catch (e) {
      error('FILE_READ_FAILED', `Cannot read --recovery-code-file: ${e.message}`);
    }
  } else if (!recoveryCode && process.env.AGENTWORK_RECOVERY_CODE) {
    recoveryCode = process.env.AGENTWORK_RECOVERY_CODE;
  }
  return recoveryCode;
}

async function cmdGenerate(args) {
  const signer = await loadSignerModule(args);
  const signerInputs = resolveSignerInputs(args, signer, { requireKeystore: signerNeedsKeystore(signer) });
  const created = await signer.createWallet(signerInputs).catch((e) => {
    error('GENERATE_FAILED', e.message);
  });
  const walletFields = buildWalletBindingFields(args, signer, created.meta ?? signerInputs.meta);
  output({
    address: created.address,
    ...(signerInputs.keystore ? { keystore_path: signerInputs.keystore } : {}),
    passphrase_storage: created.passphraseStorage ?? 'managed',
    ...walletFields,
    ...(created.meta ? { meta: created.meta } : {}),
  });
}

function cmdRegisterMessage(args) {
  const name = requireArg(args, 'name');
  const address = requireArg(args, 'address');
  const ttlMinutes = Number.parseInt(args['ttl-minutes'] ?? '5', 10);
  output({ message: buildRegistrationMessage(name, address, ttlMinutes) });
}

async function cmdRegisterSign(args) {
  const signer = await loadSignerModule(args);
  const name = requireArg(args, 'name');
  const ttlMinutes = Number.parseInt(args['ttl-minutes'] ?? '5', 10);
  const signerInputs = resolveSignerInputs(args, signer, { requireKeystore: signerNeedsKeystore(signer) });
  const created = await signer.createWallet(signerInputs).catch((e) => {
    error('GENERATE_FAILED', e.message);
  });
  const runtimeMeta = created.meta ?? signerInputs.meta;
  const address = created.address ?? (await signer.getAddress({
    ...signerInputs,
    meta: runtimeMeta,
  })).address;
  const message = buildRegistrationMessage(name, address, ttlMinutes);
  const signed = await signer.signMessage({
    ...signerInputs,
    meta: runtimeMeta,
    message,
  }).catch((e) => {
    error('SIGN_FAILED', e.message);
  });
  output({
    address,
    message,
    signature: signed.signature,
    ...buildWalletBindingFields(args, signer, runtimeMeta),
    ...(runtimeMeta ? { meta: runtimeMeta } : {}),
  });
}

async function cmdSign(args) {
  const signer = await loadSignerModule(args);
  const signed = await signer.signMessage({
    ...resolveSignerInputs(args, signer, {
      requireKeystore: signerNeedsKeystore(signer),
      requireExisting: signerNeedsKeystore(signer),
    }),
    message: requireArg(args, 'message'),
  }).catch((e) => {
    error('SIGN_FAILED', e.message);
  });
  output(signed);
}

async function cmdAddress(args) {
  const signer = await loadSignerModule(args);
  const result = await signer.getAddress(resolveSignerInputs(args, signer, {
    requireKeystore: signerNeedsKeystore(signer),
    requireExisting: signerNeedsKeystore(signer),
  })).catch((e) => {
    error('KEYSTORE_INVALID', e.message);
  });
  output(result);
}

async function cmdBalance(args) {
  const signer = await loadSignerModule(args);
  const executor = await loadExecutorModule(args);
  const balanceExecutor = typeof executor.getBalances === 'function'
    ? executor
    : await import('./executors/local-rpc.mjs');
  const { address } = await signer.getAddress(resolveSignerInputs(args, signer, {
    requireKeystore: signerNeedsKeystore(signer),
    requireExisting: signerNeedsKeystore(signer),
  })).catch((e) => {
    error('KEYSTORE_INVALID', e.message);
  });

  const balances = await balanceExecutor.getBalances({
    rpc: requireArg(args, 'rpc'),
    token: requireArg(args, 'token'),
    address,
  }).catch((e) => {
    error('RPC_FAILURE', `RPC call failed: ${e.message}`);
  });
  output(balances);
}

async function cmdTransfer(args) {
  const signer = await loadSignerModule(args);
  const executor = await loadExecutorModule(args);
  const { wallet } = await signer.loadWallet(resolveSignerInputs(args, signer, {
    requireKeystore: signerNeedsKeystore(signer),
    requireExisting: signerNeedsKeystore(signer),
  })).catch((e) => {
    error('KEYSTORE_DECRYPT_FAILED', e.message);
  });

  const transferred = await executor.transferToken({
    wallet,
    rpc: requireArg(args, 'rpc'),
    token: requireArg(args, 'token'),
    to: requireArg(args, 'to'),
    amount: requireAmountMinorArg(args),
  }).catch((e) => {
    error('TX_FAILED', e.message);
  });
  output(transferred);
}

async function buildAuthorization(args, signerModule) {
  if ((args['deposit-mode'] ?? 'approve_deposit') !== 'transfer_with_authorization') return null;

  const from = (await signerModule.getAddress({
    ...resolveSignerInputs(args, signerModule, {
      requireKeystore: signerNeedsKeystore(signerModule),
      requireExisting: signerNeedsKeystore(signerModule),
    }),
  })).address;
  const validAfter = BigInt(args['valid-after'] ?? '0');
  const validBefore = BigInt(args['valid-before'] ?? Math.floor(Date.now() / 1000 + 300).toString());
  const authNonce = args['auth-nonce'] ?? `0x${randomUUID().replace(/-/g, '').padEnd(64, '0').slice(0, 64)}`;
  const { chainId, tokenName, tokenVersion } = resolveEip3009Domain(args);
  const domain = {
    name: tokenName,
    version: tokenVersion,
    chainId,
    verifyingContract: requireArg(args, 'token'),
  };
  const types = {
    TransferWithAuthorization: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' },
    ],
  };
  const message = {
    from,
    to: requireArg(args, 'escrow'),
    value: requireAmountMinorArg(args),
    validAfter,
    validBefore,
    nonce: authNonce,
  };
  const signature = await signerModule.signTypedData({
    ...resolveSignerInputs(args, signerModule, {
      requireKeystore: signerNeedsKeystore(signerModule),
      requireExisting: signerNeedsKeystore(signerModule),
    }),
    domain,
    types,
    message,
  }).catch((e) => {
    error('SIGN_FAILED', e.message);
  });

  return {
    from,
    validAfter,
    validBefore,
    authNonce,
    signature: signature.signature,
  };
}

async function cmdDeposit(args) {
  const signer = await loadSignerModule(args);
  const executor = await loadExecutorModule(args);
  const depositMode = args['deposit-mode'] ?? 'approve_deposit';
  const signerInputs = resolveSignerInputs(args, signer, {
    requireKeystore: signerNeedsKeystore(signer),
    requireExisting: signerNeedsKeystore(signer),
  });
  const { address: walletAddress, wallet } = await signer.loadWallet(signerInputs).catch((e) => {
    error('KEYSTORE_DECRYPT_FAILED', e.message);
  });

  let deposited;
  if (depositMode === 'x402') {
    deposited = await executor.depositToEscrow({
      wallet,
      walletAddress,
      depositMode,
      orderRef: requireArg(args, 'order-ref'),
      baseUrl: requireArg(args, 'base-url'),
      apiKey: args['api-key'] ?? process.env.AGENTWORK_API_KEY,
      facilitatorId: args['facilitator-id'],
      executorType: resolveExecutorName(args),
      paymentSignature: args['payment-signature'],
    }).catch((e) => {
      error('DEPOSIT_FAILED', e.message);
    });
  } else {
    const jurors = JSON.parse(requireArg(args, 'jurors'));
    const authorization = await buildAuthorization(args, signer);
    deposited = await executor.depositToEscrow({
      wallet,
      walletAddress,
      rpc: requireArg(args, 'rpc'),
      escrow: requireArg(args, 'escrow'),
      token: requireArg(args, 'token'),
      orderId: requireArg(args, 'order-id'),
      termsHash: requireArg(args, 'terms-hash'),
      amount: requireAmountMinorArg(args),
      seller: requireArg(args, 'seller'),
      jurors,
      threshold: Number.parseInt(requireArg(args, 'threshold'), 10),
      depositMode,
      authorization,
      orderRef: args['order-ref'],
      baseUrl: args['base-url'],
      apiKey: args['api-key'] ?? process.env.AGENTWORK_API_KEY,
      facilitatorId: args['facilitator-id'],
      executorType: resolveExecutorName(args),
      paymentSignature: args['payment-signature'],
    }).catch((e) => {
      error(
        depositMode === 'transfer_with_authorization' ? 'DEPOSIT_WITH_AUTHORIZATION_FAILED' : 'DEPOSIT_FAILED',
        e.message,
      );
    });
  }
  output(deposited);
}

async function cmdAudit(args) {
  const signer = await loadSignerModule(args);
  if (typeof signer.auditKeystore === 'function') {
    output(await signer.auditKeystore({ keystore: requireArg(args, 'keystore') }).catch((e) => {
      error('AUDIT_FAILED', e.message);
    }));
    return;
  }

  output({
    signer: resolveSignerName(args),
    executor: resolveExecutorName(args),
  });
}

async function cmdVerifyWallet(args) {
  if (typeof globalThis.fetch !== 'function') {
    error('MISSING_RUNTIME', 'Node 18+ is required for verify-wallet (built-in fetch)');
  }

  const signer = await loadSignerModule(args);
  const signerInputs = resolveSignerInputs(args, signer, {
    requireKeystore: signerNeedsKeystore(signer),
    requireExisting: signerNeedsKeystore(signer),
  });
  const baseUrl = requireArg(args, 'base-url');
  const chain = args.chain ?? 'base';
  const apiKey = readApiKey(args);
  const recoveryCode = readRecoveryCode(args);

  const { address } = await signer.getAddress(signerInputs).catch((e) => {
    error('KEYSTORE_INVALID', e.message);
  });

  const challengeUrl = `${baseUrl}/agent/v1/profile/wallet-challenge?address=${encodeURIComponent(address)}&chain=${encodeURIComponent(chain)}`;
  let challengeRes;
  try {
    challengeRes = await fetch(challengeUrl, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
  } catch (e) {
    error('CHALLENGE_FETCH_FAILED', `GET wallet-challenge network error: ${e.message}`);
  }
  if (!challengeRes.ok) {
    const body = await challengeRes.text().catch(() => '');
    error('CHALLENGE_FETCH_FAILED', `GET wallet-challenge returned ${challengeRes.status}`, { body });
  }

  let challengeData;
  try {
    challengeData = await challengeRes.json();
  } catch (e) {
    error('CHALLENGE_PARSE_FAILED', `Failed to parse challenge response JSON: ${e.message}`);
  }
  const challenge = challengeData?.data?.challenge;
  if (!challenge || typeof challenge !== 'string') {
    error('CHALLENGE_INVALID', 'wallet-challenge response missing data.challenge');
  }

  const signed = await signer.signMessage({
    ...signerInputs,
    message: challenge,
  }).catch((e) => {
    error('SIGN_FAILED', e.message);
  });

  const nonceLine = challenge.split(/\r?\n/).find((line) => line.startsWith('nonce:'));
  const nonce = nonceLine?.slice('nonce:'.length).trim() ?? 'unknown';
  const body = {
    address,
    chain,
    challenge,
    signature: signed.signature,
    ...buildWalletBindingFields(args, signer, signerInputs.meta),
    ...(recoveryCode ? { recovery_code: recoveryCode } : {}),
    idempotency_key: `verify-wallet:${address.toLowerCase()}:${chain}:${nonce}`,
  };

  let verifyRes;
  try {
    verifyRes = await fetch(`${baseUrl}/agent/v1/profile/verify-wallet`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
    });
  } catch (e) {
    error('VERIFY_FAILED', `POST verify-wallet network error: ${e.message}`);
  }

  if (!verifyRes.ok) {
    const failed = await verifyRes.text().catch(() => '');
    error('VERIFY_FAILED', `POST verify-wallet returned ${verifyRes.status}`, { body: failed });
  }

  const verified = await verifyRes.json().catch((e) => {
    error('VERIFY_PARSE_FAILED', `Failed to parse verify-wallet response JSON: ${e.message}`);
  });
  output(verified.data);
}

const command = process.argv[2];
const args = parseArgs(process.argv.slice(3));

const COMMANDS = {
  generate: cmdGenerate,
  'register-sign': cmdRegisterSign,
  'register-message': cmdRegisterMessage,
  sign: cmdSign,
  'verify-wallet': cmdVerifyWallet,
  address: cmdAddress,
  balance: cmdBalance,
  transfer: cmdTransfer,
  deposit: cmdDeposit,
  audit: cmdAudit,
};

if (!command || !COMMANDS[command]) {
  error(
    'UNKNOWN_COMMAND',
    `Unknown command "${command}". Valid commands: ${Object.keys(COMMANDS).join(', ')}`,
  );
}

await COMMANDS[command](args);
