#!/usr/bin/env bash
set -euo pipefail

VERSION="3.0.0"
SCRIPT_NAME="onchain-analyzer"
DATA_DIR="${ONCHAIN_ANALYZER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/onchain-analyzer}"
mkdir -p "$DATA_DIR"

BRAND="Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"

# API endpoints
BTC_API="https://blockstream.info/api"
ETH_API="https://api.etherscan.io/api"

# ─── Helpers ──────────────────────────────────────────────────────────
log_history() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $*" >> "$DATA_DIR/history.log"
}

print_header() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $SCRIPT_NAME v$VERSION — $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

print_footer() {
    echo "──────────────────────────────────────────────────────"
    echo "  $BRAND"
    echo "──────────────────────────────────────────────────────"
}

require_cmd() {
    for cmd in "$@"; do
        if ! command -v "$cmd" &>/dev/null; then
            echo "ERROR: Required command '$cmd' not found." >&2
            exit 1
        fi
    done
}

safe_curl() {
    local url="$1"
    local result
    if ! result=$(curl -sS --max-time 15 --retry 2 "$url" 2>&1); then
        echo "ERROR: Failed to fetch $url" >&2
        echo "$result" >&2
        return 1
    fi
    echo "$result"
}

json_field() {
    local json="$1" field="$2"
    echo "$json" | grep -oP "\"$field\"\s*:\s*\"?\K[^,\"}\]]*" | head -1
}

format_btc() {
    local satoshis="$1"
    awk "BEGIN{printf \"%.8f BTC\", $satoshis / 100000000}"
}

is_eth_address() {
    [[ "$1" =~ ^0x[a-fA-F0-9]{40}$ ]]
}

is_btc_address() {
    [[ "$1" =~ ^(1|3|bc1)[a-zA-Z0-9]{25,62}$ ]]
}

# ─── Commands ─────────────────────────────────────────────────────────

cmd_address() {
    local addr="${1:-}"
    if [[ -z "$addr" ]]; then
        echo "Usage: $SCRIPT_NAME address <btc_address>" >&2
        exit 1
    fi
    require_cmd curl
    print_header "Address Info: ${addr:0:16}..."
    log_history "address $addr"
    echo ""

    if is_btc_address "$addr"; then
        echo "  Chain: Bitcoin"
        echo "  Address: $addr"
        echo ""

        local data
        data=$(safe_curl "$BTC_API/address/$addr") || { print_footer; return 1; }

        local funded_sum spent_sum tx_count
        funded_sum=$(json_field "$data" "funded_txo_sum")
        spent_sum=$(json_field "$data" "spent_txo_sum")
        tx_count=$(json_field "$data" "tx_count")

        echo "  ── Address Summary ──"
        printf "    Total Received:  %s\n" "$(format_btc "${funded_sum:-0}")"
        printf "    Total Spent:     %s\n" "$(format_btc "${spent_sum:-0}")"
        if [[ -n "$funded_sum" && -n "$spent_sum" ]]; then
            local balance
            balance=$((${funded_sum:-0} - ${spent_sum:-0}))
            printf "    Balance:         %s\n" "$(format_btc "$balance")"
        fi
        printf "    Transactions:    %s\n" "${tx_count:-0}"
        echo ""

        echo "  ── Recent Transactions ──"
        local txs
        txs=$(safe_curl "$BTC_API/address/$addr/txs" 2>/dev/null || echo "[]")
        echo "$txs" | grep -oP '"txid"\s*:\s*"\K[a-f0-9]+' | head -5 | while read -r txid; do
            echo "    $txid"
        done
    elif is_eth_address "$addr"; then
        echo "  Chain: Ethereum"
        echo "  Address: $addr"
        echo ""
        echo "  ── Balance ──"
        local bal_data
        bal_data=$(safe_curl "${ETH_API}?module=account&action=balance&address=$addr&tag=latest" 2>/dev/null || echo "{}")
        local bal_wei
        bal_wei=$(json_field "$bal_data" "result")
        if [[ -n "$bal_wei" && "$bal_wei" != "0" ]]; then
            local bal_eth
            bal_eth=$(awk "BEGIN{printf \"%.6f\", $bal_wei / 1000000000000000000}")
            printf "    Balance: %s ETH\n" "$bal_eth"
        else
            echo "    Balance: 0 ETH (or API rate limited)"
        fi

        echo ""
        echo "  ── Recent Transactions ──"
        local tx_data
        tx_data=$(safe_curl "${ETH_API}?module=account&action=txlist&address=$addr&startblock=0&endblock=99999999&page=1&offset=5&sort=desc" 2>/dev/null || echo "{}")
        echo "$tx_data" | grep -oP '"hash"\s*:\s*"\K0x[a-f0-9]+' | head -5 | while read -r txhash; do
            echo "    $txhash"
        done
    else
        echo "  ⚠️  Cannot determine chain for: $addr"
        echo "  Supported: BTC (1.../3.../bc1...) or ETH (0x...)"
    fi
    echo ""
    print_footer
}

