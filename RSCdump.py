import struct 
import os
import json
import argparse

def read_uint32(f):
    return struct.unpack(">I", f.read(4))[0]

def read_entry(f):
    unknown, size, offset_nextentry = struct.unpack(">III", f.read(4*3))
    padding = f.read(0x20-4*3)
    
    return unknown, size, offset_nextentry

def make_entry_filename(index, unknown):
    return "entry_{0}_({1}).bin".format(index, unknown)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                        help="Filepath to RSC file")
    parser.add_argument("output", default=None, nargs = '?',
                        help="Folder path to which all extracted files are written")
    
    args = parser.parse_args()
    
    in_rsc = args.input 
    
    if args.output is None:
        out_folder = in_rsc+"_Folder"
    else:
        out_folder = args.output
        
    os.makedirs(out_folder, exist_ok=True)
    
    with open(in_rsc, "rb") as f:
        header = struct.unpack(">"+32*"B", f.read(0x20))
        
        with open(os.path.join(out_folder, "header.txt"), "w") as g:
            g.write(" ".join(str(x) for x in header))
        
        entry_index = 0
        unk, size, next = read_entry(f)
        
        entry_data = f.read(size)
        
        print(unk, size, next)
        
        
        out_filename = make_entry_filename(entry_index, unk)
        
        with open(os.path.join(out_folder, out_filename), "wb") as g:
            g.write(entry_data)
        
        while next != 0:
            f.seek(next)
            
            
            entry_index += 1
            unk, size, next = read_entry(f)
            
            entry_data = f.read(size)
            
            print(unk, size, next)
            
            out_filename = make_entry_filename(entry_index, unk)
        
            with open(os.path.join(out_folder, out_filename), "wb") as g:
                g.write(entry_data)