'''
Created on Oct 18, 2017

@author: Lab 10
'''
import sys
 
def opcode_table(label=None):  # label: operator of an instruction
    instructions = {}   #define a dictionary in order to store information of instrucition
    instructions['lwd'] = {'format': 'I', 'opcode': 35 }
    instructions['add'] = {'format': 'R', 'opcode': 10, 'func':0 }
    instructions['swd'] = {'format': 'I', 'opcode': 43 }
    instructions['sub'] = {'format': 'R', 'opcode': 20, 'func':0 } 
    instructions['beq'] = {'format': 'I', 'opcode': 4 } 
    instructions['and'] = {'format': 'R', 'opcode': 40 , 'func':0 }
    instructions['nor'] = {'format': 'R', 'opcode': 50 , 'func':0 }
    instructions['slt'] = {'format': 'R', 'opcode': 30 , 'func':0 }
    instructions['j'] = {'format': 'J', 'opcode': 2 }
    
    inst = instructions[label]
    return inst
    
def dec2bi(dec,n_bits):     # decimal to binary
    return bin(int(dec))[2:].zfill(n_bits)  #if it is not n bit number, fill the most significant bit with zero.
         
def R_format(regs=None,parse_inst=None):    # instruction
    rd,rs,rt = regs.split(',')  #split the three register by ','
    
    rd,rs,rt = rd[1:],rs[1:],rt[1:]     #delete symbol $

    opcode = parse_inst['opcode']   #get the opcode from parsed instruction.e.g.{'format': 'R', 'opcode': 40 , 'func':0 }
    func = parse_inst['func']   #get the function code
    
    mcode = dec2bi(func, 6) + '00000' + dec2bi(rd, 5) + dec2bi(rs, 5) + dec2bi(rt, 5) + dec2bi(opcode,6)  #machine code   
    
    return mcode    
        
def I_format(regs=None,parse_inst=None):  
    reg = regs.split(',')       #deal with the I-format instruction like lw $rt, offset($rs)
    if len(reg) == 2:
        rt, offrs = reg[0],reg[1]    #???
        rt = rt[1:]
        offset, rs = offrs.split('($')
        rs = rs[:-1]
        
    else:       # deal with the instruction like beq $rs, $rt, offset
        rt, rs, offset = reg[0],reg[1],reg[2]
        rs,rt = rs[1:],rt[1:]

    opcode = parse_inst['opcode']
   
    mcode = dec2bi(offset, 16) + dec2bi(rs, 5) + dec2bi(rt, 5) + dec2bi(opcode, 6)
   
    return mcode
    
def J_format(addr=None,parse_inst=None): 
    
    opcode = parse_inst['opcode']         
    
    mcode = dec2bi(addr, 26) + dec2bi(opcode, 6)
    
    return mcode
        
def bi2hex(mcode):      #binary to hexadecimal
    hexstr = hex(int(mcode,2))[2:].zfill(8)     #[2:] means delete the first two characters of a string
    hexcode = '0x' + hexstr.upper()         # add 0x in front of the hexcode. All characters converted to uppercase with hexstr.upper()
    return hexcode

print "Welcome to Assembler of Lab 10!"
while True:
    command = raw_input("Please input your command:")
    if command.startswith('myProg') and command.endswith('.asm'):
        break
    else:
        print 'This is not a valid command.Please re-enter one'

inputfname = command.split()[1]     #split the command, then get the second element which is filename     ??
inputfile = open(inputfname,'r')
o_fname = inputfname.replace('.asm','.o')
psd_fname = inputfname.replace('.asm','.psd')   #define the output filename as same as the input filename.
o_file = open(o_fname, 'w')
psd_file = open(psd_fname, 'w')

stream = ''     #define string used to store the binary code stream//     ?/??
    
for operation in inputfile:     #get the instruction of file line by line.
    label,operands = operation.split()      # split operator from the instruction    /??/?
    parse_inst = opcode_table(label)        # find the information of this instruction from opcode table
    form = parse_inst['format']         #get the format of instruction
    if form == 'R':
        mcode = R_format(operands, parse_inst)
    if form == 'I':
        mcode = I_format(operands, parse_inst)
    if form == 'J':
        mcode = J_format(operands, parse_inst)
        
    stream += mcode     #store the machine code into stream
    hexcode = bi2hex(mcode)     
    psd_file.write(hexcode+'\n')    #write the hexcode of instruction into .psd file line by line
    
o_file.write(stream)    

o_file.close()

psd_file.close()

inputfile.close()

    
