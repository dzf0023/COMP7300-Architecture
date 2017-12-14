.data

	myMessage:   .asciiz "Hello world  "
	newLine:     .asciiz "\n"
	endloop:     .asciiz "this is the end of the loop"
	#space:		.asciiz " ,  "
.text 
	main:
		
		addi $t0, $zero, 0
		
		while: 
			bgt  $t0, 6, exit
			jal printSentences
			addi $t0, $t0,1			# i++
			
			
			j while 				#jump out 
			
		
		exit: 
	
			li  $v0, 6
			syscall 
		
	printSentences:
		li $v0, 4
		la $a0, myMessage 
		syscall
		
		
		jr $ra
	
	
	    
		
