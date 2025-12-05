use crate::moa_vm::VirtualMachine;

mod moa_vm;

fn main() {
    let bytecode: Vec<u8> = vec![1, 10, 0, 0, 0, 0, 0, 0, 0, 8, 1, 2, 0, 0, 0, 0, 0, 0, 0, 8, 9, 0, 0, 0, 0, 0, 0, 36, 64, 10, 12, 1, 2, 0, 0, 0, 0, 0, 0, 0, 7, 8, 13];
    let mut vm: VirtualMachine = VirtualMachine::new(bytecode);
    vm.run();

    println!("int_stack: {:?}", vm.int_stack);
    println!("float_stack: {:?}", vm.float_stack);
}
