import json
import pytest
import pexpect
import sys
from click.testing import CliRunner
from raiden.ui.cli import run
from eth_utils import to_checksum_address


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(run, ["version"])
    assert result.exit_code == 0
    result_json = json.loads(result.output)
    result_expected_keys = ["raiden", "python_implementation", "python_version", "system"]
    for expected_key in result_expected_keys:
        assert expected_key in result_json


@pytest.mark.timeout(25)
def test_cli_full_init(cli_args):
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect('Welcome to Raiden')
        child.expect('The following accounts were found in your machine:')
        child.expect('Select one of them by index to continue: ')
        child.sendline('0')
        child.expect('You are connected')
        child.expect('The Raiden API RPC server is now running')
    except pexpect.TIMEOUT as e:
        print("Timed out at", e)
    finally:
        child.close()


@pytest.mark.timeout(25)
@pytest.mark.parametrize('changed_args', [{'keystore_path': '.'}])
def test_cli_wrong_keystore_path(cli_args):
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect('No Ethereum accounts found in the provided keystore directory')
    except pexpect.TIMEOUT as e:
        print("PEXPECT timed out at", e)
    finally:
        child.close()


@pytest.mark.timeout(25)
@pytest.mark.parametrize('removed_args', [['password_file']])
def test_cli_missing_password_file_enter_password(blockchain_provider, cli_args):
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect('Welcome to Raiden')
        child.expect('The following accounts were found in your machine:')
        child.expect('Select one of them by index to continue: ')
        child.sendline('0')
        child.expect('Enter the password to unlock')
        with open(blockchain_provider['password_file'], 'r') as password_file:
            password = password_file.readline()
            child.sendline(password)
        child.expect('You are connected')
        child.expect('The Raiden API RPC server is now running')
    except pexpect.TIMEOUT as e:
        print("Timed out at", e)
    finally:
        child.close()


@pytest.mark.timeout(25)
@pytest.mark.parametrize('removed_args', [['data_dir']])
def test_cli_missing_data_dir(cli_args):
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect('Welcome to Raiden')
        child.expect('The following accounts were found in your machine:')
        child.expect('Select one of them by index to continue: ')
        child.sendline('0')
        child.expect('You are connected')
        child.expect('The Raiden API RPC server is now running')
    except pexpect.TIMEOUT as e:
        print("Timed out at", e)
    finally:
        child.close()


@pytest.mark.timeout(25)
@pytest.mark.parametrize('changed_args', [{'eth_rpc_endpoint': 'http://8.8.8.8:2020'}])
def test_cli_wrong_rpc_endpoint(cli_args):
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect('Welcome to Raiden')
        child.expect('The following accounts were found in your machine:')
        child.expect('Select one of them by index to continue: ')
        child.sendline('0')
        child.expect('Could not contact the ethereum node through JSON-RPC')
    except pexpect.TIMEOUT as e:
        print("Timed out at", e)
    finally:
        child.close()


@pytest.mark.timeout(25)
@pytest.mark.parametrize('changed_args', [{'network_id': '1'}])
def test_cli_wrong_network_id_try_mainnet(cli_args):
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect('Welcome to Raiden')
        child.expect('The following accounts were found in your machine:')
        child.expect('Select one of them by index to continue: ')
        child.sendline('0')
        child.expect(
            "The chosen ethereum network 'mainnet' differs from the ethereum "
            "client 'smoketest'")
    except pexpect.TIMEOUT as e:
        print('Timed out at', e)
    finally:
        child.close()


@pytest.mark.timeout(25)
@pytest.mark.parametrize('changed_args', [{
    'registry_contract_address': '0xdfD10vAe9CCl5EBf11bc6309A0645eFe9f979584',
}])
def test_cli_malformed_registry_address(cli_args):
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect(
            'Error: Invalid value for "--registry-contract-address"'
            ': Address must be EIP55 checksummed',
        )
    except pexpect.TIMEOUT as e:
        print("Timed out at", e)
    finally:
        child.close()


@pytest.mark.timeout(25)
@pytest.mark.parametrize('changed_args', [{
    'registry_contract_address': to_checksum_address('0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'),
}])
def test_cli_registry_address_without_deployed_contract(cli_args):
    # TODO: Change the expectation for this (don't expect a trace) when
    # https://github.com/raiden-network/raiden/issues/1996 is implemented
    child = pexpect.spawn('raiden', cli_args, logfile=sys.stdout)
    try:
        child.expect('Welcome to Raiden')
        child.expect('The following accounts were found in your machine:')
        child.expect('Select one of them by index to continue: ')
        child.sendline('0')
        child.expect('You are connected')
        child.expect('raiden.exceptions.AddressWithoutCode')
    except pexpect.TIMEOUT as e:
        print("Timed out at", e)
    finally:
        child.close()