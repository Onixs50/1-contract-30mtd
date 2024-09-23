import json
import os
import random
import time
import subprocess
from web3 import Web3
from solcx import compile_standard, install_solc
from termcolor import colored

# Install the required Solidity version
install_solc('0.8.0')

# Clear the terminal screen
def clear_screen():
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

# Print a large boxed message
def print_boxed_message(message, color='cyan'):
    box_width = len(message) + 4
    print(colored("+" + "-" * box_width + "+", color))
    print(colored("| " + message + " |", color))
    print(colored("+" + "-" * box_width + "+", color))

# Manage network information
def manage_network_info():
    if os.path.exists('network_info.json'):
        with open('network_info.json', 'r') as f:
            networks = json.load(f)
    else:
        networks = {}

    print(colored("Available networks:", 'yellow'))
    for i, (chain_id, network) in enumerate(networks.items(), 1):
        print(colored(f"{i}. RPC: {network['rpc']}", 'cyan'))

    while True:
        choice = input(colored("Enter the number to select a network, or 'a' to add a new one: ", 'green'))
        if choice.lower() == 'a':
            chain_id = input(colored("Enter the new chain ID: ", 'yellow'))
            rpc_url = input(colored("Enter the RPC URL: ", 'yellow'))
            explorer_url = input(colored("Enter the Explorer URL: ", 'yellow'))
            networks[chain_id] = {
                "rpc": rpc_url,
                "explorer": explorer_url
            }
            with open('network_info.json', 'w') as f:
                json.dump(networks, f)
            print(colored(f"Network with Chain ID {chain_id} added successfully.", 'green'))
        elif choice.isdigit() and 1 <= int(choice) <= len(networks):
            return list(networks.values())[int(choice) - 1], list(networks.keys())[int(choice) - 1]
        else:
            print(colored("Invalid choice. Please try again.", 'red'))

# Manage private keys
def manage_private_keys():
    if os.path.exists('private_keys.txt'):
        with open('private_keys.txt', 'r') as f:
            private_keys = [key.strip() for key in f.readlines()]
    else:
        private_keys = []

    if not private_keys:
        new_key = input(colored("Enter your private key: ", 'yellow'))
        private_keys.append(new_key)
        with open('private_keys.txt', 'w') as f:
            f.writelines([key + '\n' for key in private_keys])

    return private_keys

# Get gas settings from user
def get_gas_settings(web3):
    current_gas_price = web3.eth.gas_price
    current_gas_limit = 21000  # Minimum gas limit for a simple transaction

    print(colored(f"Current gas settings:", 'yellow'))
    print(colored(f"Gas Price: {web3.from_wei(current_gas_price, 'gwei'):.2f} Gwei", 'cyan'))
    print(colored(f"Gas Limit: {current_gas_limit}", 'cyan'))

    use_current = input(colored("Do you want to use these gas settings? (y/n): ", 'green')).lower() == 'y'
    
    if not use_current:
        gas_price = web3.to_wei(float(input(colored("Enter new gas price (in Gwei): ", 'yellow'))), 'gwei')
        gas_limit = int(input(colored("Enter new gas limit: ", 'yellow')))
    else:
        gas_price = current_gas_price
        gas_limit = current_gas_limit

    return gas_price, gas_limit

