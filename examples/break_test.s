	.file	"break_test.ll"
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
# %bb.1:                                # %bb0
	movl	$0, -16(%rsp)
.LBB0_2:                                # %bb1
                                        # =>This Inner Loop Header: Depth=1
	jmp	.LBB0_3
.LBB0_3:                                # %bb2
                                        #   in Loop: Header=BB0_2 Depth=1
	cmpl	$10, -16(%rsp)
	setl	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -4(%rsp)
# %bb.4:                                # %bb3
                                        #   in Loop: Header=BB0_2 Depth=1
	cmpl	$0, -4(%rsp)
	je	.LBB0_13
# %bb.5:                                # %bb4
                                        #   in Loop: Header=BB0_2 Depth=1
	cmpl	$5, -16(%rsp)
	sete	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, -8(%rsp)
# %bb.6:                                # %bb5
                                        #   in Loop: Header=BB0_2 Depth=1
	cmpl	$0, -8(%rsp)
	je	.LBB0_8
# %bb.7:                                # %bb6
	jmp	.LBB0_13
.LBB0_8:                                # %bb8
                                        #   in Loop: Header=BB0_2 Depth=1
	jmp	.LBB0_9
.LBB0_9:                                # %bb9
                                        #   in Loop: Header=BB0_2 Depth=1
	jmp	.LBB0_10
.LBB0_10:                               # %bb10
                                        #   in Loop: Header=BB0_2 Depth=1
	movl	-16(%rsp), %eax
	addl	$1, %eax
	movl	%eax, -12(%rsp)
# %bb.11:                               # %bb11
                                        #   in Loop: Header=BB0_2 Depth=1
	movl	-12(%rsp), %eax
	movl	%eax, -16(%rsp)
# %bb.12:                               # %bb12
                                        #   in Loop: Header=BB0_2 Depth=1
	jmp	.LBB0_2
.LBB0_13:                               # %bb13
	jmp	.LBB0_14
.LBB0_14:                               # %bb14
	movl	-16(%rsp), %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