cmd_tx() {
    local hash="${1:-}"
    if [[ -z "$hash" ]]; then
        echo "Usage: $SCRIPT_NAME tx <transaction_hash>" >&2
        exit 1
    fi
    require_cmd curl
    print_header "Transaction: ${hash:0:20}..."
    log_history "tx $hash"
    echo ""

    if [[ "$hash" =~ ^0x ]]; then
        echo "  Chain: Ethereum"
        echo "  Hash: $hash"
        echo ""
        local data
        data=$(safe_curl "${ETH_API}?module=proxy&action=eth_getTransactionByHash&txhash=$hash" 2>/dev/null || echo "{}")
        local from to value_hex block_hex gas_hex
        from=$(json_field "$data" "from")
        to=$(json_field "$data" "to")
        value_hex=$(json_field "$data" "value")
        block_hex=$(json_field "$data" "blockNumber")
        gas_hex=$(json_field "$data" "gas")

        if [[ -n "$from" ]]; then
            printf "    From:   %s\n" "$from"
            printf "    To:     %s\n" "$to"
            if [[ -n "$value_hex" ]]; then
                local value_dec
                value_dec=$(printf "%d" "$value_hex" 2>/dev/null || echo "0")
                printf "    Value:  %s ETH\n" "$(awk "BEGIN{printf \"%.6f\", $value_dec / 1000000000000000000}")"
            fi
            if [[ -n "$block_hex" ]]; then
                printf "    Block:  %d\n" "$block_hex" 2>/dev/null || echo "    Block: $block_hex"
            fi
        else
            echo "    Transaction not found or API rate limited"
        fi
    else
        echo "  Chain: Bitcoin"
        echo "  TXID: $hash"
        echo ""
        local data
        data=$(safe_curl "$BTC_API/tx/$hash") || { print_footer; return 1; }
        local status confirmed fee size
        status=$(json_field "$data" "confirmed")
        fee=$(json_field "$data" "fee")
        size=$(json_field "$data" "size")

        echo "  ── Transaction Details ──"
        printf "    Confirmed:  %s\n" "${status:-unknown}"
        printf "    Fee:        %s sats (%s)\n" "${fee:-?}" "$(format_btc "${fee:-0}")"
        printf "    Size:       %s bytes\n" "${size:-?}"

        local block_height block_time
        block_height=$(echo "$data" | grep -oP '"block_height"\s*:\s*\K[0-9]+' | head -1)
        block_time=$(echo "$data" | grep -oP '"block_time"\s*:\s*\K[0-9]+' | head -1)
        if [[ -n "$block_height" ]]; then
            printf "    Block:      %s\n" "$block_height"
        fi
        if [[ -n "$block_time" ]]; then
            printf "    Time:       %s\n" "$(date -d "@$block_time" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "$block_time")"
        fi

        echo ""
        echo "  ── Inputs ──"
        echo "$data" | grep -oP '"prevout".*?"value"\s*:\s*\K[0-9]+' | head -5 | while read -r val; do
            printf "    ← %s\n" "$(format_btc "$val")"
        done

        echo ""
        echo "  ── Outputs ──"
        echo "$data" | grep -oP '"scriptpubkey_address"\s*:\s*"\K[^"]+' | head -5 | while read -r out_addr; do
            echo "    → $out_addr"
        done
    fi
    echo ""
    print_footer
}

