	.file	"for_loop.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
# %bb.1:                                # %bb0
	movl	$0, -4(%rsp)
# %bb.2:                                # %bb1
	movl	$0, -8(%rsp)
# %bb.3:                                # %bb2
	movl	$0, -4(%rsp)
.LBB0_4:                                # %bb3
                                        # =>This Inner Loop Header: Depth=1
	jmp	.LBB0_5
.LBB0_5:                                # %bb4
                                        #   in Loop: Header=BB0_4 Depth=1
	cmpl	$5, -4(%rsp)
	setl	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -12(%rsp)
# %bb.6:                                # %bb5
                                        #   in Loop: Header=BB0_4 Depth=1
	cmpl	$0, -12(%rsp)
	je	.LBB0_18
# %bb.7:                                # %bb6
                                        #   in Loop: Header=BB0_4 Depth=1
	cmpl	$2, -4(%rsp)
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
	movl	-8(%rsp), %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
