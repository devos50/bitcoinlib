# -*- coding: utf-8 -*-
#
#    bitcoinlib - Compact Python Bitcoin Library
#    Block Explorer Client
#    © 2016 November - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from bitcoinlib.services.baseclient import BaseClient

PROVIDERNAME = 'blockexplorer'


class BlockExplorerClient(BaseClient):

    def __init__(self, network):
        super(self.__class__, self).__init__(network, PROVIDERNAME)

    def compose_request(self, category, data, method='', variables=None):
        url_path = category + '/' + data + '/' + method
        return self.request(url_path, variables)

    def utxos(self, addresslist):
        addresses = ','.join(addresslist)
        res = self.compose_request('addrs', addresses, 'utxo')
        utxos = []
        for utxo in res:
            utxos.append({
                'address': utxo['address'],
                'tx_hash': utxo['txid'],
                'confirmations': utxo['confirmations'],
                'output_n': utxo['vout'],
                'index': 0,
                'value': utxo['amount'],
                'script': utxo['scriptPubKey'],
            })
        return utxos

    def getbalance(self, addresslist):
        utxos = self.utxos(addresslist)
        balance = 0
        for utxo in utxos:
            balance += utxo['value']
        return balance * self.units