target triple = "x86_64-pc-linux-gnu"

define i32 @add(i32 %arg0, i32 %arg1) {
entry:
    %slot.a__v1 = alloca i32
    %slot.b__v2 = alloca i32
    %slot.t1 = alloca i32
    store i32 %arg0, ptr %slot.a__v1
    store i32 %arg1, ptr %slot.b__v2
    br label %bb0

bb0:
    %v1 = load i32, ptr %slot.a__v1
    %v2 = load i32, ptr %slot.b__v2
    %v3 = add i32 %v1, %v2
    store i32 %v3, ptr %slot.t1
    br label %bb1

bb1:
    %v4 = load i32, ptr %slot.t1
    ret i32 %v4

bb2:
    unreachable
}

define i32 @main() {
entry:
    %slot.i__v4 = alloca i32
    %slot.sum__v3 = alloca i32
    %slot.t2 = alloca i32
    %slot.t3 = alloca i32
    %slot.t4 = alloca i32
    %slot.t5 = alloca i32
    br label %bb0

bb0:
    store i32 0, ptr %slot.sum__v3
    br label %bb1

bb1:
    store i32 0, ptr %slot.i__v4
    br label %bb2

bb2:
    br label %bb3

bb3:
    %v1 = load i32, ptr %slot.i__v4
    %v2 = icmp slt i32 %v1, 5
    %v3 = zext i1 %v2 to i32
    store i32 %v3, ptr %slot.t2
    br label %bb4

bb4:
    %v4 = load i32, ptr %slot.t2
    %v5 = icmp ne i32 %v4, 0
    br i1 %v5, label %bb5, label %bb11

bb5:
    %v6 = load i32, ptr %slot.sum__v3
    %v7 = load i32, ptr %slot.i__v4
    %v8 = call i32 @add(i32 %v6, i32 %v7)
    store i32 %v8, ptr %slot.t3
    br label %bb6

bb6:
    %v9 = load i32, ptr %slot.t3
    store i32 %v9, ptr %slot.sum__v3
    br label %bb7

bb7:
    br label %bb8

bb8:
    %v10 = load i32, ptr %slot.i__v4
    %v11 = add i32 %v10, 1
    store i32 %v11, ptr %slot.t4
    br label %bb9

bb9:
    %v12 = load i32, ptr %slot.t4
    store i32 %v12, ptr %slot.i__v4
    br label %bb10

bb10:
    br label %bb2

bb11:
    br label %bb12

bb12:
    %v13 = load i32, ptr %slot.sum__v3
    %v14 = icmp ne i32 %v13, 10
    %v15 = zext i1 %v14 to i32
    store i32 %v15, ptr %slot.t5
    br label %bb13

bb13:
    %v16 = load i32, ptr %slot.t5
    %v17 = icmp ne i32 %v16, 0
    br i1 %v17, label %bb14, label %bb16

bb14:
    ret i32 1

bb15:
    br label %bb17

bb16:
    br label %bb17

bb17:
    br label %bb18

bb18:
    ret i32 0

bb19:
    unreachable
}
