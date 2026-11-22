	.file	"srs_b4.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
# %bb.1:                                # %bb0
	movl	$0, -48(%rsp)
# %bb.2:                                # %bb1
	movl	$0, -8(%rsp)
# %bb.3:                                # %bb2
	movl	$1, -4(%rsp)
.LBB0_4:                                # %bb3
                                        # =>This Inner Loop Header: Depth=1
	jmp	.LBB0_5
.LBB0_5:                                # %bb4
                                        #   in Loop: Header=BB0_4 Depth=1
	cmpl	$5, -4(%rsp)
	setle	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -12(%rsp)
# %bb.6:                                # %bb5
                                        #   in Loop: Header=BB0_4 Depth=1
	cmpl	$0, -12(%rsp)
	je	.LBB0_18
# %bb.7:                                # %bb6
                                        #   in Loop: Header=BB0_4 Depth=1
	cmpl	$3, -4(%rsp)
	sete	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -16(%rsp)
# %bb.8:                                # %bb7
                                        #   in Loop: Header=BB0_4 Depth=1
	cmpl	$0, -16(%rsp)
	je	.LBB0_10
# %bb.9:                                # %bb8
                                        #   in Loop: Header=BB0_4 Depth=1
	jmp	.LBB0_14
.LBB0_10:                               # %bb10
                                        #   in Loop: Header=BB0_4 Depth=1
	jmp	.LBB0_11
.LBB0_11:                               # %bb11
                                        #   in Loop: Header=BB0_4 Depth=1
	jmp	.LBB0_12
.LBB0_12:                               # %bb12
                                        #   in Loop: Header=BB0_4 Depth=1
	movl	-8(%rsp), %eax
	addl	-4(%rsp), %eax
	movl	%eax, -20(%rsp)
# %bb.13:                               # %bb13
                                        #   in Loop: Header=BB0_4 Depth=1
	movl	-20(%rsp), %eax
	movl	%eax, -8(%rsp)
.LBB0_14:                               # %bb14
                                        #   in Loop: Header=BB0_4 Depth=1
	jmp	.LBB0_15
.LBB0_15:                               # %bb15
                                        #   in Loop: Header=BB0_4 Depth=1
	movl	-4(%rsp), %eax
	addl	$1, %eax
	movl	%eax, -24(%rsp)
# %bb.16:                               # %bb16
                                        #   in Loop: Header=BB0_4 Depth=1
	movl	-24(%rsp), %eax
	movl	%eax, -4(%rsp)
# %bb.17:                               # %bb17
                                        #   in Loop: Header=BB0_4 Depth=1
	jmp	.LBB0_4
.LBB0_18:                               # %bb18
	jmp	.LBB0_19
.LBB0_19:                               # %bb19
	cmpl	$12, -8(%rsp)
	setne	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -28(%rsp)
# %bb.20:                               # %bb20
	cmpl	$0, -28(%rsp)
	je	.LBB0_22
# %bb.21:                               # %bb21
	movl	$1, %eax
	retq
.LBB0_22:                               # %bb23
	jmp	.LBB0_23
.LBB0_23:                               # %bb24
	jmp	.LBB0_24
.LBB0_24:                               # %bb25
                                        # =>This Inner Loop Header: Depth=1
	jmp	.LBB0_25
.LBB0_25:                               # %bb26
                                        #   in Loop: Header=BB0_24 Depth=1
	cmpl	$10, -48(%rsp)
	setl	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -32(%rsp)
# %bb.26:                               # %bb27
                                        #   in Loop: Header=BB0_24 Depth=1
	cmpl	$0, -32(%rsp)
	je	.LBB0_35
# %bb.27:                               # %bb28
                                        #   in Loop: Header=BB0_24 Depth=1
	movl	-48(%rsp), %eax
	addl	$1, %eax
	movl	%eax, -36(%rsp)
# %bb.28:                               # %bb29
                                        #   in Loop: Header=BB0_24 Depth=1
	movl	-36(%rsp), %eax
	movl	%eax, -48(%rsp)
# %bb.29:                               # %bb30
                                        #   in Loop: Header=BB0_24 Depth=1
	cmpl	$7, -48(%rsp)
	sete	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -40(%rsp)
# %bb.30:                               # %bb31
                                        #   in Loop: Header=BB0_24 Depth=1
	cmpl	$0, -40(%rsp)
	je	.LBB0_32
# %bb.31:                               # %bb32
	jmp	.LBB0_35
.LBB0_32:                               # %bb34
                                        #   in Loop: Header=BB0_24 Depth=1
	jmp	.LBB0_33
.LBB0_33:                               # %bb35
                                        #   in Loop: Header=BB0_24 Depth=1
	jmp	.LBB0_34
.LBB0_34:                               # %bb36
                                        #   in Loop: Header=BB0_24 Depth=1
	jmp	.LBB0_24
.LBB0_35:                               # %bb37
	jmp	.LBB0_36
.LBB0_36:                               # %bb38
	cmpl	$7, -48(%rsp)
	setne	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -44(%rsp)
# %bb.37:                               # %bb39
	cmpl	$0, -44(%rsp)
	je	.LBB0_39
# %bb.38:                               # %bb40
	movl	$2, %eax
	retq
.LBB0_39:                               # %bb42
	jmp	.LBB0_40
.LBB0_40:                               # %bb43
	jmp	.LBB0_41
.LBB0_41:                               # %bb44
	xorl	%eax, %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
