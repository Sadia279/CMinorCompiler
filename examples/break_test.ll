target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    %slot.t3 = alloca i32
    %slot.x = alloca i32
    br label %bb0

bb0:
    store i32 0, ptr %slot.x
    br label %bb1

bb1:
    br label %bb2

bb2:
    %v1 = load i32, ptr %slot.x
    %v2 = icmp slt i32 %v1, 10
    %v3 = zext i1 %v2 to i32
    store i32 %v3, ptr %slot.t1
    br label %bb3

bb3:
    %v4 = load i32, ptr %slot.t1
    %v5 = icmp ne i32 %v4, 0
    br i1 %v5, label %bb4, label %bb13

bb4:
    %v6 = load i32, ptr %slot.x
    %v7 = icmp eq i32 %v6, 5
    %v8 = zext i1 %v7 to i32
    store i32 %v8, ptr %slot.t2
    br label %bb5

bb5:
    %v9 = load i32, ptr %slot.t2
    %v10 = icmp ne i32 %v9, 0
    br i1 %v10, label %bb6, label %bb8

bb6:
    br label %bb13

bb7:
    br label %bb9

bb8:
    br label %bb9

bb9:
    br label %bb10

bb10:
    %v11 = load i32, ptr %slot.x
    %v12 = add i32 %v11, 1
    store i32 %v12, ptr %slot.t3
    br label %bb11

bb11:
    %v13 = load i32, ptr %slot.t3
    store i32 %v13, ptr %slot.x
    br label %bb12

bb12:
    br label %bb1

bb13:
    br label %bb14

bb14:
    %v14 = load i32, ptr %slot.x
    ret i32 %v14

bb15:
    unreachable
}

