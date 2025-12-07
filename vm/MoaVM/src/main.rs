use std::fs;
use crate::moa_vm::VirtualMachine;

mod moa_vm;

fn main() {
    use std::env;

    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage : {} <file.mvm> [-d|--debug]", args[0]);
        std::process::exit(1);
    }

    let filename = &args[1];
    let debug_mode = args.contains(&"-d".to_string()) || args.contains(&"--debug".to_string());

    let bytecode = match fs::read(filename) {
        Ok(bytes) => bytes,
        Err(e) => {
            eprintln!("Error reading file {}: {}", filename, e);
            std::process::exit(1);
        }
    };

    let mut vm: VirtualMachine = VirtualMachine::new(bytecode);
    vm.run();

    if debug_mode {
        println!("int_stack   : {:?}", vm.int_stack);
        println!("float_stack : {:?}", vm.float_stack);
    }
}