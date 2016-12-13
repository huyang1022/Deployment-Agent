#! /usr/bin/env python

__author__ = 'Yang Hu'

import argparse, os, sys
import time
from vm_info import VmInfo
import docker_engine, docker_registry, docker_execute, docker_distribute, docker_kubernetes
import threading

def parse_args(args_str):
    description = "Deployment Agent"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-i", action = "store",
            dest = "file",
            help = "The input file")
    parser.add_argument("-o", action = "store",
            dest = "process",
            help = "The input of processing")

    return parser.parse_args(args_str)

def main():
    args = parse_args(sys.argv[1:])
    in_file = open(args.file, "r")
    threads = []
    if args.process == "distribute":
        docker_distribute.distribute(in_file)
    if args.process == "kubernetes":
        docker_kubernetes.install_kubernetes(in_file)
    else:
        while True:
            line = in_file.readline()
            if not line: break
            file_list = line.split()
            vm = VmInfo(file_list[0], file_list[1], file_list[2], "")
            if args.process == "engine":
                threads.append(threading.Thread(target = docker_engine.install_engine, args = (vm, )))
                threads[-1].start()
            elif args.process == "registry":
                threads.append(threading.Thread(target = docker_registry.install_registry, args = (vm, file_list[3])))
                threads[-1].start()
            elif args.process == "execute":
                threads.append(threading.Thread(targe = docker_execute.execute, args = (vm, file_list[3])))
                threads[-1].start()
    for t in threads:
        t.join()


    
if __name__ == '__main__':
    start = time.time()
    main()
    print time.time()-start
