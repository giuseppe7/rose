# R.O.S.E.

ROSE stands for "Recursive organizational structure extractor" and was created as a personal project.

## Environment Setup

Use the following to prepare your local environment.

1. Ensure you have the latest `pip` installed.  
   ```
   python3 -m pip install --upgrade pip
   ```
1. Install `virtualenv` to avoid installing anything globally that may disrupt your other applications.  
   ```
   python3 -m pip install --user virtualenv
   python3 -m venv  ./venv 
   source ./venv/bin/activate
   ```
1. Run `pip` with the requirements file to locally install necessary modules.  
   ```
   pip install -r requirements.txt
   ```
1. Set up your required environment variables `ROSE_HOST`, `ROSE_PORT`, `ROSE_UNAME`, `ROSE_PWORD`, and `ROSE_SEARCH_BASE` for connectivity for the LDAP search.

## Usage

To use the python script, invoke it with a sAMAccountName to perform the organization printout. Use the `--help` option for additional options. 

```
$ ./rose.py example
John Hancock
    Jane Doe
    John Doe
```

## Contributions

Basic unit tests required. Currently linting is only done with `flake8`.


## References

See below for helpful sources.

1. https://ldap3.readthedocs.io/en/latest/index.html
1. https://www.viget.com/articles/two-ways-to-share-git-hooks-with-your-team/
