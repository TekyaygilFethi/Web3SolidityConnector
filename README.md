# Web3 Solidity Connector


With this project, you can compile your sol files and create new transactions including creating contract and calling the state changer functions. You can integrate integrate your sol files with Python and you can call functions with using Python.

# Program Life Cycle

1. Compile the Solidity(.sol) file
2. Deploy the contract which is in Solidity file
3. Manipulate the main.py file for calling and executing relevant functions in contract even with parameters via the help of Web3


# Folder Structure

To assure the program is working, there are folder structure rules to follow. 

1. This projects points to sol_files folder for your Solidity files. This means sol_files folder must contain your .sol extensioned files. You should select one of the sol file in this directory to be compiled.

2. After you execute compile.py, "compilation_files_out" folder will be created which contains your output files. "compiled_abi.json" and "compiled_bytecode.txt" files should not be deleted or overwritten! You can examine your compiled code in "compiled_code.json" file.

3. global_variables.py file contains your default paths for compilation files and the sol files that will be compiled. You can change this structure any way you want.
```python
GLOBAL_COMPILATION_PATH = "./compilation_files_out"  # folder that contains output files
GLOBAL_SOL_PATH = "./sol_files"  # folder that contains sol file
```


# Running the Program

1. Clone the repository

```bash
git clone https://github.com/TekyaygilFethi/ContractDeploment.git
```

2. Create an .env file on current folder that contains your address(with MY_ADDRESS key), private key(with PRIVATE_KEY key), rinkeby rpc url(with RINKEBY_RPC_URL key) and chain id(with CHAIN_ID key) values. Your .env file should look like this:

```python
PRIVATE_KEY ="0x{YOUR PRIVATE KEY}"
RINKEBY_RPC_URL = "{YOUR RINKEBY RPC URL}"
MY_ADDRESS = "{YOUR ADDRESS}"
CHAIN_ID = "{YOUR CHAIN ID}"
```

3. Install the dependencies from requirements.txt file.
```bash
pip install -r requirements.txt
```
4. After setting the .env file, to run the program, you first need to go to the project directory and run:

```bash
python compile.py {YOUR_SOL_FILE} // python compile.py SimpleContract.sol
```
! Please note that your sol files must be in the folder `sol_files` folder by default or in the folder you specified custom in `global_variables.py` file by assigning to `GLOBAL_SOL_PATH`.

5. After compilation you should see screen like this:
```bash
Compilation folder created!
Compiled successfully!
```

6. When you check your folders, you can see `compilation_files_out` folder is created. If you changed the folder path and name from global_variables you may see different folder. This folder be based on when deploying your contracts and running your Solidity functions!

7. For next step, you must deploy your compiled contract. To do this, you must run:

```bash
python deploy.py
```
This command will creates a transaction for contract creation based on your compiled Solidity file. This command will output the success message, transaction receipt and contract address. To use this deployed contract and it's functions, you must copy the address of this deployed contract. You should see response like this (Please note that receipt and address may differ)
```bash
New Contract Transaction has been created!

AttributeDict({'transactionHash': HexBytes('0x19f1237cd0bf13bf1112f7e60b9dd7570dcca38c18718368e09c462e01482272'), 'transactionIndex': 0, 'blockHash': HexBytes('0xa47912b38dec2fdecfed283da5fd6a7d778def3f62bc2c629373903cbd5f59bc'), 'blockNumber': 34, 'from': '0x2DAc2487DD401D9E5C757eb03B8928b70FFaFe6e', 'to': None, 'gasUsed': 640222, 'cumulativeGasUsed': 640222, 'contractAddress': '0x874E06Aff5a1031Bd5AE07100A7A518D0C72b8E2', 'logs': [], 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})

Contract Address: 0x874E06Aff5a1031Bd5AE07100A7A518D0C72b8E2 //This address you should copy.
```

8. Edit your main.py content according to your functions. For example, I have addHero function in my compiled Solidity:
```c
struct Hero {
    string name;
    string lightsaberColor;
    uint256 age;
}

Hero[] heroes;

function addHero(
        string memory _name,
        string memory _lightsaberColor,
        uint256 _age
    ) public {
        heroes.push(Hero(_name, _lightsaberColor, _age));
        uint256 idx = heroes.length - 1;
        nameToIndex[_name] = idx;
    }
```
 You can call this function from my main.py file with parameters like this: 

```python
# write functions with their parameters if any after this line inside of executeContractFunction method.
contractOps.executeContractFunction(
    # write your contract functions as contract.functions.{your function}, your private key
    contract.functions.addHero("Obi-Wan Kenobi", "Blue", 29),
    private_key,
)
```

Here, `contractOps` is an object that allows you to perform contract operations such as creating, deploying, gathering contracts or executing a function inside a contract. And `executeContractFunction` is a special function that allow you to execute a functions. It creates, signs, sends and gets the receipt for transaction automatically.

- If you have a function that is not changing a state in Solidity file you also can call it. For example here's the function that is not changing state in my Solidity file:
```c
function getInfoByName(string memory name)
        public
        view
        returns (Hero memory)
    {
        uint256 idx = nameToIndex[name];
        return heroes[idx];
    }

function getAllHeroes() public view returns (Hero[] memory) {
        return heroes;
    }
```
You can call the `getAllHeroes` function like this:
```python
print(contract.functions.getAllHeroes().call())
```

You can call the `getInfoByName` function which takes parameter like this:
```python
print(contract.functions.getInfoByName("Obi-Wan Kenobi").call())
```
Please note that we had to use `.call()` at the end of the function call to gather response and make the function call.


9. To run main.py file, you need to supply contract address. You should use the contracty address you copied at Step 6.
```bash
python main.py {ContractAddress}
```
Here is an example:

```bash
python main.py 0x874E06Aff5a1031Bd5AE07100A7A518D0C72b8E2
```

And you can see the results when you execute this command:
![Result](https://res.cloudinary.com/dpzdg2rik/image/upload/v1644060134/samples/WebPy3%20Solidity%20Connector/Result.png)

And you're done! Congratulations!
