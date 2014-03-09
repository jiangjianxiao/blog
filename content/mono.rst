
install
====================

sudo apt-get install mono-complete

sudo apt-get install mono-devel


ppa
==============

sudo add-apt-repository ppa:directhex/monoxide
(If you use Ubuntu saucy 13.10, after adding the repository you need to edit the file /etc/apt/sources.list.d/directhex-monoxide-saucy.list and replace the word saucy with raring)

Then, after that:

sudo apt-get update && sudo apt-get dist-upgrade

fix  json.net BigInteger.parse 问题

问题
=============

Error CS1902: Invalid debug option `+'. Valid options are `full' or `pdbonly' (CS1902) (TAG)


Unhandled Exception:
System.TypeLoadException: Could not load type 'Monodoc.EditMerger' from assembly 'monodoc, Version=1.0.0.0, Culture=neutral, PublicKeyToken=0738eb9f132ed756'.
[ERROR] FATAL UNHANDLED EXCEPTION: System.TypeLoadException: Could not load type 'Monodoc.EditMerger' from assembly 'monodoc, Version=1.0.0.0, Culture=neutral, PublicKeyToken=0738eb9f132ed756'.


仅影响 debug版本

https://github.com/OpenRA/OpenRA/pull/2596/files 移去+debug