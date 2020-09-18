; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

declare i64 @input()

define i32 @add(i64 %x, i64 %y) {
Entry:
  %addtemp = add i64 %x, %y
  %trunctemp = trunc i64 %addtemp to i32
  ret i32 %trunctemp
}

define i32 @main() {
Entry:
  %calltemp = call i32 @add(i64 1, i64 2)
  ret i32 %calltemp
}

; Function Attrs: nounwind
declare void @llvm.stackprotector(i8*, i8**) #0

attributes #0 = { nounwind }
