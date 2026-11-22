	.file	"custom_output.ll"
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
	pushq	%rax
	.cfi_def_cfa_offset 16
# %bb.1:                                # %bb0
	movl	$10, %edi
	movl	$20, %esi
	callq	add@PLT
	movl	%eax, (%rsp)
# %bb.2:                                # %bb1
	movl	(%rsp), %eax
	movl	%eax, 4(%rsp)
# %bb.3:                                # %bb2
	movl	4(%rsp), %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
