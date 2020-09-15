; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

declare i64 @print(i64)

declare i64 @input()

define i64 @sum(i64 %a, i64 %b) {
Entry:
  %addtemp = add i64 %a, %b
  ret i64 %addtemp
}

define i64 @fact(i64 %a) {
Entry:
  br label %startloop

startloop:                                        ; preds = %loop, %Entry
  %loadtemp.4 = phi i64 [ %multemp, %loop ], [ 1, %Entry ]
  %loadtemp.2 = phi i64 [ %subtemp, %loop ], [ %a, %Entry ]
  %cmptemp = icmp eq i64 %loadtemp.2, 0
  br i1 %cmptemp, label %endloop, label %loop

loop:                                             ; preds = %startloop
  %multemp = mul i64 %loadtemp.4, %loadtemp.2
  %subtemp = add i64 %loadtemp.2, -1
  br label %startloop

endloop:                                          ; preds = %startloop
  ret i64 %loadtemp.4
}

define i64 @abs(i64 %x) {
Entry:
  %cmptemp = icmp slt i64 %x, 0
  %.5 = sub i64 0, %x
  %iftemp = select i1 %cmptemp, i64 %.5, i64 %x
  ret i64 %iftemp
}

define i64 @main() {
Entry:
  br label %startloop

startloop:                                        ; preds = %startloop, %Entry
  %calltemp = call i64 @input()
  %0 = icmp slt i64 %calltemp, 0
  %neg = sub nsw i64 0, %calltemp
  %1 = select i1 %0, i64 %neg, i64 %calltemp
  %calltemp.2 = call i64 @print(i64 %1)
  %calltemp.3 = call i64 @fact(i64 %calltemp)
  %calltemp.4 = call i64 @print(i64 %calltemp.3)
  br label %startloop
}

; Function Attrs: nounwind
declare void @llvm.stackprotector(i8*, i8**) #0

attributes #0 = { nounwind }
