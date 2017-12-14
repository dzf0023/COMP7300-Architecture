'''
Created on Oct 18, 2017

@author: Lab 10
'''
 
def opcode_table(label=None):  # operator of an instruction
    instructions = {}
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
    
def dec2bi(dec,n_bits):  
    return bin(int(dec))[2:].zfill(n_bits)
         
def R_format(regs=None,parse_inst=None):  # instruction
#    label, regs = inst.split()
    rd,rs,rt = regs.split(',')
    
    rd,rs,rt = rd[1:],rs[1:],rt[1:] #delete symbol $
    
#     parse_inst = opcode_table(label)    
    opcode = parse_inst['opcode']
    func = parse_inst['func']
    
    mcode = dec2bi(func, 6) + '00000' + dec2bi(rd, 5) + dec2bi(rs, 5) + dec2bi(rt, 5) + dec2bi(opcode,6)
    
    return mcode
        
def I_format(regs=None,parse_inst=None): 
    reg = regs.split(',')       
    if len(reg) == 2:
        rt, offrs = reg[0],reg[1]
        rt = rt[1:]
        offset, rs = offrs.split('($')
        rs = rs[:-1]
#         print rt,rs,offset
         
    else:
        rt, rs, offset = reg[0],reg[1],reg[2]
        rs,rt = rs[1:],rt[1:]
#        print rt,rs,offset
#     parse_inst = opcode_table(label)
    opcode = parse_inst['opcode']
   
    mcode = dec2bi(offset, 16) + dec2bi(rs, 5) + dec2bi(rt, 5) + dec2bi(opcode, 6)
   
    return mcode
    
def J_format(addr=None,parse_inst=None): 
#     label, addr = inst.split()    
#     parse_inst = opcode_table(label)   
    
    opcode = parse_inst['opcode']         
    
    mcode = dec2bi(addr, 26) + dec2bi(opcode, 6)
    
    return mcode
        
def bi2hex(mcode):
    hexstr = hex(int(mcode,2))[2:].zfill(8)
    hexcode = '0x' + hexstr.upper()         # instruction code in hex
    return hexcode

print "Welcome to Assembler of Lab 10!"
while True:
    command = raw_input("Please input your command:")
    if command.startswith('myProg') and command.endswith('.asm'):
        break
    else:
        print 'This is not a valid command.Please re-enter one'

inputfname = command.split()[1]
# print inputfname
inputfile = open(inputfname,'r')
o_fname = inputfname.replace('.asm','.o')
psd_fname = inputfname.replace('.asm','.psd')
# print o_fname,psd_fname
o_file = open(o_fname, 'w')
psd_file = open(psd_fname, 'w')

stream = ''
    
for operation in inputfile:
    label,operands = operation.split()
    parse_inst = opcode_table(label)
    form = parse_inst['format'] 
    if form == 'R':
        mcode = R_format(operands, parse_inst)
    if form == 'I':
        mcode = I_format(operands, parse_inst)
    if form == 'J':
        mcode = J_format(operands, parse_inst)
        
    stream += mcode
    hexcode = bi2hex(mcode)
    psd_file.write(hexcode+'\n')
    
o_file.write(stream)

o_file.close()

psd_file.close()

inputfile.close()

    
