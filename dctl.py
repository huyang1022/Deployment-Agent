 #! /usr/bin/env python

 # Copyright 2017 --Yang Hu--
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
 

__author__ = 'Yang Hu'

import argparse, sys
import time
from vm_info import VmInfo
import docker_engine, docker_registry, docker_execute, docker_distribute, docker_kubernetes, docker_swarm, docker_image, control_agent

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
    vm_list = []

    if args.process == "registry":
        docker_registry.run(in_file)
    if args.process == "distribute":
        docker_distribute.run(in_file)
        
    while True:
        line = in_file.readline()
        file_list = line.split()
        if not file_list: break
        vm = VmInfo(file_list[0], file_list[1], file_list[2], file_list[3])
        vm_list.append(vm)

    if args.process == "engine":
        docker_engine.run(vm_list)
    if args.process == "kubernetes":
        docker_kubernetes.run(vm_list)
    if args.process == "swarm":
        docker_swarm.run(vm_list)
    if args.process == "image":
        docker_image.run(vm_list)     
    if args.process == "execute":
        docker_execute.run(vm_list)
    if args.process == "agent":
        control_agent.run(vm_list)


    
    
if __name__ == '__main__':
    start = time.time()
    main()
    print time.time()-start
