target triple = "x86_64-pc-linux-gnu"

define i32 @main() {
entry:
    %slot.i = alloca i32
    %slot.sum = alloca i32
    %slot.t1 = alloca i32
    %slot.t2 = alloca i32
    %slot.t3 = alloca i32
    %slot.t4 = alloca i32
    %slot.t5 = alloca i32
    %slot.t6 = alloca i32
    %slot.t7 = alloca i32
    %slot.t8 = alloca i32
    %slot.t9 = alloca i32
    %slot.x = alloca i32
    br label %bb0

bb0:
    store i32 0, ptr %slot.x
    br label %bb1

bb1:
    store i32 0, ptr %slot.sum
    br label %bb2

bb2:
    store i32 1, ptr %slot.i
    br label %bb3

bb3:
    br label %bb4

bb4:
    %v1 = load i32, ptr %slot.i
    %v2 = icmp sle i32 %v1, 5
    %v3 = zext i1 %v2 to i32
    store i32 %v3, ptr %slot.t1
    br label %bb5

bb5:
    %v4 = load i32, ptr %slot.t1
    %v5 = icmp ne i32 %v4, 0
    br i1 %v5, label %bb6, label %bb18

bb6:
    %v6 = load i32, ptr %slot.i
    %v7 = icmp eq i32 %v6, 3
    %v8 = zext i1 %v7 to i32
    store i32 %v8, ptr %slot.t2
    br label %bb7

bb7:
    %v9 = load i32, ptr %slot.t2
    %v10 = icmp ne i32 %v9, 0
    br i1 %v10, label %bb8, label %bb10

bb8:
    br label %bb14

bb9:
    br label %bb11

bb10:
    br label %bb11

bb11:
    br label %bb12

bb12:
    %v11 = load i32, ptr %slot.sum
    %v12 = load i32, ptr %slot.i
    %v13 = add i32 %v11, %v12
    store i32 %v13, ptr %slot.t3
    br label %bb13

bb13:
    %v14 = load i32, ptr %slot.t3
    store i32 %v14, ptr %slot.sum
    br label %bb14

bb14:
    br label %bb15

bb15:
    %v15 = load i32, ptr %slot.i
    %v16 = add i32 %v15, 1
    store i32 %v16, ptr %slot.t4
    br label %bb16

bb16:
    %v17 = load i32, ptr %slot.t4
    store i32 %v17, ptr %slot.i
    br label %bb17

bb17:
    br label %bb3

bb18:
    br label %bb19

bb19:
    %v18 = load i32, ptr %slot.sum
    %v19 = icmp ne i32 %v18, 12
    %v20 = zext i1 %v19 to i32
    store i32 %v20, ptr %slot.t5
    br label %bb20

bb20:
    %v21 = load i32, ptr %slot.t5
    %v22 = icmp ne i32 %v21, 0
    br i1 %v22, label %bb21, label %bb23

bb21:
    ret i32 1

bb22:
    br label %bb24

bb23:
    br label %bb24

bb24:
    br label %bb25

bb25:
    br label %bb26

bb26:
    %v23 = load i32, ptr %slot.x
    %v24 = icmp slt i32 %v23, 10
    %v25 = zext i1 %v24 to i32
    store i32 %v25, ptr %slot.t6
    br label %bb27

bb27:
    %v26 = load i32, ptr %slot.t6
    %v27 = icmp ne i32 %v26, 0
    br i1 %v27, label %bb28, label %bb37

bb28:
    %v28 = load i32, ptr %slot.x
    %v29 = add i32 %v28, 1
    store i32 %v29, ptr %slot.t7
    br label %bb29

bb29:
    %v30 = load i32, ptr %slot.t7
    store i32 %v30, ptr %slot.x
    br label %bb30

bb30:
    %v31 = load i32, ptr %slot.x
    %v32 = icmp eq i32 %v31, 7
    %v33 = zext i1 %v32 to i32
    store i32 %v33, ptr %slot.t8
    br label %bb31

bb31:
    %v34 = load i32, ptr %slot.t8
    %v35 = icmp ne i32 %v34, 0
    br i1 %v35, label %bb32, label %bb34

bb32:
    br label %bb37

bb33:
    br label %bb35

bb34:
    br label %bb35

bb35:
    br label %bb36

bb36:
    br label %bb25

bb37:
    br label %bb38

bb38:
    %v36 = load i32, ptr %slot.x
    %v37 = icmp ne i32 %v36, 7
    %v38 = zext i1 %v37 to i32
    store i32 %v38, ptr %slot.t9
    br label %bb39

bb39:
    %v39 = load i32, ptr %slot.t9
    %v40 = icmp ne i32 %v39, 0
    br i1 %v40, label %bb40, label %bb42

bb40:
    ret i32 2

bb41:
    br label %bb43

bb42:
    br label %bb43

bb43:
    br label %bb44

bb44:
    ret i32 0

bb45:
    unreachable
}
