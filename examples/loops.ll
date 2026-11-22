target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.sum = alloca i32
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    %slot.t3 = alloca i32
    %slot.t4 = alloca i32
    %slot.x = alloca i32
    br label %bb0

bb0:
    store i32 0, ptr %slot.x
    br label %bb1

bb1:
    store i32 0, ptr %slot.sum
    br label %bb2

bb2:
    br label %bb3

bb3:
    %v1 = load i32, ptr %slot.x
    %v2 = icmp slt i32 %v1, 5
    %v3 = zext i1 %v2 to i32
    store i32 %v3, ptr %slot.t1
    br label %bb4

bb4:
    %v4 = load i32, ptr %slot.t1
    %v5 = icmp ne i32 %v4, 0
    br i1 %v5, label %bb5, label %bb15

bb5:
    %v6 = load i32, ptr %slot.x
    %v7 = icmp slt i32 %v6, 5
    %v8 = zext i1 %v7 to i32
    store i32 %v8, ptr %slot.t2
    br label %bb6

bb6:
    %v9 = load i32, ptr %slot.t2
    %v10 = icmp ne i32 %v9, 0
    br i1 %v10, label %bb7, label %bb10

bb7:
    %v11 = load i32, ptr %slot.sum
    %v12 = load i32, ptr %slot.x
    %v13 = add i32 %v11, %v12
    store i32 %v13, ptr %slot.t3
    br label %bb8

bb8:
    %v14 = load i32, ptr %slot.t3
    store i32 %v14, ptr %slot.sum
    br label %bb9

bb9:
    br label %bb11

bb10:
    br label %bb11

bb11:
    br label %bb12

bb12:
    %v15 = load i32, ptr %slot.x
    %v16 = add i32 %v15, 1
    store i32 %v16, ptr %slot.t4
    br label %bb13

bb13:
    %v17 = load i32, ptr %slot.t4
    store i32 %v17, ptr %slot.x
    br label %bb14

bb14:
    br label %bb2

bb15:
    br label %bb16

bb16:
    %v18 = load i32, ptr %slot.sum
    ret i32 %v18

bb17:
    unreachable
}

