target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.a = alloca i32
    %slot.b = alloca i32
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    %slot.t3 = alloca i32
    %slot.total = alloca i32
    br label %bb0

bb0:
    store i32 10, ptr %slot.a
    br label %bb1

bb1:
    store i32 2, ptr %slot.b
    br label %bb2

bb2:
    %v1 = load i32, ptr %slot.b
    %v2 = mul i32 %v1, 3
    store i32 %v2, ptr %slot.t1
    br label %bb3

bb3:
    %v3 = load i32, ptr %slot.a
    %v4 = load i32, ptr %slot.t1
    %v5 = add i32 %v3, %v4
    store i32 %v5, ptr %slot.t2
    br label %bb4

bb4:
    %v6 = load i32, ptr %slot.t2
    store i32 %v6, ptr %slot.total
    br label %bb5

bb5:
    %v7 = load i32, ptr %slot.total
    %v8 = icmp ne i32 %v7, 16
    %v9 = zext i1 %v8 to i32
    store i32 %v9, ptr %slot.t3
    br label %bb6

bb6:
    %v10 = load i32, ptr %slot.t3
    %v11 = icmp ne i32 %v10, 0
    br i1 %v11, label %bb7, label %bb9

bb7:
    ret i32 1

bb8:
    br label %bb10

bb9:
    br label %bb10

bb10:
    br label %bb11

bb11:
    ret i32 0

bb12:
    unreachable
}
