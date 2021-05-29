#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:
 rose <person>
"""

from docopt import docopt
import os
import ldap3
from ldap3.core.exceptions \
    import LDAPBindError, LDAPPasswordIsMandatoryError, LDAPSocketOpenError
import ssl
import sys


# Constants ..................................................................

ENV_HOST = 'ROSE_HOST'
ENV_PORT = 'ROSE_PORT'
ENV_UNAME = 'ROSE_UNAME'
ENV_PWORD = 'ROSE_PWORD'
ENV_SEARCH_BASE = 'ROSE_SEARCH_BASE'

# Functions ..................................................................

# Main .......................................................................


def main():
    '''
    Convenient main method.
    '''
    arguments = docopt(__doc__)
    target_person = arguments["<person>"]

    # Pull in host, port information from the environment variables.
    if ENV_HOST not in os.environ or ENV_PORT not in os.environ:
        print('Please set {} and {} in the env.'.format(ENV_HOST, ENV_PORT))
        sys.exit(1)
    if ENV_UNAME not in os.environ or ENV_PWORD not in os.environ:
        print('Please set {} and {} in the env.'.format(ENV_UNAME, ENV_PWORD))
        sys.exit(1)
    if ENV_SEARCH_BASE not in os.environ:
        print('Please set {} in the env.'.format(ENV_SEARCH_BASE))
        sys.exit(1)

    # Assign environment variables.
    target_host = os.getenv(ENV_HOST).strip()
    target_port = int(os.getenv(ENV_PORT))
    target_search_base = os.getenv(ENV_SEARCH_BASE).strip()
    target_uname = os.getenv(ENV_UNAME).strip()
    target_pword = os.getenv(ENV_PWORD).strip()

    # Check connectivity to the target LDAP server.
    try:
        tls_config = ldap3.Tls(
            validate=ssl.CERT_REQUIRED,
            version=ssl.PROTOCOL_TLSv1)

        s = ldap3.Server(
            target_host,
            port=target_port,
            use_ssl=True,
            tls=tls_config,
            get_info=ldap3.ALL)

        c = ldap3.Connection(
                s,
                user=target_uname,
                password=target_pword,
                auto_bind=True,
                read_only=True)

        c.start_tls()
        c.bind()

    except TypeError as err:
        print(err)
        sys.exit(1)
    except (LDAPBindError,
            LDAPPasswordIsMandatoryError, LDAPSocketOpenError) as err:
        print(err)
        sys.exit(1)
    except Exception as err:
        print(err)
        sys.exit(1)

    # Perform a basic search for now.
    try:
        search_attrs = [
            'sAMAccountName', 'cn', 'name', 'title', 'mail',
            'department', 'directReports', 'manager']
        # search_attrs=['*']

        results = c.search(
            target_search_base,
            "(&(objectClass=person)(sAMAccountName={}))".format(target_person),
            attributes=search_attrs)

        if results:
            for e in c.entries:
                print(e)

    except Exception as err:
        print(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())
