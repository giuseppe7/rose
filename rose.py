#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:
 rose <sAMAccountName> [--detailed] [--directsonly]

Options:
  -h --help      Show this screen.
  --version      Show version.
  --detailed     Include additional details in output.
  --directsonly  Only list the target and their current directs.
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

SEARCH_ATTRS = [
    'distinguishedName', 'sAMAccountName', 'userPrincipalName',
    'objectClass', 'objectCategory',
    'cn', 'name', 'title', 'mail', 'department', 'directReports', 'manager']
#SEARCH_ATTRS = ['*']


# Functions ..................................................................


def get_person_dn(conn, basedn, sAMAccountName):
    '''
    Returns the person's DN given the connection, basedn, and sAMAccountName
    '''
    results = conn.search(
        basedn,
        "(&(objectClass=person)(sAMAccountName={}))".format(sAMAccountName),
        attributes=SEARCH_ATTRS)

    if results:
        if len(conn.entries) > 1:
            # Only expect one result.
            raise Exception('Found more than one result.')
        return conn.entries[0]
    else:
        raise Exception("No results found.")


def print_person(conn, basedn, targetdn, prefix, detailed):
    #print(targetdn)
    #return
    if detailed is True:
        print('{}"{}", "{}", "{}", "{}"'.format(
            prefix, targetdn.name,
            targetdn.userPrincipalName,
            targetdn.mail,
            targetdn.title,
            ))
    else:
        print('{}{}'.format(prefix, targetdn.name))
    return


def print_person_and_directs(
        conn, basedn, targetdn, prefix,
        detailed=False, directs_only=False):

    print_person(conn, basedn, targetdn, prefix, detailed)
    if 'directReports' not in targetdn:
        return

    new_prefix = prefix + '    '
    for directReport in sorted(targetdn.directReports.values):
        matches = ["DisabledAccounts", "Disabled Users"]
        if any(x in directReport for x in matches):
            # TODO: Seems like something that wont be the same for everyone.
            continue

        results = conn.search(
            search_base=directReport,
            search_filter="(objectClass=*)",
            search_scope=ldap3.BASE,
            attributes=SEARCH_ATTRS)
        if not results:
            continue  # No results for this direct, continue with the list.

        if directs_only:
            print_person(conn, basedn, conn.entries[0], new_prefix, detailed)
        else:
            print_person_and_directs(
                conn, basedn, conn.entries[0], new_prefix,
                detailed, directs_only)


# Main .......................................................................


def main():
    '''
    Convenient main method.
    '''
    try:
        file_path = os.path.dirname(os.path.realpath(__file__))
        f = open('{}/build_number'.format(file_path), 'r')
        build_number = f.read().strip()
    except Exception:
        build_number = 0

    arguments = docopt(__doc__, version='ROSE v{}'.format(build_number))
    target_person = arguments['<sAMAccountName>']
    detailed = arguments['--detailed']
    directs_only = arguments['--directsonly']

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
            get_info=ldap3.NONE)

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
        print("LDAP exception occurred:", err)
        sys.exit(1)
    except Exception as err:
        print("Exception occurred:", err)
        sys.exit(1)

    # Perform a basic search to obtain the DN of the given person.
    try:
        dn = get_person_dn(c, target_search_base, target_person)
        print_person_and_directs(
            c, target_search_base, dn, "", detailed, directs_only)

    except Exception as err:
        print(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())
