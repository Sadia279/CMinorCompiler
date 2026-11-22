	.file	"simple.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
# %bb.1:                                # %bb0
	movl	$20, %eax
	addl	$10, %eax
	movl	%eax, -4(%rsp)
# %bb.2:                                # %bb1
	movl	-4(%rsp), %eax
	movl	%eax, -8(%rsp)
# %bb.3:                                # %bb2
	movl	-8(%rsp), %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
