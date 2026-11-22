target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.result = alloca i32
    %slot.t1 = alloca i32
    %slot.x = alloca i32
    br label %bb0

bb0:
    store i32 10, ptr %slot.t1
    br label %bb1

bb1:
    store i32 20, ptr %slot.x
    br label %bb2

bb2:
    %v1 = load i32, ptr %slot.t1
    %v2 = load i32, ptr %slot.x
    %v3 = add i32 %v1, %v2
    store i32 %v3, ptr %slot.t1
    br label %bb3

bb3:
    %v4 = load i32, ptr %slot.t1
    store i32 %v4, ptr %slot.result
    br label %bb4

bb4:
    %v5 = load i32, ptr %slot.result
    ret i32 %v5

bb5:
    unreachable
}
