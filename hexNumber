# Objective: asks the user for decimal number n. Convert it to hex and print the result   

	.data 
	
prompt: .asciiz "Enter a decimal value: \n" 
res: .asciiz "\nThe number in hexadecimal is: " 
result: .space 8     

	.text     
main:     
	la $a0, prompt     
	li $v0, 4    
	syscall
	     
        li $v0, 51          # Specify Read Integer service (#51)
        syscall             # System call to execute service # 51 (in Register $v0) : Read the number. After this instruction, the number read is in Register $a0.
        beq $a1, -2, Quit   # Quit when user cancel input
        
        li $v0,1	    #print out the input
        syscall
	     
	move $t2, $a0       # move the input value in register t2
	la $a0, res    
	li $v0, 4     
	syscall 
	    
	li $t0, 8           # counter     
	la $t3, result      # where result will be stored 
	
	
Loop:   beqz $t0, Exit      # branch to exit if counter is equal to zero     
	rol $t2, $t2, 4     # rotate 4 bits to the left     
	and $t4, $t2, 0xf   # mask with 1111     
	ble $t4, 9, Sum     # if less than or equal to nine, branch to sum     
	addi $t4, $t4, 55   # if greater than nine, add 55     
	b End 
	
Sum:    addi $t4, $t4, 48   # add 48 to result   
	
End:	sb $t4, 0($t3)      # store hex digit into result     
	addi $t3, $t3, 1    # increment address counter     
	addi $t0, $t0, -1   # decrement loop counter 
	j Loop 
	
	
Exit:     
	la $a0, result     
	li $v0, 4     
	syscall
	    
Quit:	li $v0, 10     
	syscall  
