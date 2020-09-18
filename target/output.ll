; ModuleID = "Entry"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i64 @"input"() 

define i32 @"add"(i64 %"x", i64 %"y") 
{
Entry:
  %"x.1" = alloca i64
  store i64 %"x", i64* %"x.1"
  %"y.1" = alloca i64
  store i64 %"y", i64* %"y.1"
  %"x.2" = load i64, i64* %"x.1"
  %"y.2" = load i64, i64* %"y.1"
  %"addtemp" = add i64 %"x.2", %"y.2"
  %"trunctemp" = trunc i64 %"addtemp" to i32
  ret i32 %"trunctemp"
}

define i32 @"main"() 
{
Entry:
  %"calltemp" = call i32 @"add"(i64 1, i64 2)
  ret i32 %"calltemp"
}
