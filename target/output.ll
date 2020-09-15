; ModuleID = "Entry"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i64 @"print"(i64 %".1") 

declare i64 @"input"() 

define i64 @"sum"(i64 %"a", i64 %"b") 
{
Entry:
  %"a.1" = alloca i64
  store i64 %"a", i64* %"a.1"
  %"b.1" = alloca i64
  store i64 %"b", i64* %"b.1"
  %"loadtemp" = load i64, i64* %"a.1"
  %"loadtemp.1" = load i64, i64* %"b.1"
  %"addtemp" = add i64 %"loadtemp", %"loadtemp.1"
  ret i64 %"addtemp"
}

define i64 @"fact"(i64 %"a") 
{
Entry:
  %"a.1" = alloca i64
  store i64 %"a", i64* %"a.1"
  %"result" = alloca i64
  store i64 1, i64* %"result"
  br label %"startloop"
startloop:
  %"loadtemp" = load i64, i64* %"a.1"
  %"cmptemp" = icmp ne i64 %"loadtemp", 0
  br i1 %"cmptemp", label %"loop", label %"endloop"
loop:
  %"loadtemp.1" = load i64, i64* %"result"
  %"loadtemp.2" = load i64, i64* %"a.1"
  %"multemp" = mul i64 %"loadtemp.1", %"loadtemp.2"
  store i64 %"multemp", i64* %"result"
  %"loadtemp.3" = load i64, i64* %"a.1"
  %"subtemp" = sub i64 %"loadtemp.3", 1
  store i64 %"subtemp", i64* %"a.1"
  br label %"startloop"
endloop:
  %"loadtemp.4" = load i64, i64* %"result"
  ret i64 %"loadtemp.4"
}

define i64 @"abs"(i64 %"x") 
{
Entry:
  %"x.1" = alloca i64
  store i64 %"x", i64* %"x.1"
  %"loadtemp" = load i64, i64* %"x.1"
  %"cmptemp" = icmp slt i64 %"loadtemp", 0
  %"cmptemp.1" = icmp ne i1 %"cmptemp", 0
  br i1 %"cmptemp.1", label %"then", label %"else"
then:
  %"loadtemp.1" = load i64, i64* %"x.1"
  %".5" = sub i64 0, %"loadtemp.1"
  br label %"murge"
else:
  %"loadtemp.2" = load i64, i64* %"x.1"
  br label %"murge"
murge:
  %"iftemp" = phi i64 [%"loadtemp.2", %"else"], [%".5", %"then"]
  ret i64 %"iftemp"
}

define i64 @"main"() 
{
Entry:
  br label %"startloop"
startloop:
  %"cmptemp" = icmp ne i64 1, 0
  br i1 %"cmptemp", label %"loop", label %"endloop"
loop:
  %"in" = alloca i64
  %"calltemp" = call i64 @"input"()
  store i64 %"calltemp", i64* %"in"
  %"result" = alloca i64
  %"loadtemp" = load i64, i64* %"in"
  %"calltemp.1" = call i64 @"abs"(i64 %"loadtemp")
  store i64 %"calltemp.1", i64* %"result"
  %"loadtemp.1" = load i64, i64* %"result"
  %"calltemp.2" = call i64 @"print"(i64 %"loadtemp.1")
  %"result.1" = alloca i64
  %"loadtemp.2" = load i64, i64* %"in"
  %"calltemp.3" = call i64 @"fact"(i64 %"loadtemp.2")
  store i64 %"calltemp.3", i64* %"result.1"
  %"loadtemp.3" = load i64, i64* %"result.1"
  %"calltemp.4" = call i64 @"print"(i64 %"loadtemp.3")
  br label %"startloop"
endloop:
  ret i64 0
}
