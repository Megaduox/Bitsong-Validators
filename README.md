# Bitsong Validators
This is sevice for Bitsong Validators. You can see how it works here 
[Bitsong.blockmachine.pro](https://bitsong.blockmachine.pro/)
## How to use
1. Use function add_to_database_many(record=get_validators_delegators()) in
the file get_delgators.py. You will get all validators, delgators and 
they will be added to database
2. Use function get_time_tokens_for_delegations(validators_delegators=get_validators_delegators(validators_with_valopers=True))
in the file get_delgators.py. You will get all delegators and add tokens, date to database.

## Functions
In file get_delegators.py.
### get_validators_PSSSlist()
Get list of all validators from Bitsong blockchain.
### get_validator_delegators(validator_valoper)
Through the cicle get all delegators by validators valoper.
Need one argument - validator valoper.
### add_to_database_one(address, validator_id)
Temporary function, not use anywhere. Get address, validator_id and add
to delegators table one row.
### get_mysql_id_by_valoper(valoper)
Return validator_id by valoper for one validator. Parameter - valoper.
### get_validators_delegators(validators_with_valopers=False)
One parameter - if False function return list without valopers, only Id's.
It needs for different use cases.
Functuion return all validators and theis delegators.
### add_to_database_many(record)
Argument record is list with data to export to database many rows.
### get_time_tokens_for_delegations(validators_delegators)
Function return list of all delegators tokens and dates when its delegation
was delegated. Get one argument - list of all validatros with their delegators.
