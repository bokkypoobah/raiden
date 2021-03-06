from eth_utils import denoms, to_hex

from raiden.constants import Environment

INITIAL_PORT = 38647

CACHE_TTL = 60
GAS_LIMIT = 10 * 10**6
GAS_LIMIT_HEX = to_hex(GAS_LIMIT)
GAS_PRICE = denoms.shannon * 20  # pylint: disable=no-member

DEFAULT_TRANSPORT_RETRIES_BEFORE_BACKOFF = 5
DEFAULT_TRANSPORT_THROTTLE_CAPACITY = 10.
DEFAULT_TRANSPORT_THROTTLE_FILL_RATE = 10.
DEFAULT_TRANSPORT_UDP_RETRY_INTERVAL = 1.
# matrix gets spammed with the default retry-interval of 1s, wait a little more
DEFAULT_TRANSPORT_MATRIX_RETRY_INTERVAL = 5.
DEFAULT_MATRIX_KNOWN_SERVERS = {
    Environment.PRODUCTION: (
        "https://raw.githubusercontent.com/raiden-network/raiden-transport"
        "/master/known_servers.main.yaml"
    ),
    Environment.DEVELOPMENT: (
        "https://raw.githubusercontent.com/raiden-network/raiden-transport"
        "/master/known_servers.test.yaml"
    ),
}

DEFAULT_REVEAL_TIMEOUT = 50
DEFAULT_SETTLE_TIMEOUT = 500
DEFAULT_RETRY_TIMEOUT = 0.5
DEFAULT_JOINABLE_FUNDS_TARGET = 0.4
DEFAULT_INITIAL_CHANNEL_TARGET = 3
DEFAULT_WAIT_FOR_SETTLE = True
DEFAULT_NUMBER_OF_BLOCK_CONFIRMATIONS = 5
DEFAULT_WAIT_BEFORE_LOCK_REMOVAL = 2 * DEFAULT_NUMBER_OF_BLOCK_CONFIRMATIONS
DEFAULT_CHANNEL_SYNC_TIMEOUT = 5

DEFAULT_NAT_KEEPALIVE_RETRIES = 5
DEFAULT_NAT_KEEPALIVE_TIMEOUT = 5
DEFAULT_NAT_INVITATION_TIMEOUT = 15

DEFAULT_SHUTDOWN_TIMEOUT = 2

ORACLE_BLOCKNUMBER_DRIFT_TOLERANCE = 3
ETHERSCAN_API = 'https://{network}.etherscan.io/api?module=proxy&action={action}'