cmd_balance() {
    local addr="${1:-}"
    if [[ -z "$addr" ]]; then
        echo "Usage: $SCRIPT_NAME balance <address>" >&2
        exit 1
    fi
    require_cmd curl
    print_header "Balance Check"
    log_history "balance $addr"
    echo ""

    if is_btc_address "$addr"; then
        echo "  Chain:   Bitcoin"
        echo "  Address: $addr"
        echo ""
        local data
        data=$(safe_curl "$BTC_API/address/$addr") || { print_footer; return 1; }
        local funded spent
        funded=$(json_field "$data" "funded_txo_sum")
        spent=$(json_field "$data" "spent_txo_sum")
        local balance_sats=$(( ${funded:-0} - ${spent:-0} ))
        printf "  Balance: %s\n" "$(format_btc "$balance_sats")"
        printf "  Satoshis: %d\n" "$balance_sats"
        echo ""
        # Approximate USD (rough rate)
        echo "  Note: For live USD conversion, check a price API"
    elif is_eth_address "$addr"; then
        echo "  Chain:   Ethereum"
        echo "  Address: $addr"
        echo ""
        local data
        data=$(safe_curl "${ETH_API}?module=account&action=balance&address=$addr&tag=latest" 2>/dev/null || echo "{}")
        local bal_wei
        bal_wei=$(json_field "$data" "result")
        if [[ -n "$bal_wei" && "$bal_wei" =~ ^[0-9]+$ ]]; then
            local bal_eth
            bal_eth=$(awk "BEGIN{printf \"%.8f\", $bal_wei / 1000000000000000000}")
            printf "  Balance: %s ETH\n" "$bal_eth"
            printf "  Wei:     %s\n" "$bal_wei"
        else
            echo "  Balance: Unable to fetch (API rate limit or invalid address)"
        fi
    else
        echo "  ⚠️  Unsupported address format: $addr"
    fi
    echo ""
    print_footer
}

