# R.O.S.E.

ROSE stands for "Recursive organizational structure extractor" and was created as a personal project. It connects to LDAP to extract user information including manager information to construct a tree.

## Running the CLI Application

There are now two methods to invoke this application: a docker container that encapsulates the necessary prerequisites and the simple Python application using the same steps to build on your host machine.

### Docker Container Version

Use the following to prepare your local environment.

1. Set up these required environment variables for connectivity for LDAP search.
    * `ROSE_HOST`
    * `ROSE_PORT`
    * `ROSE_UNAME`
    * `ROSE_PWORD`
    * `ROSE_SEARCH_BASE` 
1. Copy any public certicates from any certifcate authority you require into the `certs/` folder.
1. Build the local container by executing the `make` command.

Once built, run the Docker command line specifying the aforementioned necessary environment variables.
```
$ docker run \
    -e ROSE_HOST -e ROSE_PORT \
    -e ROSE_UNAME -e ROSE_PWORD \
    -e ROSE_SEARCH_BASE \
    giuseppe7/rose --directs jhancock

John Hancock
    Jane Doe
    John Doe
```


### Stand-alone Python

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
1. Set up these required environment variables for connectivity for the LDAP search.
    * `ROSE_HOST`
    * `ROSE_PORT`
    * `ROSE_UNAME`
    * `ROSE_PWORD`
    * `ROSE_SEARCH_BASE` 

To use the python script, invoke it with a sAMAccountName to perform the organization printout. Use the `--help` option for additional options. 

```
$ ./rose.py jhancock
John Hancock
    Jane Doe
    John Doe
```

Basic unit tests required. Currently linting is only done with `flake8`.


---

## References

See below for helpful sources.

1. https://ldap3.readthedocs.io/en/latest/index.html
1. https://www.viget.com/articles/two-ways-to-share-git-hooks-with-your-team/