# Deploy contract
def deploy_contract(web3, private_key, explorer_url):
    with open('AdvancedInteraction.sol', 'r') as f:
        contract_source = f.read()

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "AdvancedInteraction.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["*"]
                }
            }
        }
    })

    contract_interface = compiled_sol['contracts']['AdvancedInteraction.sol']['AdvancedInteraction']
    bytecode = contract_interface['evm']['bytecode']['object']
    abi = contract_interface['abi']

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)

    # Estimate gas
    estimated_gas = web3.eth.estimate_gas({
        'from': account.address,
        'data': bytecode
    })

    # Get current gas price
    gas_price = web3.eth.gas_price
    
    tx = contract.constructor().build_transaction({
        'chainId': web3.eth.chain_id,
        'gas': estimated_gas,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_tx = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(colored(f"Contract deployed at address: {tx_receipt.contractAddress}", 'green'))
    print(colored(f"View on explorer: {explorer_url}/address/{tx_receipt.contractAddress}", 'cyan'))
    return tx_receipt.contractAddress, abi

def interact_with_contract(web3, contract_address, abi, private_key, interaction_count, min_delay, max_delay, explorer_url):
    contract = web3.eth.contract(address=contract_address, abi=abi)
    account = web3.eth.account.from_key(private_key)

    interaction_methods = [
        contract.functions.setValue,
        contract.functions.getValue,
        contract.functions.incrementValue,
        contract.functions.decrementValue,
        contract.functions.resetValue,
        contract.functions.isGreaterThan,
        contract.functions.saveHistory,
        contract.functions.getHistory,
        contract.functions.resetHistory,
        contract.functions.historyCount,
        contract.functions.multiplyValue,
        contract.functions.divideValue,
        contract.functions.isEven,
        contract.functions.isOdd,
        contract.functions.updateHistory,
        contract.functions.removeHistory,
        contract.functions.getMaxHistoryValue,
        contract.functions.getMinHistoryValue,
        contract.functions.getSumHistory,
        contract.functions.getAverageHistory,
        contract.functions.setUserValue,
        contract.functions.getUserValue,
        contract.functions.incrementUserValue,
        contract.functions.decrementUserValue,
        contract.functions.transferUserValue,
        contract.functions.getContractBalance,
        contract.functions.donate,
        contract.functions.withdraw,
        contract.functions.getTimestamp,
        contract.functions.getBlockNumber
    ]

    confirmed = 0
    failed = 0

    for _ in range(interaction_count):
        method = random.choice(interaction_methods)
        print(colored(f"Interacting with method: {method.fn_name}", 'yellow'))

        try:
            # Estimate gas and get current gas price for each transaction
            if method.fn_name in ['setValue', 'isGreaterThan', 'multiplyValue', 'divideValue', 'updateHistory', 'setUserValue', 'transferUserValue', 'withdraw']:
                value = random.randint(1, 100)
                estimated_gas = method(value).estimate_gas({'from': account.address})
                tx = method(value).build_transaction({
                    'chainId': web3.eth.chain_id,
                    'gas': estimated_gas,
                    'gasPrice': web3.eth.gas_price,
                    'nonce': web3.eth.get_transaction_count(account.address),
                })
            elif method.fn_name == 'donate':
                estimated_gas = method().estimate_gas({'from': account.address, 'value': web3.to_wei(0.001, 'ether')})
                tx = method().build_transaction({
                    'chainId': web3.eth.chain_id,
                    'gas': estimated_gas,
                    'gasPrice': web3.eth.gas_price,
                    'nonce': web3.eth.get_transaction_count(account.address),
                    'value': web3.to_wei(0.001, 'ether')
                })
            else:
                estimated_gas = method().estimate_gas({'from': account.address})
                tx = method().build_transaction({
                    'chainId': web3.eth.chain_id,
                    'gas': estimated_gas,
                    'gasPrice': web3.eth.gas_price,
                    'nonce': web3.eth.get_transaction_count(account.address),
                })

            signed_tx = account.sign_transaction(tx)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            confirmed += 1
            print(colored(f"Transaction confirmed: {tx_hash.hex()}", 'green'))
            print(colored(f"View on explorer: {explorer_url}/tx/{tx_hash.hex()}", 'cyan'))
        except Exception as e:
            failed += 1
            print(colored(f"Transaction failed: {str(e)}", 'red'))

        delay = random.uniform(min_delay, max_delay)
        print(colored(f"Waiting for {delay:.2f} seconds before next interaction...", 'yellow'))
        time.sleep(delay)

    return confirmed, failed

def main():
    clear_screen()
    print_boxed_message("Coded by onixia", 'yellow')

    network, chain_id = manage_network_info()
    rpc_url = network["rpc"]
    explorer_url = network["explorer"]
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    if not web3.is_connected():
        print(colored("Failed to connect to the network. Please check your RPC URL.", 'red'))
        return

    private_keys = manage_private_keys()

    interaction_count = int(input(colored("Enter the number of interactions to perform per wallet: ", 'yellow')))
    min_delay = float(input(colored("Enter the minimum delay between interactions (in seconds): ", 'yellow')))
    max_delay = float(input(colored("Enter the maximum delay between interactions (in seconds): ", 'yellow')))

    total_confirmed = 0
    total_failed = 0

    for private_key in private_keys:
        clear_screen()
        account = web3.eth.account.from_key(private_key)
        print_boxed_message(f"Processing wallet: {account.address}", 'cyan')
        
        # Deploy a new contract for each wallet
        contract_address, abi = deploy_contract(web3, private_key, explorer_url)
        
        # Interact with the newly deployed contract
        confirmed, failed = interact_with_contract(web3, contract_address, abi, private_key, interaction_count, min_delay, max_delay, explorer_url)
        total_confirmed += confirmed
        total_failed += failed

    print_boxed_message("Summary Report", 'green')
    print(colored(f"Total confirmed interactions: {total_confirmed}", 'cyan'))
    print(colored(f"Total failed interactions: {total_failed}", 'cyan'))
    print_boxed_message("Coded by onixia", 'yellow')

if __name__ == "__main__":
    main()