cmd_gas() {
    require_cmd curl
    print_header "Gas Prices"
    log_history "gas"
    echo ""

    echo "  ── Ethereum Gas (from Etherscan) ──"
    local data
    data=$(safe_curl "${ETH_API}?module=gastracker&action=gasoracle" 2>/dev/null || echo "{}")
    local safe_gas propose_gas fast_gas
    safe_gas=$(json_field "$data" "SafeGasPrice")
    propose_gas=$(json_field "$data" "ProposeGasPrice")
    fast_gas=$(json_field "$data" "FastGasPrice")

    if [[ -n "$safe_gas" ]]; then
        printf "    🐢 Safe:     %s Gwei\n" "$safe_gas"
        printf "    🚗 Standard: %s Gwei\n" "$propose_gas"
        printf "    🚀 Fast:     %s Gwei\n" "$fast_gas"
        echo ""
        echo "  ── Estimated Transfer Costs ──"
        echo "    (21,000 gas units for ETH transfer)"
        if [[ -n "$safe_gas" ]]; then
            printf "    Safe:     %s ETH\n" "$(awk "BEGIN{printf \"%.6f\", $safe_gas * 21000 / 1000000000}")"
            printf "    Standard: %s ETH\n" "$(awk "BEGIN{printf \"%.6f\", $propose_gas * 21000 / 1000000000}")"
            printf "    Fast:     %s ETH\n" "$(awk "BEGIN{printf \"%.6f\", $fast_gas * 21000 / 1000000000}")"
        fi
    else
        echo "    Unable to fetch gas prices (API rate limit)"
        echo "    Try again in a moment"
    fi

    echo ""
    echo "  ── Bitcoin Fee Estimates ──"
    local btc_fees
    btc_fees=$(safe_curl "$BTC_API/fee-estimates" 2>/dev/null || echo "{}")
    local fee_1 fee_3 fee_6
    fee_1=$(echo "$btc_fees" | grep -oP '"1"\s*:\s*\K[0-9.]+' | head -1)
    fee_3=$(echo "$btc_fees" | grep -oP '"3"\s*:\s*\K[0-9.]+' | head -1)
    fee_6=$(echo "$btc_fees" | grep -oP '"6"\s*:\s*\K[0-9.]+' | head -1)
    if [[ -n "$fee_1" ]]; then
        printf "    Next block (~10min): %s sat/vB\n" "$fee_1"
        printf "    3 blocks  (~30min):  %s sat/vB\n" "${fee_3:-?}"
        printf "    6 blocks  (~60min):  %s sat/vB\n" "${fee_6:-?}"
        echo ""
        echo "    (Typical TX ~140 vBytes)"
        printf "    Fast estimate: ~%s sats (~%s)\n" \
            "$(awk "BEGIN{printf \"%.0f\", ${fee_1:-1} * 140}")" \
            "$(format_btc "$(awk "BEGIN{printf \"%.0f\", ${fee_1:-1} * 140}")")"
    else
        echo "    Unable to fetch fee estimates"
    fi
    echo ""
    print_footer
}

cmd_block() {
    local block_num="${1:-}"
    require_cmd curl
    print_header "Block Info${block_num:+ (#$block_num)}"
    log_history "block ${block_num:-latest}"
    echo ""

    if [[ -z "$block_num" ]]; then
        echo "  ── Latest Bitcoin Block ──"
        local height
        height=$(safe_curl "$BTC_API/blocks/tip/height" 2>/dev/null || echo "?")
        printf "    Current Height: %s\n" "$height"
        echo ""
        local hash
        hash=$(safe_curl "$BTC_API/blocks/tip/hash" 2>/dev/null || echo "?")
        printf "    Block Hash: %s\n" "$hash"
        echo ""

        if [[ "$hash" != "?" ]]; then
            local block_data
            block_data=$(safe_curl "$BTC_API/block/$hash" 2>/dev/null || echo "{}")
            local timestamp tx_count bsize weight
            timestamp=$(json_field "$block_data" "timestamp")
            tx_count=$(json_field "$block_data" "tx_count")
            bsize=$(json_field "$block_data" "size")
            weight=$(json_field "$block_data" "weight")

            if [[ -n "$timestamp" ]]; then
                printf "    Time:       %s\n" "$(date -d "@$timestamp" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "$timestamp")"
            fi
            printf "    TX Count:   %s\n" "${tx_count:-?}"
            printf "    Size:       %s bytes (%s KB)\n" "${bsize:-?}" "$(awk "BEGIN{printf \"%.1f\", ${bsize:-0}/1024}")"
            printf "    Weight:     %s WU\n" "${weight:-?}"
        fi
    else
        echo "  ── Bitcoin Block #$block_num ──"
        local hash
        hash=$(safe_curl "$BTC_API/block-height/$block_num" 2>/dev/null || echo "")
        if [[ -n "$hash" && "$hash" != "Block not found" ]]; then
            printf "    Hash: %s\n" "$hash"
            echo ""
            local block_data
            block_data=$(safe_curl "$BTC_API/block/$hash" 2>/dev/null || echo "{}")
            local timestamp tx_count bsize
            timestamp=$(json_field "$block_data" "timestamp")
            tx_count=$(json_field "$block_data" "tx_count")
            bsize=$(json_field "$block_data" "size")

            if [[ -n "$timestamp" ]]; then
                printf "    Time:     %s\n" "$(date -d "@$timestamp" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "$timestamp")"
            fi
            printf "    TX Count: %s\n" "${tx_count:-?}"
            printf "    Size:     %s bytes\n" "${bsize:-?}"
        else
            echo "    Block #$block_num not found"
        fi
    fi
    echo ""
    print_footer
}

cmd_token() {
    local addr="${1:-}"
    if [[ -z "$addr" ]]; then
        echo "Usage: $SCRIPT_NAME token <contract_address>" >&2
        exit 1
    fi
    require_cmd curl
    print_header "Token Info: ${addr:0:20}..."
    log_history "token $addr"
    echo ""

    if is_eth_address "$addr"; then
        echo "  Chain:    Ethereum"
        echo "  Contract: $addr"
        echo ""

        # Token supply
        local supply_data
        supply_data=$(safe_curl "${ETH_API}?module=stats&action=tokensupply&contractaddress=$addr" 2>/dev/null || echo "{}")
        local supply
        supply=$(json_field "$supply_data" "result")
        if [[ -n "$supply" && "$supply" =~ ^[0-9]+$ ]]; then
            printf "  Total Supply (raw): %s\n" "$supply"
            # Assume 18 decimals (most common)
            printf "  Total Supply (18d): %s\n" "$(awk "BEGIN{printf \"%.2f\", $supply / 1000000000000000000}")"
        else
            echo "  Supply: Unable to fetch (may need API key or invalid contract)"
        fi

        echo ""
        echo "  ── Contract Details ──"
        local src_data
        src_data=$(safe_curl "${ETH_API}?module=contract&action=getabi&address=$addr" 2>/dev/null || echo "{}")
        local abi_status
        abi_status=$(json_field "$src_data" "status")
        if [[ "$abi_status" == "1" ]]; then
            echo "    Contract: Verified ✓"
        else
            echo "    Contract: Not verified or proxy"
        fi

        echo ""
        echo "  ── Recent Token Transfers ──"
        local tx_data
        tx_data=$(safe_curl "${ETH_API}?module=account&action=tokentx&contractaddress=$addr&page=1&offset=5&sort=desc" 2>/dev/null || echo "{}")
        local tx_count
        tx_count=$(echo "$tx_data" | grep -c '"hash"' 2>/dev/null || echo "0")
        echo "    Recent transfers found: $tx_count"
        echo "$tx_data" | grep -oP '"hash"\s*:\s*"\K0x[a-f0-9]+' | head -5 | while read -r txhash; do
            echo "      $txhash"
        done
    else
        echo "  ⚠️  Token lookup requires an Ethereum contract address (0x...)"
    fi
    echo ""
    print_footer
}

cmd_help() {
    print_header "Help"
    cat <<EOF

  Usage: $SCRIPT_NAME <command> [args]

  Commands:
    address <addr>     Show address info (BTC or ETH)
    tx <hash>          Look up transaction details
    balance <addr>     Check address balance
    gas                Show current gas/fee estimates
    block [number]     Show block info (latest or specific)
    token <addr>       Look up ERC-20 token contract info

    help               Show this help message
    version            Print version

  Supported chains:
    Bitcoin  — addresses starting with 1, 3, or bc1
    Ethereum — addresses starting with 0x (40 hex chars)

  APIs used:
    BTC: blockstream.info (no key required)
    ETH: etherscan.io (free tier, rate limited)

  Examples:
    $SCRIPT_NAME balance 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
    $SCRIPT_NAME gas
    $SCRIPT_NAME block
    $SCRIPT_NAME block 800000
    $SCRIPT_NAME tx <txid>

EOF
    print_footer
}

cmd_version() {
    echo "$SCRIPT_NAME v$VERSION"
}

# ─── Main Dispatch ────────────────────────────────────────────────────
main() {
    local command="${1:-help}"
    shift 2>/dev/null || true

    case "$command" in
        address)        cmd_address "${1:-}" ;;
        tx)             cmd_tx "${1:-}" ;;
        balance)        cmd_balance "${1:-}" ;;
        gas)            cmd_gas ;;
        block)          cmd_block "${1:-}" ;;
        token)          cmd_token "${1:-}" ;;
        help|--help|-h) cmd_help ;;
        version|--version|-v) cmd_version ;;
        *)
            echo "Unknown command: $command" >&2
            echo "Run '$SCRIPT_NAME help' for usage." >&2
            exit 1
            ;;
    esac
}

main "$@"
