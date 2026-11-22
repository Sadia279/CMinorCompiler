	.file	"srs_b1.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
# %bb.1:                                # %bb0
	movl	$10, -4(%rsp)
# %bb.2:                                # %bb1
	movl	$2, -8(%rsp)
# %bb.3:                                # %bb2
	imull	$3, -8(%rsp), %eax
	movl	%eax, -12(%rsp)
# %bb.4:                                # %bb3
	movl	-4(%rsp), %eax
	addl	-12(%rsp), %eax
	movl	%eax, -16(%rsp)
# %bb.5:                                # %bb4
	movl	-16(%rsp), %eax
	movl	%eax, -24(%rsp)
# %bb.6:                                # %bb5
	cmpl	$16, -24(%rsp)
	setne	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -20(%rsp)
# %bb.7:                                # %bb6
	cmpl	$0, -20(%rsp)
	je	.LBB0_9
# %bb.8:                                # %bb7
	movl	$1, %eax
	retq
.LBB0_9:                                # %bb9
	jmp	.LBB0_10
.LBB0_10:                               # %bb10
	jmp	.LBB0_11
.LBB0_11:                               # %bb11
	xorl	%eax, %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
