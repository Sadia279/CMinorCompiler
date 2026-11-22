	.file	"srs_b3.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
# %bb.1:                                # %bb0
	movl	$5, %edi
	callq	factorial@PLT
	movl	%eax, 4(%rsp)
# %bb.2:                                # %bb1
	cmpl	$120, 4(%rsp)
	setne	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, (%rsp)
# %bb.3:                                # %bb2
	cmpl	$0, (%rsp)
	je	.LBB0_5
# %bb.4:                                # %bb3
	movl	$1, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.LBB0_5:                                # %bb5
	.cfi_def_cfa_offset 16
	jmp	.LBB0_6
.LBB0_6:                                # %bb6
	jmp	.LBB0_7
.LBB0_7:                                # %bb7
	xorl	%eax, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.globl	factorial                       # -- Begin function factorial
	.p2align	4
	.type	factorial,@function
factorial:                              # @factorial
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movl	%edi, 20(%rsp)
# %bb.1:                                # %bb0
	cmpl	$1, 20(%rsp)
	setle	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, 16(%rsp)
# %bb.2:                                # %bb1
	cmpl	$0, 16(%rsp)
	je	.LBB1_4
# %bb.3:                                # %bb2
	movl	$1, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.LBB1_4:                                # %bb4
	.cfi_def_cfa_offset 32
	jmp	.LBB1_5
.LBB1_5:                                # %bb5
	jmp	.LBB1_6
.LBB1_6:                                # %bb6
	movl	20(%rsp), %eax
	subl	$1, %eax
	movl	%eax, 12(%rsp)
# %bb.7:                                # %bb7
	movl	12(%rsp), %edi
	callq	factorial@PLT
	movl	%eax, 8(%rsp)
# %bb.8:                                # %bb8
	movl	20(%rsp), %eax
	imull	8(%rsp), %eax
	movl	%eax, 4(%rsp)
# %bb.9:                                # %bb9
	movl	4(%rsp), %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	factorial, .Lfunc_end1-factorial
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
