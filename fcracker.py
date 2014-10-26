#!/usr/bin/python3
# fcracker.py - multi forum password cracker
# 10/26/14

import argparse
import datetime
import hashlib
import sys

# crack multiple hashes, loop through both dictionary list and hash list
def multi_crack_smf(alist, adict):
  with open(adict) as f:
    for fdict in f:
      #print('Our hash: %s, File hash: %s' % (n.hexdigest(), ghash))
      with open(alist) as g:
        for ghash in g:
          listblock = ghash.split(':')
          fuser = listblock[0]
          fhash = listblock[1]
          crack_smf(fhash, fuser, fdict)
          
# crack only a single hash, loop through only dictionary list
def single_crack_smf(ahash, user, adict):
  with open(adict) as f:
    for fdict in f:
      crack_smf(ahash, user, fdict)

# smf hash - sha1(username + password)
def crack_smf(ahash, auser, aword):
  n = hashlib.sha1()
  n.update(auser.replace('\n', ' ').replace('\r', '').rstrip().lower().encode("utf-8") + aword.lower().replace('\n', ' ').replace('\r', '').rstrip().encode("utf-8"))
  if(n.hexdigest() == ahash.replace('\n', ' ').replace('\r', '').rstrip()):
    print('*** Hash Cracked ***\nHash: %sPassword: %s' % (ahash, aword))
  
def multi_crack_fluxbb(adict, alist, salt):
  print("Cracking fluxbb hashes found in: %s\n with dictionary: %s" % (alist, adict))
  
def single_crack_fluxbb(adict, ahash, salt):
  print("Cracking fluxbb hash: %s\n with dictionary: %s" % (ahash, adict))

# check the system version and exit if python 2
if sys.version_info[0] == 2:
  print("Incompatible python version, please use python version 3")
  print("https://www.python.org/downloads/")
  exit()

parser = argparse.ArgumentParser(description="fcracker.py - Simple python forum cracker")
parser.add_argument("-w", "--software", help="Software that made the hash, e.g: smf, fluxbb", required=True)
parser.add_argument("-a", "--hash", help="A single hash with which to crack", action="store")
parser.add_argument("-l", "--hash-list", help="Provide a list of hashes to crack", action="store")
parser.add_argument("-d", "--dictionary", help="Provide a dictionary of words to hash", required=True)
parser.add_argument("-u", "--user", help="smf hashes with the username", action="store")
parser.add_argument("-s", "--salt", help="fluxbb hashes with a salt", action="store")
args = parser.parse_args()

if(args.hash) and (args.hash_list):
  print("You must either input a single hash, or a list of hashes, not both")
  exit()
  
if(args.hash_list) and (args.user):
  print("You must provide the hash list as user:hash instead of only selecting one user")
  exit()

if(args.software == 'smf'):
  if(args.hash): # they only want to crack a single hash
    if(args.user): 
      print("Cracking smf user/hash: %s:%s\nTime: %s\n" % (args.user, args.hash, datetime.datetime.now()))
      single_crack_smf(args.hash, args.user, args.dictionary)
    else:
      print("Cracking a single smf hash requires you to include --user parameter")
  else:
    if(args.hash_list):
      print("Cracking smf hashes found in: %s\nWith dictionary: %s\nTime: %s\n" % (args.hash_list, args.dictionary, datetime.datetime.now()))
      multi_crack_smf(args.hash_list, args.dictionary)
    else:
      print("Cracking smf in multi-hash mode requiers a --hash-list parameter")
elif(args.software == 'fluxbb'):
  if(args.salt):
    if(args.hash): # they only want to crack a single hash
      print("Cracking fluxbb hash: %s\n with salt: %s" % (args.hash, args.salt))
      single_crack_fluxbb(args.dictionary, args.hash, args.salt)
    else:
      multi_crack_fluxbb(args.dictionary, args.hash_list, args.salt)
  else:
    print("Selecting fluxbb requires you to include --salt paramater");
else:
  print("You input a forum type for which we have not implemented yet");
