target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    %slot.t3 = alloca i32
    %slot.t4 = alloca i32
    %slot.t5 = alloca i32
    br label %bb0

bb0:
    %v1 = icmp sgt i32 10, 5
    %v2 = zext i1 %v1 to i32
    store i32 %v2, ptr %slot.t3
    br label %bb1

bb1:
    %v3 = load i32, ptr %slot.t3
    %v4 = icmp ne i32 %v3, 0
    br i1 %v4, label %bb2, label %bb6

bb2:
    %v5 = icmp slt i32 3, 4
    %v6 = zext i1 %v5 to i32
    store i32 %v6, ptr %slot.t4
    br label %bb3

bb3:
    %v7 = load i32, ptr %slot.t4
    %v8 = icmp ne i32 %v7, 0
    br i1 %v8, label %bb4, label %bb6

bb4:
    store i32 1, ptr %slot.t2
    br label %bb5

bb5:
    br label %bb8

bb6:
    br label %bb7

bb7:
    store i32 0, ptr %slot.t2
    br label %bb8

bb8:
    br label %bb9

bb9:
    %v9 = load i32, ptr %slot.t2
    %v10 = icmp ne i32 %v9, 0
    br i1 %v10, label %bb14, label %bb10

bb10:
    %v12 = icmp eq i32 0, 0
    %v11 = zext i1 %v12 to i32
    store i32 %v11, ptr %slot.t5
    br label %bb11

bb11:
    %v13 = load i32, ptr %slot.t5
    %v14 = icmp ne i32 %v13, 0
    br i1 %v14, label %bb14, label %bb12

bb12:
    store i32 0, ptr %slot.t1
    br label %bb13

bb13:
    br label %bb16

bb14:
    br label %bb15

bb15:
    store i32 1, ptr %slot.t1
    br label %bb16

bb16:
    br label %bb17

bb17:
    %v15 = load i32, ptr %slot.t1
    %v16 = icmp ne i32 %v15, 0
    br i1 %v16, label %bb18, label %bb20

bb18:
    ret i32 7

bb19:
    br label %bb21

bb20:
    br label %bb21

bb21:
    br label %bb22

bb22:
    ret i32 9

bb23:
    unreachable
}

