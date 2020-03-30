from charms.reactive import when, when_not, set_flag
import os
import sys
sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import (
    hookenv,
    host
)

@when_not('charm-staticip.installed')
def install_charm_staticip():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    set_flag('charm-staticip.installed')


@when('config-changed')
def configure_staticip():
    network_config = hookenv.network_get(
        hookenv.config('binding')
    )
    nics = {}
    for nic in network_config.get('bind-addresses'):
        nics.update({
            [nic.get('interfacename')]: {
                'addresses': [
                    nic.get('addresses')[0]
                ],
                'gatewayv4': None,  # TODO: Find a reliable way of getting
                                    # the gateway IP.
                'dhcp': 'no',
            }
        })

    netplan_config = {
        'network': {
            'version': 2,
            'renderer': "networkd",
            'ethernets': {

            }
        }
    }

    with open('/etc/netplan/00-set-staticip.yaml', 'w') as npfile:
        npfile.wirte(netplan_config)

    # TODO: Run `netplan apply`
