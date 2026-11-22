target triple = "x86_64-pc-linux-gnu"

define i32 @fact(i32 %arg0) {
entry:
    %slot.n = alloca i32
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    %slot.t3 = alloca i32
    %slot.t4 = alloca i32
    store i32 %arg0, ptr %slot.n
    br label %bb0

bb0:
    %v1 = load i32, ptr %slot.n
    %v2 = icmp sle i32 %v1, 1
    %v3 = zext i1 %v2 to i32
    store i32 %v3, ptr %slot.t1
    br label %bb1

bb1:
    %v4 = load i32, ptr %slot.t1
    %v5 = icmp ne i32 %v4, 0
    br i1 %v5, label %bb2, label %bb4

bb2:
    ret i32 1

bb3:
    br label %bb9

bb4:
    br label %bb5

bb5:
    %v6 = load i32, ptr %slot.n
    %v7 = sub i32 %v6, 1
    store i32 %v7, ptr %slot.t2
    br label %bb6

bb6:
    %v8 = load i32, ptr %slot.t2
    %v9 = call i32 @fact(i32 %v8)
    store i32 %v9, ptr %slot.t3
    br label %bb7

bb7:
    %v10 = load i32, ptr %slot.n
    %v11 = load i32, ptr %slot.t3
    %v12 = mul i32 %v10, %v11
    store i32 %v12, ptr %slot.t4
    br label %bb8

bb8:
    %v13 = load i32, ptr %slot.t4
    ret i32 %v13

bb9:
    br label %bb10

bb10:
    unreachable
}

define i32 @main() {
entry:
    %slot.t5 = alloca i32
    br label %bb0

bb0:
    %v1 = call i32 @fact(i32 5)
    store i32 %v1, ptr %slot.t5
    br label %bb1

bb1:
    %v2 = load i32, ptr %slot.t5
    ret i32 %v2

bb2:
    unreachable
}

