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

import sys
import argparse

from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client import client
from httplib2 import Http
from apiclient.discovery import build


#The unique client email address that was created from the creating a Service Account within the Google Developer Console
client_email = "[Your Client Email]@developer.gserviceaccount.com"

#Process commmand line arguments
argparser = argparse.ArgumentParser(add_help=False)

argparser.add_argument(
    'merchant_id',
    help='The ID of the merchant center.')

argparser.add_argument(
  'product_id',
  help='The ID of the product to get.')

args = argparser.parse_args()

merchant_id = args.merchant_id
product_id = args.product_id


try:    
    #Read in the private key.  PEM key created from Developer Console P12 key using Open SSL.
    #P12 key doesn't seem to be supported by PyCrypto 2.6.1, need to swith to PEM key.
    with open("[Your PEM Key].pem") as f:
        private_key = f.read()


    #Create a SignedJwtAssertionCredentials object passing in the client email, private key, and API scope
    credentials = SignedJwtAssertionCredentials(
        client_email,
        private_key,
        "https://www.googleapis.com/auth/content")


    #authorize an Http instance
    http_auth = credentials.authorize(Http())


    #build a service object for the Content API For Shopping (version 2) and pass in an authorized Http object.
    contentService = build("content",
                           "v2",
                            http=http_auth)

    #Setup the request for the products().get method
    request = contentService.products().get(merchantId=merchant_id, productId="online:en:US:"+product_id)

    #make the call to the API
    result = request.execute()

    print "----------"
          
    #print the product ID
    print "Product ID: %s" % result['id']

    #retrieve and print the price
    price = result['price']
    print "Product Price: %s" %  price['value']
                    
    #print the title of the product
    print "Product Title: %s" % result['title']

    #print the stock avaiability of the product
    print "Product Stock Availability: %s" % result['availability']

except client.AccessTokenRefreshError:
    print ("There was an error obtaining the access or refresh token for " + client_email)

