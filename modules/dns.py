#!/usr/bin/env python

# Copyright 2013, 2014 Philipp Winter <phw@nymity.ch>
#
# This file is part of exitmap.
#
# exitmap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# exitmap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with exitmap.  If not, see <http://www.gnu.org/licenses/>.

"""
Module to detect malfunctioning DNS resolution.
"""

import log
import const
import mysocks

logger = log.getLogger()

destinations = None

def resolve( exitFpr, domain, whitelist ):
    """
    Resolve a `domain' and compare it to the `whitelist'.

    If the domain is not part of the whitelist, an error is logged.
    """

    sock = mysocks.socksocket()
    sock.setproxy(mysocks.PROXY_TYPE_SOCKS5, "127.0.0.1", const.TOR_SOCKS_PORT)
    # Resolve the domain using Tor's SOCKS extension.
    ipv4 = sock.resolve(domain)

    if ipv4 not in whitelist:
        logger.error("Exit relay %s returned unexpected IPv4 address for " \
                     "\"%s\": %s." % (exitFpr, domain, ipv4))
    else:
        logger.info("IPv4 address of \"%s\" as expected for %s." %
                    (domain, exitFpr))

def probe( exitFpr, cmd ):
    """
    Probe the given exit relay and check if the domains resolve as expected.
    """

    # Format: <domain> : <ipv4_addresses>
    domains = {
        "youporn.com" : ["31.192.116.24"],
        "www.torproject.org" : ["38.229.72.14", "93.95.227.222", "86.59.30.40",
                                "38.229.72.16", "82.195.75.101"],
        "www.wikileaks.org" : ["95.211.113.131", "95.211.113.154"]
    }

    for domain in domains.iterkeys():
        resolve(exitFpr, domain, domains[domain])
