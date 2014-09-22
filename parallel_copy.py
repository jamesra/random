'''
Created on Sep 22, 2014

@author: u0490822
'''

import sys
import argparse
import os
import multiprocessing
import nornir_pools as pools

def create_parser():
    parser = argparse.ArgumentParser('parallel_copy', conflict_handler='resolve', description='Options available to all build commands.  Specific pipelines may extend the argument list.')

    parser.add_argument('src_path',
                        metavar='import',
                        action='store',
                        type=str,
                        default=None,
                        
                        help='The source directory',
                        )
    
    parser.add_argument('dest_path',
                        metavar='import',
                        action='store',
                        type=str,
                        default=None,
                        help='The destination directory',
                        ) 
    
    parser.add_argument('-mt', 
                        action='store',
                        type=int,
                        dest='cpu_count',
                        default=multiprocessing.cpu_count(),
                        help='Number of processes to launch simultaneously',
                        ) 
    
    return parser

cmd_template = 'robocopy %s %s /MIR /Z /R:3 /W:1 /NFL /TEE /LEV:1 && exit'
    
def Execute(buildArgs=None):
    if buildArgs is None:
        buildArgs = sys.argv[1:]
        
    parser = create_parser()
    args = parser.parse_args()
    
    src_path = args.src_path
    dest_path = args.dest_path
    
    if not src_path.endswith(os.path.sep) or src_path.endswith(os.path.altsep):
        src_path += os.path.sep
        
    if not dest_path.endswith(os.path.sep) or dest_path.endswith(os.path.altsep):
        dest_path += os.path.sep
    
    if not os.path.exists(src_path):
        print("Input path %s must exist" % (src_path))
        
    try:
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
    except IOError:
        print("Could not create destination path %s" % (dest_path))
    
    pool = pools.GetLocalMachinePool("parallel_copy", num_threads=args.cpu_count)
                        
    len_src_path = len(src_path)
    for (path, dirnames, filenames) in os.walk(src_path):         
        #path should start with src_path, so remove that from the path
        rel_path = path[len_src_path:]
        
        if len(rel_path) > 0:
            if rel_path[0] == os.path.sep or rel_path[0] == os.path.altsep:
                rel_path = rel_path[1:]
        
        full_dest_path = os.path.join(dest_path, rel_path)
        
        if not os.path.exists(full_dest_path):
            os.makedirs(full_dest_path)
         
        cmd = cmd_template % (path, full_dest_path)
        print(cmd)    
        
        pool.add_process(cmd, cmd)
    
if __name__ == '__main__':
    Execute()
     