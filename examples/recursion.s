	.file	"recursion.ll"
	.text
	.globl	fact                            # -- Begin function fact
	.p2align	4
	.type	fact,@function
fact:                                   # @fact
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
	je	.LBB0_4
# %bb.3:                                # %bb2
	movl	$1, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.LBB0_4:                                # %bb4
	.cfi_def_cfa_offset 32
	jmp	.LBB0_5
.LBB0_5:                                # %bb5
	movl	20(%rsp), %eax
	subl	$1, %eax
	movl	%eax, 12(%rsp)
# %bb.6:                                # %bb6
	movl	12(%rsp), %edi
	callq	fact@PLT
	movl	%eax, 8(%rsp)
# %bb.7:                                # %bb7
	movl	20(%rsp), %eax
	imull	8(%rsp), %eax
	movl	%eax, 4(%rsp)
# %bb.8:                                # %bb8
	movl	4(%rsp), %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	fact, .Lfunc_end0-fact
	.cfi_endproc
                                        # -- End function
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
	callq	fact@PLT
	movl	%eax, 4(%rsp)
# %bb.2:                                # %bb1
	movl	4(%rsp), %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
