target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.t1 = alloca i32
    %slot.x = alloca i32
    br label %bb0

bb0:
    %v1 = add i32 10, 20
    store i32 %v1, ptr %slot.t1
    br label %bb1

bb1:
    %v2 = load i32, ptr %slot.t1
    store i32 %v2, ptr %slot.x
    br label %bb2

bb2:
    %v3 = load i32, ptr %slot.x
    ret i32 %v3

bb3:
    unreachable
}

