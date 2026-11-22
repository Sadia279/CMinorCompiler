target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    br label %bb0

bb0:
    %v1 = call i32 @factorial(i32 5)
    store i32 %v1, ptr %slot.t1
    br label %bb1

bb1:
    %v2 = load i32, ptr %slot.t1
    %v3 = icmp ne i32 %v2, 120
    %v4 = zext i1 %v3 to i32
    store i32 %v4, ptr %slot.t2
    br label %bb2

bb2:
    %v5 = load i32, ptr %slot.t2
    %v6 = icmp ne i32 %v5, 0
    br i1 %v6, label %bb3, label %bb5

bb3:
    ret i32 1

bb4:
    br label %bb6

bb5:
    br label %bb6

bb6:
    br label %bb7

bb7:
    ret i32 0

bb8:
    unreachable
}

define i32 @factorial(i32 %arg0) {
entry:
    %slot.n__v1 = alloca i32
    %slot.t3 = alloca i32
    %slot.t4 = alloca i32
    %slot.t5 = alloca i32
    %slot.t6 = alloca i32
    store i32 %arg0, ptr %slot.n__v1
    br label %bb0

bb0:
    %v1 = load i32, ptr %slot.n__v1
    %v2 = icmp sle i32 %v1, 1
    %v3 = zext i1 %v2 to i32
    store i32 %v3, ptr %slot.t3
    br label %bb1

bb1:
    %v4 = load i32, ptr %slot.t3
    %v5 = icmp ne i32 %v4, 0
    br i1 %v5, label %bb2, label %bb4

bb2:
    ret i32 1

bb3:
    br label %bb5

bb4:
    br label %bb5

bb5:
    br label %bb6

bb6:
    %v6 = load i32, ptr %slot.n__v1
    %v7 = sub i32 %v6, 1
    store i32 %v7, ptr %slot.t4
    br label %bb7

bb7:
    %v8 = load i32, ptr %slot.t4
    %v9 = call i32 @factorial(i32 %v8)
    store i32 %v9, ptr %slot.t5
    br label %bb8

bb8:
    %v10 = load i32, ptr %slot.n__v1
    %v11 = load i32, ptr %slot.t5
    %v12 = mul i32 %v10, %v11
    store i32 %v12, ptr %slot.t6
    br label %bb9

bb9:
    %v13 = load i32, ptr %slot.t6
    ret i32 %v13

bb10:
    unreachable
}
