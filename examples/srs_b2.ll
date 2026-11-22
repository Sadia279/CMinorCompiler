target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.result = alloca i32
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    br label %bb0

bb0:
    %v1 = call i32 @add(i32 10, i32 20)
    store i32 %v1, ptr %slot.t1
    br label %bb1

bb1:
    %v2 = load i32, ptr %slot.t1
    store i32 %v2, ptr %slot.result
    br label %bb2

bb2:
    %v3 = load i32, ptr %slot.result
    %v4 = icmp ne i32 %v3, 30
    %v5 = zext i1 %v4 to i32
    store i32 %v5, ptr %slot.t2
    br label %bb3

bb3:
    %v6 = load i32, ptr %slot.t2
    %v7 = icmp ne i32 %v6, 0
    br i1 %v7, label %bb4, label %bb6

bb4:
    ret i32 1

bb5:
    br label %bb7

bb6:
    br label %bb7

bb7:
    br label %bb8

bb8:
    ret i32 0

bb9:
    unreachable
}

define i32 @add(i32 %arg0, i32 %arg1) {
entry:
    %slot.a = alloca i32
    %slot.b = alloca i32
    %slot.t3 = alloca i32
    store i32 %arg0, ptr %slot.a
    store i32 %arg1, ptr %slot.b
    br label %bb0

bb0:
    %v1 = load i32, ptr %slot.a
    %v2 = load i32, ptr %slot.b
    %v3 = add i32 %v1, %v2
    store i32 %v3, ptr %slot.t3
    br label %bb1

bb1:
    %v4 = load i32, ptr %slot.t3
    ret i32 %v4

bb2:
    unreachable
}
