pub(crate) struct VirtualMachine {
    pub(crate) bytecode: Vec<u8>,
    pub(crate) ip: usize,
    pub(crate) int_stack: Vec<i64>,
    pub(crate) float_stack: Vec<f64>,
}

impl VirtualMachine {
    pub(crate) fn new(bytecode: Vec<u8>) -> VirtualMachine {
        VirtualMachine {
            bytecode,
            ip: 0,
            int_stack: Vec::new(),
            float_stack: Vec::new(),
        }
    }

    pub(crate) fn run(&mut self) {
        while self.ip < self.bytecode.len() {
            self.execute();
        }
    }

    fn int_fetch(&mut self) -> i64 {
        self.ip += 8;
        i64::from_le_bytes(self.bytecode[self.ip - 8..self.ip].try_into().unwrap())
    }

    fn float_fetch(&mut self) -> f64 {
        self.ip += 8;
        f64::from_le_bytes(self.bytecode[self.ip - 8..self.ip].try_into().unwrap())
    }

    fn execute(&mut self) {
        let opcode = self.bytecode[self.ip];
        self.ip += 1;

        match opcode {
            0x00 => {}
            0x01 => {  // INT_PUSH int 0 int 1
                let a = self.int_fetch();
                self.int_stack.push(a);
            }
            0x02 => {  // INT_ADD int 2 int 1
                let b = self.int_stack.pop().unwrap();
                let a = self.int_stack.pop().unwrap();
                self.int_stack.push(a + b);
            }
            0x03 => {  // INT_SUB int 2 int 1
                let b = self.int_stack.pop().unwrap();
                let a = self.int_stack.pop().unwrap();
                self.int_stack.push(a - b);
            }
            0x04 => {  // INT_MUL int 2 int 1
                let b = self.int_stack.pop().unwrap();
                let a = self.int_stack.pop().unwrap();
                self.int_stack.push(a * b);
            }
            0x05 => {  // INT_DIV int 2 int 1
                let b = self.int_stack.pop().unwrap();
                let a = self.int_stack.pop().unwrap();
                self.int_stack.push(a / b);
            }
            0x06 => {  // INT_MOD int 2 int 1
                let b = self.int_stack.pop().unwrap();
                let a = self.int_stack.pop().unwrap();
                self.int_stack.push(a % b);
            }
            0x07 => {  // INT_NEG int 1 int 1
                let a = self.int_stack.pop().unwrap();
                self.int_stack.push(-a)
            }
            0x08 => {  // INT_FLOAT int 1 float 1
                let a = self.int_stack.pop().unwrap();
                self.float_stack.push(a as f64);
            }
            0x09 => {  // FLOAT_PUSH float 0 float 1
                let a = self.float_fetch();
                self.float_stack.push(a);
            }
            0x0a => {  // FLOAT_ADD float 2 float 1
                let b = self.float_stack.pop().unwrap();
                let a = self.float_stack.pop().unwrap();
                self.float_stack.push(a + b);
            }
            0x0b => {  // FLOAT_SUB float 2 float 1
                let b = self.float_stack.pop().unwrap();
                let a = self.float_stack.pop().unwrap();
                self.float_stack.push(a - b);
            }
            0x0c => {  // FLOAT_MUL float 2 float 1
                let b = self.float_stack.pop().unwrap();
                let a = self.float_stack.pop().unwrap();
                self.float_stack.push(a * b);
            }
            0x0d => {  // FLOAT_DIV float 2 float 1
                let b = self.float_stack.pop().unwrap();
                let a = self.float_stack.pop().unwrap();
                self.float_stack.push(a / b);
            }
            0x0e => {  // FLOAT_NEG float 1 float 1
                let a = self.float_stack.pop().unwrap();
                self.float_stack.push(-a);
            }
            0x0f => {  // FLOAT_INT float 1 int 1
                let a = self.float_stack.pop().unwrap();
                self.int_stack.push(a as i64);
            }
            _ => {}
        }
    }
}
