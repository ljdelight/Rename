#!/usr/bin/python
#
# Lucas Burson
# Do a recursive rename of files in a given directory using a regex.
#
# Examples:  
##  Remove the string 'The.' from the beginning of all files. 
##   'The.Big.Bang.Theory' -> 'Big.Bang.Theory'
##    rename.py "^The\." "" --verbose --write
##
##  Replace all dots within a filename with a space, except the extension.
##    'The.Big.Bang.Theory.avi' -> 'The Big Bang Theory.avi'
##    rename.py "\.(?=.*?\.)" " " --verbose --write
##

from __future__ import print_function
import os
import re
import fnmatch
from optparse import OptionParser

def renameFiles( re_exprToMatch, toSubstitute, 
            shellStyle_fileMatch='*', directory='.', write=False, verbose=True ):
   regex = re.compile( re_exprToMatch )
   count = 0

   # gather all (root,file/folder) pairs that match the expression
   for root, dirs, files in os.walk( directory ):
      toRename = []
      for f in fnmatch.filter( files, shellStyle_fileMatch ):
         if ( regex.search( f ) ):
            toRename.append( [root, f] )
      for d in fnmatch.filter( dirs, shellStyle_fileMatch ):
         if ( regex.search( d ) ):
            toRename.append( [root, d] )
            # We must rename the dir in the dirs list since the walk
            #     will miss a directory that we rename
            if ( write ):
               dirs[ dirs.index( d ) ] = regex.sub( toSubstitute, d )

      for pair in toRename:
         orig = os.path.join( pair[0], pair[1] )
         renamed = os.path.join( pair[0], regex.sub( toSubstitute, pair[1] ) )
         try:
            with open( renamed ) as f:
               print( pair[1], 'not renamed:', renamed, 'already exists' )
         except IOError as e:
            count += 1
            if ( write ):
               os.rename( orig, renamed )
            if ( verbose ):
               print( orig, '->', renamed )

   print( 'Renamed', count, 'files/folders' )
   if not write:
      print( 'NO CHANGES MADE (use --write)' )



def main():
   usage = 'usage: %prog re_exprToMatch toSubstitute [options]'
   parser = OptionParser(usage)
   parser.add_option( '--directory', '-d', type = 'string', 
      dest = 'directory', default ='.', help = 'directory to recurse and rename' )
   parser.add_option( '--file-pattern', '-p', type = 'string', 
      dest = 'filepattern', default = '*', help = 'shell-style pattern to filter files' )
   parser.add_option( '--verbose', '-v', action = 'store_true', 
      dest = 'verbose', default = False, help = 'show verbose output about renamed files' )
   parser.add_option( '--write', '-w', action = 'store_true', 
      dest = 'write', default = False, help = 'perform the changes')

   ( options, args ) = parser.parse_args()
   options.directory = os.path.abspath( options.directory )
   
   if ( len(args) != 2 ):
      parser.error( 'incorrect number of arguments' )
   if ( options.verbose ):
      print( 'Verbose:', options.verbose )
      print( 'Directory:', options.directory )
      print( 'File-pattern:', options.filepattern )
      print( 'Write:', options.write )
      print( 're_exprToMatch:', args[0] )
      print( 'toSubstitute:', args[1] )

   renameFiles( args[0], args[1], 
          options.filepattern, directory=options.directory, write=options.write, verbose=options.verbose )

if __name__ == "__main__":
   main()

