	.file	"logical.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
# %bb.1:                                # %bb0
	movl	$10, %eax
	cmpl	$5, %eax
	setg	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -12(%rsp)
# %bb.2:                                # %bb1
	cmpl	$0, -12(%rsp)
	je	.LBB0_7
# %bb.3:                                # %bb2
	movl	$3, %eax
	cmpl	$4, %eax
	setl	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -16(%rsp)
# %bb.4:                                # %bb3
	cmpl	$0, -16(%rsp)
	je	.LBB0_7
# %bb.5:                                # %bb4
	movl	$1, -8(%rsp)
# %bb.6:                                # %bb5
	jmp	.LBB0_9
.LBB0_7:                                # %bb6
	jmp	.LBB0_8
.LBB0_8:                                # %bb7
	movl	$0, -8(%rsp)
.LBB0_9:                                # %bb8
	jmp	.LBB0_10
.LBB0_10:                               # %bb9
	cmpl	$0, -8(%rsp)
	jne	.LBB0_15
# %bb.11:                               # %bb10
	movb	$1, %al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -20(%rsp)
# %bb.12:                               # %bb11
	cmpl	$0, -20(%rsp)
	jne	.LBB0_15
# %bb.13:                               # %bb12
	movl	$0, -4(%rsp)
# %bb.14:                               # %bb13
	jmp	.LBB0_17
.LBB0_15:                               # %bb14
	jmp	.LBB0_16
.LBB0_16:                               # %bb15
	movl	$1, -4(%rsp)
.LBB0_17:                               # %bb16
	jmp	.LBB0_18
.LBB0_18:                               # %bb17
	cmpl	$0, -4(%rsp)
	je	.LBB0_20
# %bb.19:                               # %bb18
	movl	$7, %eax
	retq
.LBB0_20:                               # %bb20
	jmp	.LBB0_21
.LBB0_21:                               # %bb21
	jmp	.LBB0_22
.LBB0_22:                               # %bb22
	movl	$9, %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
