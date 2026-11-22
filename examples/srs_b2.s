	.file	"srs_b2.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
# %bb.1:                                # %bb0
	movl	$10, %edi
	movl	$20, %esi
	callq	add@PLT
	movl	%eax, 16(%rsp)
# %bb.2:                                # %bb1
	movl	16(%rsp), %eax
	movl	%eax, 20(%rsp)
# %bb.3:                                # %bb2
	cmpl	$30, 20(%rsp)
	setne	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, 12(%rsp)
# %bb.4:                                # %bb3
	cmpl	$0, 12(%rsp)
	je	.LBB0_6
# %bb.5:                                # %bb4
	movl	$1, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.LBB0_6:                                # %bb6
	.cfi_def_cfa_offset 32
	jmp	.LBB0_7
.LBB0_7:                                # %bb7
	jmp	.LBB0_8
.LBB0_8:                                # %bb8
	xorl	%eax, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.globl	add                             # -- Begin function add
	.p2align	4
	.type	add,@function
add:                                    # @add
	.cfi_startproc
# %bb.0:                                # %entry
	movl	%edi, -4(%rsp)
	movl	%esi, -8(%rsp)
# %bb.1:                                # %bb0
	movl	-4(%rsp), %eax
	addl	-8(%rsp), %eax
	movl	%eax, -12(%rsp)
# %bb.2:                                # %bb1
	movl	-12(%rsp), %eax
	retq
.Lfunc_end1:
	.size	add, .Lfunc_end1-add
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
