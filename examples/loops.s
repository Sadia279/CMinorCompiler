	.file	"loops.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
# %bb.1:                                # %bb0
	movl	$0, -24(%rsp)
# %bb.2:                                # %bb1
	movl	$0, -4(%rsp)
.LBB0_3:                                # %bb2
                                        # =>This Inner Loop Header: Depth=1
	jmp	.LBB0_4
.LBB0_4:                                # %bb3
                                        #   in Loop: Header=BB0_3 Depth=1
	cmpl	$5, -24(%rsp)
	setl	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -8(%rsp)
# %bb.5:                                # %bb4
                                        #   in Loop: Header=BB0_3 Depth=1
	cmpl	$0, -8(%rsp)
	je	.LBB0_16
# %bb.6:                                # %bb5
                                        #   in Loop: Header=BB0_3 Depth=1
	cmpl	$5, -24(%rsp)
	setl	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -12(%rsp)
# %bb.7:                                # %bb6
                                        #   in Loop: Header=BB0_3 Depth=1
	cmpl	$0, -12(%rsp)
	je	.LBB0_11
# %bb.8:                                # %bb7
                                        #   in Loop: Header=BB0_3 Depth=1
	movl	-4(%rsp), %eax
	addl	-24(%rsp), %eax
	movl	%eax, -16(%rsp)
# %bb.9:                                # %bb8
                                        #   in Loop: Header=BB0_3 Depth=1
	movl	-16(%rsp), %eax
	movl	%eax, -4(%rsp)
# %bb.10:                               # %bb9
                                        #   in Loop: Header=BB0_3 Depth=1
	jmp	.LBB0_12
.LBB0_11:                               # %bb10
                                        #   in Loop: Header=BB0_3 Depth=1
	jmp	.LBB0_12
.LBB0_12:                               # %bb11
                                        #   in Loop: Header=BB0_3 Depth=1
	jmp	.LBB0_13
.LBB0_13:                               # %bb12
                                        #   in Loop: Header=BB0_3 Depth=1
	movl	-24(%rsp), %eax
	addl	$1, %eax
	movl	%eax, -20(%rsp)
# %bb.14:                               # %bb13
                                        #   in Loop: Header=BB0_3 Depth=1
	movl	-20(%rsp), %eax
	movl	%eax, -24(%rsp)
# %bb.15:                               # %bb14
                                        #   in Loop: Header=BB0_3 Depth=1
	jmp	.LBB0_3
.LBB0_16:                               # %bb15
	jmp	.LBB0_17
.LBB0_17:                               # %bb16
	movl	-4(%rsp), %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
