	.file	"pipeline_loop_call.ll"
	.text
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
.Lfunc_end0:
	.size	add, .Lfunc_end0-add
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
# %bb.1:                                # %bb0
	movl	$0, 16(%rsp)
# %bb.2:                                # %bb1
	movl	$0, 20(%rsp)
.LBB1_3:                                # %bb2
                                        # =>This Inner Loop Header: Depth=1
	jmp	.LBB1_4
.LBB1_4:                                # %bb3
                                        #   in Loop: Header=BB1_3 Depth=1
	cmpl	$5, 20(%rsp)
	setl	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, 12(%rsp)
# %bb.5:                                # %bb4
                                        #   in Loop: Header=BB1_3 Depth=1
	cmpl	$0, 12(%rsp)
	je	.LBB1_12
# %bb.6:                                # %bb5
                                        #   in Loop: Header=BB1_3 Depth=1
	movl	16(%rsp), %edi
	movl	20(%rsp), %esi
	callq	add@PLT
	movl	%eax, 8(%rsp)
# %bb.7:                                # %bb6
                                        #   in Loop: Header=BB1_3 Depth=1
	movl	8(%rsp), %eax
	movl	%eax, 16(%rsp)
# %bb.8:                                # %bb7
                                        #   in Loop: Header=BB1_3 Depth=1
	jmp	.LBB1_9
.LBB1_9:                                # %bb8
                                        #   in Loop: Header=BB1_3 Depth=1
	movl	20(%rsp), %eax
	addl	$1, %eax
	movl	%eax, 4(%rsp)
# %bb.10:                               # %bb9
                                        #   in Loop: Header=BB1_3 Depth=1
	movl	4(%rsp), %eax
	movl	%eax, 20(%rsp)
# %bb.11:                               # %bb10
                                        #   in Loop: Header=BB1_3 Depth=1
	jmp	.LBB1_3
.LBB1_12:                               # %bb11
	jmp	.LBB1_13
.LBB1_13:                               # %bb12
	cmpl	$10, 16(%rsp)
	setne	%al
	andb	$1, %al
	movzbl	%al, %eax
	movl	%eax, (%rsp)
# %bb.14:                               # %bb13
	cmpl	$0, (%rsp)
	je	.LBB1_16
# %bb.15:                               # %bb14
	movl	$1, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.LBB1_16:                               # %bb16
	.cfi_def_cfa_offset 32
	jmp	.LBB1_17
.LBB1_17:                               # %bb17
	jmp	.LBB1_18
.LBB1_18:                               # %bb18
	xorl	%eax, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
