#!/usr/bin/python
#
# Copyright 2014 David Tzau. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Get a single product from a specified Google Merchant Center account and a product ID"""

import argparse
import sys

from apiclient import sample_tools
from oauth2client import client


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)


argparser.add_argument(
    'merchant_id',
    help='The ID of the merchant center.')

argparser.add_argument(
  'product_id',
  help='The ID of the product to get.')


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'content', 'v2', __doc__, __file__, parents=[argparser])

  #grab the command line paramaters for Merchant ID, and the product ID
  merchant_id = flags.merchant_id
  product_id = flags.product_id

  try:
   
    request = service.products().get(merchantId=merchant_id, productId="online:en:US:" + product_id)
    result = request.execute()
    
    #print some product attribute information

    #print the product ID
    print "Product ID: " + result['id']

    #retrieve and print the price
    price = result['price']
    print "Product Price: " + price['value']

    #print the title of the product
    print "Product Title: " + result['title']

    #print the stock avaiability of the product
    print "Product Stock Availability:" + result['availability']   

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)