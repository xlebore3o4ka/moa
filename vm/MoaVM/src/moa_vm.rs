#[derive(Debug, Clone)]
pub(crate) struct ErrorData {
    pub error_type: String,
    pub line: u32,
    pub pos: u16,
    pub len: u16,
    pub lexeme: String,
    pub file: String,
}

impl ErrorData {
    pub fn new(
        error_type: String,
        line: u32,
        pos: u16,
        len: u16,
        lexeme: String,
        file: String,
    ) -> Self {
        Self {
            error_type,
            line,
            pos,
            len,
            lexeme,
            file,
        }
    }
}


pub(crate) struct VirtualMachine {
    pub(crate) bytecode: Vec<u8>,
    pub(crate) ip: usize,
    pub(crate) error_stack: Vec<ErrorData>,
    pub(crate) int_stack: Vec<i64>,
    pub(crate) float_stack: Vec<f64>,
    halted: bool,
}

impl VirtualMachine {
    pub(crate) fn new(bytecode: Vec<u8>) -> VirtualMachine {
        VirtualMachine {
            bytecode,
            ip: 0,
            error_stack: Vec::new(),
            int_stack: Vec::new(),
            float_stack: Vec::new(),
            halted: false,
        }
    }

    pub(crate) fn run(&mut self) {
        while self.ip < self.bytecode.len() && !self.halted {
            self.execute();
        }
    }

    fn int_fetch(&mut self) -> i64 {
        self.ip += 8;
        i64::from_le_bytes(self.bytecode[self.ip - 8..self.ip].try_into().unwrap())
    }

    fn u8_fetch(&mut self) -> u8 {
        self.ip += 1;
        self.bytecode[self.ip-1]
    }

    fn u16_fetch(&mut self) -> u16 {
        self.ip += 2;
        u16::from_le_bytes(self.bytecode[self.ip - 2..self.ip].try_into().unwrap())
    }

    fn u32_fetch(&mut self) -> u32 {
        self.ip += 4;
        u32::from_le_bytes(self.bytecode[self.ip - 4..self.ip].try_into().unwrap())
    }

    fn utf8_fetch(&mut self, len: u64) -> String {
        let len_usize = len as usize;

        if self.ip + len_usize > self.bytecode.len() {
            return String::new();
        }

        let bytes = &self.bytecode[self.ip..self.ip + len_usize];
        self.ip += len_usize;

        String::from_utf8_lossy(bytes).into_owned()
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
                if b == 0 { return self.raise("Division by zero"); }
                self.error_stack.pop();
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
                if b == 0. { return self.raise("Division by zero"); }
                self.error_stack.pop();
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
            0x10 => {  // ERR_DATA error 0 error 1
                let error_type_string_len = self.u8_fetch();
                let error_type_string = self.utf8_fetch(error_type_string_len as u64);
                let line = self.u32_fetch();
                let pos = self.u16_fetch();
                let len = self.u16_fetch();
                let lexeme_string_len = self.u16_fetch();
                let lexeme_string = self.utf8_fetch(lexeme_string_len as u64);
                let file_string_len = self.u16_fetch();
                let file_string = self.utf8_fetch(file_string_len as u64);
                self.error_stack.push(ErrorData::new(error_type_string, line, pos, len, lexeme_string, file_string));
            }
            _ => {}
        }
    }
    fn raise(&mut self, msg: &str) {
        let error_data = self.error_stack.pop().unwrap();
        println!("Error in {:?} for the reason:", error_data.file);
        // TODO: stacktrace
        println!("  {:<width$} |", "", width = error_data.line.to_string().len());
        println!("  {} | {lexeme}", error_data.line.to_string(), lexeme = error_data.lexeme);
        println!("  {:<width$} | {spaces}{arrows}", "", width = error_data.line.to_string().len(), spaces = " ".repeat(error_data.pos as usize),
                 arrows = "^".repeat(error_data.len as usize));
        println!("[{}] {msg}", error_data.error_type);
        self.halted = true;
    }
}
